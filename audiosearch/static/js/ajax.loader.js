/* JSLint */
/* jslint browser: true */
/* global $, jQuery */
'use strict';


var AJAX_SNOOZE = 2000,             // Time in ms between failed AJAX requests.
    AJAX_INITIAL_SNOOZE = 1500,     // Initial delay in ms before beginning AJAX requests.
    AJAX_SLOW_THRESHOLD = 6,        // Number of failed attempts before displaying 'slow results' message.
    AJAX_SLOW_MSG = "This request appears to be taking longer than expected.",
    AJAX_FAIL_THRESHOLD = 15,       // Number of failed attempts before displaying 'failed' message and halting AJAX requests.
    AJAX_FAIL_MSG = "There was an error retrieving this content.",
    HIDE_DELAY = 600,
    SHOW_DELAY = 1000,


    // Used to build table row links.
    artist_table_link_generator = function(element) {
        var artist = element['name'],
            url = "/music/" + artist + "/",

            $a = $("<a />",{
                text: artist,
                href: space_to_plus(url)
            });

        return $a;
    },


    // Used to build table row links for artist playlist.
    song_table_link_generator = function(element, include_by_artist) {
        var artist = element['artist_name'],
            title = element['title'],
            url = "/music/" + artist + "/_/" + title + "/",

            $a = $("<a />",{
                text: title,
                href: space_to_plus(url)
            });

        return $a;
    },


    // Used to build table row links including 'by (artist)'.
    song_artist_table_link_generator = function(element, include_by_artist) {
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
    };


// Urls are a mess because of front-end redesign.  
// If content_key is profile, attach items to html.
// Else, build a url map, then pass all data to the table builder.
function load_content(opts, data) {
    var resource_name_plus = space_to_plus(opts.resource_name),
        content_key = opts.content_key,
        data_is_paged = opts.data_is_paged,
        use_generic_key = opts.use_generic_key;

    // TODO: generate urls in python, pass it in opts, remove giant switch.
    switch (content_key) {

    // Profile for artist and song.
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

                    $(key_string).append($tag);
                    $(key_string).append(" ");
                }
            }
            else {
                $(key_string).append(data[key]).fadeIn(150 + (offset * 180));
            }

            offset++;
        }

        break;


    // Artist results for search query.
    case "search_artists":
        var urls = {
                more: "?q=" + resource_name_plus + "&type=artists",
                previous: "?q=" + resource_name_plus + "&type=artists&page=" + data['previous'],
                next: "?q=" + resource_name_plus + "&type=artists&page=" + data['next'],
                item: artist_table_link_generator
        };

        load_table(content_key, data_is_paged, use_generic_key, data, urls);
        break;


    // Song results for search query.
    case "search_songs":
        var urls = {
                more: "?q=" + resource_name_plus + "&type=songs",
                previous: "?q=" + resource_name_plus + "&type=songs&page=" + data['previous'],
                next: "?q=" + resource_name_plus + "&type=songs&page=" + data['next'],
                item: song_artist_table_link_generator
        };

        load_table(content_key, data_is_paged, use_generic_key, data, urls);
        break;


    // Artist songs.
    case "songs":
        var urls = {
                more: "/music/" + resource_name_plus + "/+songs/",
                previous: "?page=" + data['previous'],
                next: "?page=" + data['next'],
                item: song_table_link_generator
        };

        load_table(content_key, data_is_paged, use_generic_key, data, urls);
        break;


    // Recommended artists for song items.
    // Similar artists for artist items.
    case "similar_artists":
        var urls = {
                previous: "?page=" + data['previous'],
                next: "?page=" + data['next'],
                item: artist_table_link_generator
        };

        load_table(content_key, data_is_paged, use_generic_key, data, urls);
        break;


    // Similar songs for song items.
    // Recommended songs for artist items.
    case "song_playlist":
        var artist_name_plus = space_to_plus(opts.artist_name);
        var urls = {
                more: "/music/" + artist_name_plus + "/_/" + resource_name_plus + "/+similar/",
                previous: "?page=" + data['previous'],
                next: "?page=" + data['next'],
                item: song_artist_table_link_generator
        };

        load_table(content_key, data_is_paged, use_generic_key, data, urls);
        break;


    // Content displayed on /music/
    case "top_artists":
        var urls = {
                previous: "?page=" + data['previous'],
                next: "?page=" + data['next'],
                item: artist_table_link_generator
        };

        load_table(content_key, data_is_paged, use_generic_key, data, urls);
    break;


    // Catch invalid content_keys.
    default:
        console.log("what is this: ");
        console.log("\t" + content_key);
        console.log("\t" + data);
    }
}


// Create rows / columns by iterating through data object.  Use urls object to generate the appropriate link structure.
function load_table(content_key, data_is_paged, use_generic_key, data, urls) {
    // build paged table nav
    if (data_is_paged) {
        build_paged_table_nav(content_key, use_generic_key, data, urls);
    }
    // add 'more' results link
    else if (data['next'] && 'more' in urls){
        var $more_id = "#" + content_key + "-more",
            $more_a = $("<a />",{
            text: "more",
            href: space_to_plus(urls['more'])
        });
        $($more_id).append($more_a);
    }

    var $table_id = "#" + content_key + "-table",
        $tbody = $("<tbody />"),
        index = 0;

    // Attach tbody.
    if (use_generic_key) {
        $('#content-table').append($tbody);
    }
    else {
        $($table_id).append($tbody);
    }

    // build rows / columns from data list
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


// Use_generic_key determines if the target div id uses content_key in the string or uses the generic 'content' value.
function build_paged_table_nav(content_key, use_generic_key, data, urls) {
    // previous div
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

    // current div
    if ((data['previous'] || data['next']) && data['current']) {
        if (use_generic_key) {
            $('#current').text(data['current'] + " of " + data['total']);
        }
        else {
            var $current_key = "#" + content_key + "-current"; 
            $($current_key).text(data['current'] + " of " + data['total']);
        }
    }

    // next div
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
        }
    }
}


function handle_failed() {
    var $div_id = "#content-notification";

    $($div_id).fadeOut(HIDE_DELAY);

    setTimeout(function() {
            $($div_id).text(AJAX_FAIL_MSG).fadeIn(SHOW_DELAY);
        }, HIDE_DELAY);
    //OLD
    // if (use_generic_key) {
    //     var $div_id = "#content-notification";
    // }
    // else {
    //     var $div_id = "#" + content_key + "-notification";
    // }

    // // If an existing notification is displayed, remove it, then fadein the failure message.
    // if ($($div_id).is(":visible")) {
    //     $($div_id).fadeOut(NOTIF_DELAY);
        
    //     setTimeout(function() {
    //         $($div_id).html(' ');
    //         $($div_id).text("There was an error retrieving this content.").fadeIn(NOTIF_DELAY);
    //     }
    //     , NOTIF_DELAY + 200);
    // }
    // else {
    //     $($div_id).html('');
    //     $($div_id).text("There was an error retrieving this content.").fadeIn(NOTIF_DELAY);
    // }
}


function load_resource_table(res_data, div_id) {
    var $table_id = "#" + div_id + "-table",
        $tbody = $("<tbody />"),
        index = 0;

    $($table_id).append($tbody);

    for (var index = 0, len = res_data.length - 1; index < len; index++) {
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
            $td_data = $("<td />");
            // $item_a = urls['item'](res_data[item]);

        // $td_index.append(index + res_data['offset'] + ".");
        // $td_data.append($item_a);
        $td_index.append((index + 1) + ".");
        $td_data.append(res_data[index].name);
        $tr.append($td_index);
        $tr.append($td_data).hide().fadeIn(150 + (index * 180));  
        
        $($tbody).append($tr);
    }

    console.log($table_id);
    for (var key in res_data[0]) {
        if (res_data[0].hasOwnProperty(key)) {
            console.log(key + ": " + res_data[0][key]);
        }
    }
}


function load_profile(res_data, div_id) {
    var offset = 0;
    $("#profile-box").show();

    for (var key in res_data) {
        var key_string = "#profile-" + key; // make this profile-data

        if (key === "genres") {
            for (var i = 0; i < res_data[key].length; i++) {
                var $tag = $("<li />",{
                    class: "genre-tag left",
                    text: res_data[key][i]
                });

                $(key_string).append($tag);
                $(key_string).append(" ");
            }
        }
        else {
            $(key_string).append(res_data[key]).fadeIn(150 + (offset * 180));
        }

        offset++;
    }
}


function load_resource_data(res_data, res_type, div_id) {
    if (res_type === 'profile') {
        load_profile(res_data, div_id);
    }
    else {
        load_resource_table(res_data, div_id);
    }
}


function hide_spinner(div_id) {
    $("#" + div_id + "-spinner").hide();
}


function dispatch(opts, attempt) {
    $.ajax({
        url: "/ajax/retrieval/",
        data: opts,
        dataType: 'json',
        contentType: "application/json",
        type: 'GET',
        success: function(context, stat, o) {
            console.log(context['status']);

            switch (context['status']) {

            case 'complete':
                var res_data = context['resource_data'],
                    res_type = context['resource_type'],
                    div_id = context['div_id'];


                // console.log(res_data);
                console.log(res_type);
                console.log(div_id);


                hide_spinner(div_id);
                load_resource_data(res_data, res_type, div_id);
                break;

            case 'pending':
                if (attempt > AJAX_FAIL_THRESHOLD) {
                    // handle failed.
                    return false;
                }
                else {
                    // Continue AJAX requests.
                    setTimeout(function() {
                        dispatch(opts, attempt++)
                    }, AJAX_SNOOZE);
                }
                break;

            case 'failed':
                // handle failed.
                break;
            }  
        },
        error: function(o, stat, er) {
            return false;
        }
        // ,complete: function(o, stat) {}
    });
}



