/* JSLint */
/* jslint browser: true */
/* global $, jQuery */
'use strict';


var AJAX_SNOOZE = 2000,
    AJAX_INITIAL_SNOOZE = 1500,
    AJAX_SLOW_THRESHOLD = 6,          // number of failed attempts before displaying 'slow results' message
    FADE_DELAY = 8000,
    NOTIF_DELAY = 1000;


function load_content(opts, data) {
    var resource_name_plus = space_to_plus(opts.resource_name),
        content_key = opts.content_key,
        data_is_paged = opts.data_is_paged,
        use_generic_key = opts.use_generic_key;

    switch (content_key) {
    case "profile":
        var offset = 0;
        $("#profile-box").show();

        for (var key in data) {
            var key_string = "#profile-" + key;

            // if (Object.prototype.toString.call(key) === '[object Array]') {
            if (key === "genres") {
                for (var i = 0; i < data[key].length; i++) {
                    var $tag = $("<li />",{
                        class: "genre-tag left",
                        text: data[key][i]
                    });

                    $(key_string).append($tag).fadeIn(150 + (offset * 180) + (100 * i));
                    $(key_string).append(" ").fadeIn(150 + (offset * 180) + (100 * i));
                }
            }
            else {
                $(key_string).append(data[key]).fadeIn(150 + (offset * 180));
            }

            offset++;
        }

        break;

    case "search_artists":
        var urls = {
                more: "?q=" + resource_name_plus + "&type=artists",
                previous: "?q=" + resource_name_plus + "&type=artists&page=" + data['previous'],
                next: "?q=" + resource_name_plus + "&type=artists&page=" + data['next'],
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

        load_table(content_key, data_is_paged, use_generic_key, data, urls);
        break;

    case "search_songs":
        var urls = {
                more: "?q=" + resource_name_plus + "&type=songs",
                previous: "?q=" + resource_name_plus + "&type=songs&page=" + data['previous'],
                next: "?q=" + resource_name_plus + "&type=songs&page=" + data['next'],
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

        load_table(content_key, data_is_paged, use_generic_key, data, urls);
        break;

    case "songs":
        var urls = {
                more: "/music/" + resource_name_plus + "/+songs/",
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

        load_table(content_key, data_is_paged, use_generic_key, data, urls);
        break;

    case "similar_artists":
        var urls = {
                previous: "?page=" + data['previous'],
                next: "?page=" + data['next'],
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

        load_table(content_key, data_is_paged, use_generic_key, data, urls);
        break;

    case "song_playlist":
        var urls = {
                previous: "?page=" + data['previous'],
                next: "?page=" + data['next'],
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

        load_table(content_key, data_is_paged, use_generic_key, data, urls);
        break;

    case "top_artists":
        var urls = {
                previous: "?page=" + data['previous'],
                next: "?page=" + data['next'],
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

        load_table(content_key, data_is_paged, use_generic_key, data, urls);
    break;

    // case "top_songs":
    //     var urls = {
    //             previous: "?type=songs&page=" + data['previous'],
    //             next: "?type=songs&page=" + data['next'],
    //             item: function(element) {
    //                 var artist = element['artist_name'],
    //                     title = element['title'],
    //                     url = "/music/" + artist + "/_/" + title + "/",

    //                     $a = $("<a />",{
    //                         text: title,
    //                         href: space_to_plus(url)
    //                     }),
    //                     $song_by_artist = $("<span />");

    //                 $song_by_artist.append($a);
    //                 $song_by_artist.append(" by " + artist);

    //                 return $song_by_artist;
    //             }
    //     };

    //     load_table(content_key, data_is_paged, use_generic_key, data, urls);
    // break;

    default:
        console.log("what is this: ");
        console.log("\t" + content_key);
        console.log("\t" + data);
    }
}


function load_table(content_key, data_is_paged, use_generic_key, data, urls) {
    //build paged table nav
    if (data_is_paged) {
        console.log("?");
        build_paged_table_nav(content_key, use_generic_key, data, urls);
    }
    //add 'more' results link
    else if (data['next'] && 'more' in urls){
        var $more_id = "#" + content_key + "-more",
            $more_a = $("<a />",{
            text: "more",
            href: space_to_plus(urls['more'])
        });
        $($more_id).append($more_a);
        console.log($more_id);
    }

    //table
    var $table_id = "#" + content_key + "-table",
        $tbody = $("<tbody />"),
        index = 0;

    //attach tbody
    if (use_generic_key) {
        $('#content-table').append($tbody);
    }
    else {
        $($table_id).append($tbody);
    }

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
        $tr.append($td_data).hide().fadeIn(150 + (index * 180));
        
        $($tbody).append($tr);

        index++;
    }
}


function build_paged_table_nav(content_key, use_generic_key, data, urls) {
    if (data['previous']) {
        var $prev_a = $("<a />",{
            text: "previous",
            href: space_to_plus(urls['previous'])
        });

        if (use_generic_key) {
            $('#previous').append($prev_a);
        }
        else {
            var $prev_id = "#" + content_key + "-previous";
            $($prev_id).append($prev_a);
        }
    }

    //current
    if ((data['previous'] || data['next']) && data['current']) {
        if (use_generic_key) {
            $('#current').text(data['current'] + " of " + data['total']);
        }
        else {
            var $current_key = "#" + content_key + "-current"; 
            $($current_key).text(data['current'] + " of " + data['total']);
        }
    }

    //next
    if (data['next']) {
        var $next_a = $("<a />",{
            text: "next",
            href: space_to_plus(urls['next'])
        });

        if (use_generic_key) {
            $('#next').append($next_a);
        }
        else {
            var $next_id = "#" + content_key + "-next";
            $($next_id).append($next_a);
            console.log($next_id);
        }
    }
}


function hide_spinner(content_key, use_generic_key) {
    if (use_generic_key) {
        $("#content-spinner").hide();
        $("#content-slow").hide();
    }
    else {
        var $spinner = "#" + content_key + "-spinner",
            $slow_id = "#" + content_key + "-slow";

        $($spinner).hide();
        $($slow_id).hide();
    }
}


function handle_failed(content_key, use_generic_key) {
    console.log("in handle_failed: " + content_key);

    if (use_generic_key) {
        var $div_id = "#content-notification";
    }
    else {
        var $div_id = "#" + content_key + "-notification";
    }

    if ($($div_id).is(":visible")) {
        $($div_id).fadeOut(NOTIF_DELAY);
        
        setTimeout(function() {
            $($div_id).html(' ');
            $($div_id).text("There was an error retrieving this content.").fadeIn(NOTIF_DELAY);
        }
        , NOTIF_DELAY + 200);
    }
    else {
        $($div_id).html('');
        $($div_id).text("There was an error retrieving this content.").fadeIn(NOTIF_DELAY);
    }
}


function handle_slow_results(content_key, use_generic_key) {
    if (use_generic_key) {
        var $div_id = "#content-slow";
    }
    else {
        var $div_id = "#" + content_key + "-slow";
    }

    $($div_id).text("This request appears to be taking longer than expected.").fadeIn(NOTIF_DELAY);
}


function dispatch(opts) {
    if (opts.content_key === "profile") { return false }
    opts.attempt++;

    if (opts.attempt == 3) {
        handle_slow_results(opts.content_key, opts.use_generic_key);
    }

    if (opts.attempt == 6) {
        handle_failed(opts.content_key, opts.use_generic_key);
    }

    setTimeout(function() {
            dispatch(opts);
        }
    , AJAX_SNOOZE);

    

    $.ajax({
        url: "/ajax/retrieval/",
        data: opts,
        dataType: 'json',
        type: 'GET',
        success: function(json_context, stat, o) {
        //     switch (json_context['status']) {
        //     case 'complete':
        //         hide_spinner(opts.content_key, opts.use_generic_key);
        //         load_content(opts, json_context['data']);

        //         break;

        //     case 'pending':
        //         if (opts.attempt > AJAX_SLOW_THRESHOLD) {
        //             handle_slow_results(opts.content_key, opts.use_generic_key);
        //         }
        //         opts.attempt++;

        //         setTimeout(function() {
        //                 dispatch(opts);
        //             }
        //         , AJAX_SNOOZE);

        //         break;

        //     case 'failed':
        //         handle_failed(opts.content_key, opts.use_generic_key);

        //         break;
        //     }  
        }
        // ,
        // error: function(o, stat, er) {},
        // complete: function(o, stat) {}
    });
}



