from django.shortcuts import render
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect, HttpResponse

from audiosearch.redis import client as RC
from models import ENCall, AudiosearchConstants as AC
import tasks
import util

def artist_info(request):
    request_id = request.GET['q']
    context = Context({})

    # cache check
    # HIT: get json and return
    if RC.exists(request_id):
        artist_json = RC.get(request_id)
        context.update(artist_json)
        context['served'] = True

        return render(request, 'artist.html', context)

    # MISS: create request package, defer call, return pending context
    package = ENCall('artist', 'profile')
    package.build(request_id, bucket=AC.ARTIST_PROFILE_B)
    tasks.call_API.delay(package)
    context['served'] = False

    return render(request, 'artist.html', context)






# check redis for request artist
#     if hit -> return json
#
#     else -> defer request, poll response in ajax

def artist_info_OLD(request):
    EN_id = request.GET['q']

    tasks.queue_id(EN_id)



    query = request.GET['q']
    context = Context({})

    # req = Request(query)

    tasks.call_API.delay(query)

    context['served'] = False

    return render(request, 'artist.html', context)
    # end test=================================================

    # attempt to request echo nest data, catch limit exception
    try:
        artist_ = artist.Artist(query, buckets=['biographies', 'hotttnesss', 'images', 'terms'])
        songs = song.search(artist_id=artist_.id, sort='song_hotttnesss-desc', results=35)

        # pass context as param to avoid combining both dicts
        map_artist_context(artist_, context)
        map_song_context(songs, context)

        return render(request, 'artist.html', context)

    # defer the request, return an empty page, then do an async request
    except EchoNestAPIError:
        # thread = threading.Thread(target=defer_request, args=(query))
        # thread.start()

        context['served'] = False

        return render(request, 'artist.html', context)



# serves 500 pages
def server_error(request):
    response = render(request, "500.html")
    response.status_code = 500
    return response

# will continuously 
# def defer_request(query):
    


def obtain_request(request):
    query = request.GET['q']
    print 'in obtain_request'
    data = tasks.get_data(query)
    print 'completed task'
    print data[0]
    print data[1]

    return HttpResponse(data[1], content_type="application/json")

