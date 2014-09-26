from __future__ import absolute_import

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


_N_CONTENT_ROWS = 10    # Default number of rows in content table.
NAV_MORE = 'more'
NAV_PAGES = 'pages'


def build_template_map(available, failed, page, n_items, nav_style):
    
    complete = dict()

    for res, data in (available + failed):
        template_dict = {
            'div_id': res.id,
            'title': res.title,
            'nav_style': nav_style,
        }
        try:
            processed_data = _page(res, page, n_items)
        except TypeError:
            processed_data = data
        template_dict.update(processed_data)
        complete[res.name].update(template_dict)

    return complete


def _page(resource, page, n_items):
    """Create paged content dict for generate template tables."""

    n_items = n_items or _N_CONTENT_ROWS
    paginator = Paginator(resource, n_items)

    try:
        paged = paginator.page(page)
    except PageNotAnInteger:
        paged = paginator.page(1)
    except EmptyPage:
        paged = paginator.page(paginator.num_pages)

    # Need to create paged dict because we cannot seralize Django's paged class.
    paged_data = {
        'data': paged.object_list,
        'next': paged.next_page_number() if paged.has_next() else None,
        'previous': paged.previous_page_number() if paged.has_previous() else None,
        'current': paged.number,
        'total': paged.paginator.num_pages,
        'offset': paged.start_index(),
    }

    return paged_data



# class NavStyle(object):
#     """Content header navigation enums."""
#     more = 'more'
#     pages = 'pages'
# NAV_STYLE = NavStyle()



# def build_content_from_data(available_resources, nav, page=None, n_items=None):
#     content = {}

#     for resource, data in available_resources:
#         template_content = {
#             'div_id': resource.div_id,
#             'title': resource.title,
#             'display_page_nav': nav,
#         }
        
#         try:
#             template_content[resource.div_id] = _page(data, page, n_items)
#         except AttributeError:
#             template_content[resource.div_id] = data

#     return content






# def create_template_content(resource_map, page, n_items, is_home_page):
#     complete = {}

#     for resource, content in resource_map.items():
#         template_content = {
#             'div_id': resource.div_id,
#             'title': resource.title,
#             'display_page_nav': is_home_page,
#         }
#         paged_content = page_content(content, page, n_items)
#         template_content.update(paged_content)
#         complete[resource.div_id] = template_content

#     return complete







