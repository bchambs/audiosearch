from __future__ import absolute_import

import logging

from celery import shared_task
from redis import WatchError

from audiosearch import config as cfg
from audiosearch.config import T_HASH, T_CONTENT, T_MIN, T_COUNT
from audiosearch.redis_client import store
from src.consumer import ENConsumer
import src.services as services


logger = logging.getLogger("general_logger")


# Consume RESTful service, process response data, and store in cache.
@shared_task
def generate_resource(resource_id, content_key, service):
    pipe = cache.pipeline()

    try:
        if service.dependency:
            intermediate = ENConsumer.consume(service.dependency)
            service.build(intermediate)

        echo_nest_response = ENConsumer.consume(service)

        try:
            content = service.trim(echo_nest_response)
        except AttributeError:
            pass

        content_struct = {
            'status': "complete",
            'data': content,
        }

        pipe.hset(resource_id, content_key, content_struct)

    # Received error message in EchoNest response.
    except services.EchoNestServiceFailure as err_msg:
        content_struct = {
            'status': "failed",
            'error_message': str(err_msg),
        }
        pipe.hset(resource_id, content_key, content_struct)

        logger.warning("Service Failure::%s, %s, %s") %(resource_id, content_key, service)
        logger.warning("Error   Message::%s") %(err_msg)
        
    # Service or dependency returned zero results.
    except services.EmptyServiceResponse:
        content_struct = {
            'status': "empty",
            'error_message': "None.",
        }
        pipe.hset(resource_id, content_key, content_struct)

    pipe.expire(resource_id, service.ttl)
    pipe.execute()


@shared_task
def log_dbsize():
    pipe = cache.pipeline()
    pipe.dbsize()
    pipe.hlen(T_HASH)
    pipe.get(T_CONTENT)

    key_count, trending_count, trending_content = pipe.execute()

    # Key report
    report_text = "Key Report"
    side_banner = '~' *  7
    bottom_banner = '~' * (len(side_banner) * 2 + len(report_text))

    logger.info("%s%s%s") %(side_banner, report_text, side_banner)
    logger.info("DB KEY COUNT: %s" %(key_count))
    logger.info("TRENDING KEY COUNT: %s" %(trending_count))
    logger.info("%s" %(bottom_banner))

    # Trending report
    report_text = "Trending Report"

    logger.info("%s%s%s") %(side_banner, report_text, side_banner)
    for item, views in trending_content.items():
        logger.info("%s:%s" %(item, views))
    logger.info("%s" %(bottom_banner))


# T_MIN, min_list = List tracking 
# T_CONTENT, content = Hash of top [T_COUNT] trending items
# T_HASH = Map of all { resource_id : view count }.  
@shared_task
def maintain_trending(resource_id):
    # If the value of the lowest trending item is modified during this block, we
    # could be storing incorrect trending data.  This block will throw an exception
    # if T_MIN is modified before we execute the pipe and restart the loop.
    with cache.pipeline() as pipe:
        while 1:
            try:
                pipe.hincrby(T_HASH, resource_id, 1)
                pipe.hgetall(T_CONTENT)
                pipe.lrange(T_MIN, 0, T_COUNT - 1)
                view_count, content, min_list = pipe.execute()

                # Except if trending:min or trending:content is modified.
                pipe.watch(T_MIN, T_CONTENT)

                # First item tracked.  Update min_list and content.
                # NOTE: this should only occur if the cache was flushed.
                if not content and not min_list:
                    logger.warning("Zero trending items found.  Building Trending data.")

                    pipe.multi()
                    pipe.lpush(T_MIN, resource_id)
                    pipe.hset(T_CONTENT, resource_id, view_count)
                    pipe.execute()

                    break


                min_item = min_list[0]
                min_views = content.get(min_item)
                pipe.multi()

                # If task is already trending, update content and pass.
                if resource_id in content:
                    print "in 1"
                    pipe.hset(T_CONTENT, resource_id, view_count)
                    pass

                # We're below the trending count threshold.
                # Update min_list and content accordingly.
                # NOTE: this should only occur if the cache was flushed.
                elif len(content) < T_COUNT:
                    print "in 3"
                    logger.warning("Not enough trending items.")

                    pipe.hset(T_CONTENT, resource_id, view_count)

                    if view_count > min_views:
                        pipe.LINSERT("BEFORE", lambda a: min_views < a, resource_id)
                        yes = True
                    else:
                        pipe.lpush(T_MIN, resource_id)


                # New trending item:
                #   1. Remove min_item from trending:content.
                #   2. Pop min_views from trending:list.
                #   3. Push view_count to appropriate place in min_list.
                #   3. Add { resource_id:view_count } to trending:content.
                elif view_count > min_views:
                    print "in 4"

                    pipe.hdel(T_CONTENT, min_item)
                    pipe.lpop(T_MIN)
                    pipe.LINSERT("BEFORE", lambda a: min_views < a, resource_id)
                    pipe.hset(T_CONTENT, resource_id, view_count)

                pipe.execute()
                break

            except WatchError:
                pass



