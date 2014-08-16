/* JSLint */
/* jslint browser: true */
/* global $, jQuery */
'use strict';


var AJAX_SNOOZE = 2000,
    AJAX_INITIAL_SNOOZE = 1500,
    ATTEMPT_LIMIT = 4,
    FADE_DELAY = 8000;


function load_content(opts, data) {
    var resource_id = opts.resource_id,
        content_key = opts.content_key,
        data_is_paged = opts.data_is_paged,
        use_generic_key = opts.use_generic_key;

    switch (content_key) {
    case "profile":
        for (var key in data) {
            var key_string = "#profile-" + key;

            if (Object.prototype.toString.call(key) === '[object Array]') {
                for (var i = 0; i < data[key].length; i++) {
                    $(key_string).append(data[key][i]);
                }
            }
            else {
                $(key_string).append(data[key]);
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

        load_table(resource_id, content_key, data_is_paged, use_generic_key, data, urls);
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
                        }),
                        $song_by_artist = $("<span />");

                    $song_by_artist.append($a);
                    $song_by_artist.append(" by " + artist);

                    return $song_by_artist;
                }
        };

        load_table(resource_id, content_key, data_is_paged, use_generic_key, data, urls);
        break;

    case "songs":
        var urls = {
                view_more: "songs/",
                previous: "?page=" + data['previous'],
                next: "?page=" + data['next'],
                item: function(element) {
                    var artist = element['artist_name'],
                        title = element['title'],
                        url = "/music/" + artist + "/_/" + title + "/",

                        $a = $("<a />",{
                            text: title,
                            href: space_to_plus(url)
                        });

                    return $a;
                }
        };

        load_table(resource_id, content_key, data_is_paged, use_generic_key, data, urls);
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

        load_table(resource_id, content_key, data_is_paged, use_generic_key, data, urls);
        break;

    case "song_playlist":
        var urls = {
                view_more: "similar/?type=songs",
                previous: "?type=songs&page=" + data['previous'],
                next: "?type=songs&page=" + data['next'],
                item: function(element) {
                    var artist = element['artist_name'],
                        title = element['title'],
                        url = "/music/" + artist + "/_/" + title + "/",

                        $a = $("<a />",{
                            text: title,
                            href: space_to_plus(url)
                        }),
                        $song_by_artist = $("<span />");

                    $song_by_artist.append($a);
                    $song_by_artist.append(" by " + artist);

                    return $song_by_artist;
                }
        };

        load_table(resource_id, content_key, data_is_paged, use_generic_key, data, urls);
        break;

    case "top_artists":
        var urls = {
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

        load_table(resource_id, content_key, data_is_paged, use_generic_key, data, urls);
    break;

    default:
        console.log("what is this: ");
        console.log("\t" + content_key);
        console.log("\t" + data);
    }
}


function load_table(resource_id, content_key, data_is_paged, use_generic_key, data, urls) {
    if (data_is_paged) {
        build_paged_table_nav(content_key, data, urls);
    }

    //table
    var $table_key = "#" + content_key + "-table",
        $tbody = $("<tbody />"),
        index = 0;

    //build rows / columns
    for (var item in data['data']) {
        if (index % 2 === 0) {
            var row_class = "even";
        }
        else {
            var row_class = "odd";
        }

        var $tr = $("<tr />",{
                class: row_class
            }),
            $td_index = $("<td />",{
                class: 'index'
            }),
            $td_data = $("<td />"),
            $item_a = urls['item'](data['data'][item]);

        $td_index.append(index + data['offset'] + ".");
        $td_data.append($item_a);
        $tr.append($td_index);
        $tr.append($td_data);
        
        $($tbody).append($tr);

        index++;
    }

    //attach to table
    // if (Boolean(use_generic_key)) {
    if (use_generic_key) {
        $('#content-table').append($tbody);
    }
    else {
        $($table_key).append($tbody);
    }
}


function build_paged_table_nav(content_key, data, urls) {
    //previous
    if (data['previous']) {
        var $previous_key = "#" + content_key + "-previous", 
            $prev_a = $("<a />",{
            text: "previous",
            href: space_to_plus(urls['previous'])
        });

        $('#previous').append($prev_a);
    }

    //current
    if ((data['previous'] || data['next']) && data['current']) {
        var $current_key = "#" + content_key + "-current"; 

        $('#current').text(data['current'] + " of " + data['total']);
    }

    //next
    if (data['next']) {
        var $next_key = "#" + content_key + "-next", 
            $next_a = $("<a />",{
            text: "next",
            href: space_to_plus(urls['next'])
        });

        $('#next').append($next_a);
    }
}


function hide_spinner(content_key, use_generic_key) {
    if (use_generic_key) {
        $("#content-spinner").hide();
    }
    else {
        var $spinner = "#" + content_key + "-spinner";
        $($spinner).hide();
    }
}


function handle_timeout(content_key, message) {
    console.log("in handle_timeout: " + content_key);
    console.log(message);
}


function dispatch(opts) {
    $.ajax({
        url: "/ajax/retrieval/",
        data: opts,
        dataType: 'json',
        type: 'GET',
        success: function(json_context, stat, o) {
            switch (json_context['status']) {
            case 'complete':
                hide_spinner(opts.content_key, opts.use_generic_key);
                load_content(opts, json_context['data']);

                break;

            case 'pending':
                if (opts.attempt > ATTEMPT_LIMIT) {
                    handle_timeout(opts.content_key, o);
                }
                else {
                    opts.attempt++;

                    setTimeout(function() {
                            dispatch(opts);
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



