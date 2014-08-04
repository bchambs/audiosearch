/* JSLint */
/* jslint browser: true */
/* global $, jQuery */


var AJAX_SNOOZE = 2000,
    ATTEMPT_LIMIT = 4,
    FADE_DELAY = 8000;


function load_content(resource_id, content_key, data) {
    'use strict';

    switch (content_key) {
    case "profile":
        for (var key in data) {
            var key_string = "#" + content_key + "-" + key;

            if (Object.prototype.toString.call(key) === '[object Array]') {
                for (var i = 0; i < data[key].length; i++) {
                    $(key_string).append(data[key][i]).fadeIn(FADE_DELAY);
                }
            }
            else {
                $(key_string).append(data[key]).fadeIn(FADE_DELAY);
            }
        }

        break;

    case "search_artists":
        var urls = {
                view_more: "?q=" + resource_id + "&type=artists",
                previous: "?q=" + resource_id + "&type=artists&page=" + data['previous'],
                next: "?q=" + resource_id + "&type=artists&page=" + data['next'],
                item: function(element) {
                    var artist = element['name'],
                        url = "/music/" + artist + "/",

                        $a = $("<a />",{
                            text: artist,
                            href: space_to_plus(url)
                        });

                    return $a;
                }
        };

        load_paged_table(resource_id, content_key, data, urls);
        break;

    case "search_songs":
        var urls = {
                view_more: "?q=" + resource_id + "&type=songs",
                previous: "?q=" + resource_id + "&type=songs&page=" + data['previous'],
                next: "?q=" + resource_id + "&type=songs&page=" + data['next'],
                item: function(element) {
                    var artist = element['artist_name'],
                        title = element['title'],
                        url = "/music/" + artist + "/" + title + "/",

                        $a = $("<a />",{
                            text: title,
                            href: space_to_plus(url)
                        });

                    return $a;
                }
        };

        load_paged_table(resource_id, content_key, data, urls);
        break;

    case "songs":
        var urls = {
                view_more: "songs/",
                previous: "?page=" + data['previous'],
                next: "?page=" + data['next'],
                item: function(element) {
                    var artist = element['artist_name'],
                        title = element['title'],
                        url = "/music/" + artist + "/" + title + "/",

                        $a = $("<a />",{
                            text: title,
                            href: space_to_plus(url)
                        });

                    return $a;
                }
        };

        load_paged_table(resource_id, content_key, data, urls);
        break;

    case "similar_artists":
        var urls = {
                view_more: "similar/?type=artists",
                previous: "?type=artists&page=" + data['previous'],
                next: "?type=artists&page=" + data['next'],
                item: function(element) {
                    var artist = element['name'],
                        url = "/music/" + artist + "/",

                        $a = $("<a />",{
                            text: artist,
                            href: space_to_plus(url)
                        });

                    return $a;
                }
        };

        load_paged_table(resource_id, content_key, data, urls);
        break;

    case "similar_songs":
        var urls = {
                view_more: "similar/?type=songs",
                previous: "?type=songs&page=" + data['previous'],
                next: "?type=songs&page=" + data['next'],
                item: function(element) {
                    var artist = element['artist_name'],
                        title = element['title'],
                        url = "/music/" + artist + "/" + title + "/",

                        $a = $("<a />",{
                            text: title,
                            href: space_to_plus(url)
                        });

                    return $a;
                }
        };

        load_paged_table(resource_id, content_key, data, urls);
        break;

        default:
            console.log("what is this: ");
            console.log("\t" + content_key);
            console.log("\t" + data);
    }
}


function load_paged_table(resource_id, content_key, data, urls) {
    console.log("load_paged_table::" + content_key);
    var $table_id_key = "#" + content_key + "-table";

    //tfoot
    //display 'view more results' 
    if (typeof display_more !== 'undefined' && display_more && data['next']) {
        var $tfoot_key = "#" + content_key + "-tfoot", 
            $tr = $("<tr />"),
            $td = $("<td />").attr('colspan', 2),
            $more_a = $("<a />",{
                text: "view more",
                href: space_to_plus(urls['view_more'])
            });
            $td.append($more_a);
            $tr.append($td);
            $($tfoot_key).append($tr);
    }

    //display page nav
    else {

        //previous
        if (data['previous']) {
            var $previous_key = "#" + content_key + "-previous", 
            $prev_a = $("<a />",{
                text: "previous",
                href: space_to_plus(urls['previous'])
            });

            $($previous_key).append($prev_a);
        }

        //current
        if (data['current']) {
            var $current_key = "#" + content_key + "-current"; 
            $($current_key).text(data['current'] + " of " + data['total']);
        }

        //next
        if (data['next']) {
            var $next_key = "#" + content_key + "-next", 
            $next_a = $("<a />",{
                text: "next",
                href: space_to_plus(urls['next'])
            });

            $($next_key).append($next_a);
        }
    }

    //tbody
    var $tbody_key = "#" + content_key + "-tbody",
        index = 0;

    for (var item in data['data']) {
        var $tr = $("<tr />"),
            $td_index = $("<td />"),
            $td_data = $("<td />"),
            $item_a = urls['item'](data['data'][item]);

        $td_index.append(index + data['offset']);
        $td_data.append($item_a);
        $tr.append($td_index);
        $tr.append($td_data);
        $($tbody_key).append($tr);

        index++;
    }
}


// remove loader image, display sad face, display error notification
function handle_timeout(content_key, message) {
    'use strict';
    console.log("in handle_timeout: " + content_key);
    console.log(message);
}


function dispatch(resource, resource_id, content_key, attempt, page) {
    'use strict';

    var params = {
        'resource': resource,
        'content_key': content_key
    }

    if (page) {
        params['page'] = page;
    }

    $.ajax({
        url: "/ajax/retrieval/",
        data: params,
        dataType: 'json',
        type: 'GET',
        success: function(data, stat, o) {
            switch (data['status']) {
                case 'success':
                    load_content(resource_id, content_key, data[content_key]);

                    break;

                case 'pending':
                    if (attempt > ATTEMPT_LIMIT) {
                        handle_timeout(content_key, o);
                    }
                    else {
                        setTimeout(function() {
                                dispatch(resource, resource_id, content_key, ++attempt, page);
                            }
                        , AJAX_SNOOZE);
                    }

                    break;
            }
        }
        // ,
        // error: function(o, stat, er) {},
        // complete: function(o, stat) {}
    });
}



