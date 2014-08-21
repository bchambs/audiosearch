/* JSLint */
/* jslint browser: true */
/* global $, jQuery */
'use strict';


var AJAX_SNOOZE = 2000,             // Time in ms between failed AJAX requests.
    AJAX_INITIAL_SNOOZE = 1500,     // Initial delay in ms before beginning AJAX requests.
    AJAX_SLOW_THRESHOLD = 6,        // Number of failed attempts before displaying 'slow results' message.
    AJAX_FAIL_THRESHOLD = 15,       // Number of failed attempts before displaying 'failed' message and halting AJAX requests.
    FADE_DELAY = 8000,
    NOTIF_DELAY = 1000,


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


    // Added this to allow more 'top content' on /music/.  The results are lackluster.
    // case "top_songs":
    //     var urls = {
    //             previous: "?type=songs&page=" + data['previous'],
    //             next: "?type=songs&page=" + data['next'],
    //             item: song_table_link_generator
    //     };

    //     load_table(content_key, data_is_paged, use_generic_key, data, urls);
    // break;


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
    if (use_generic_key) {
        var $div_id = "#content-notification";
    }
    else {
        var $div_id = "#" + content_key + "-notification";
    }

    // If an existing notification is displayed, remove it, then fadein the failure message.
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
        var $div_id = "#content-notification";
    }
    else {
        var $div_id = "#" + content_key + "-notification";
    }

    $($div_id).text("This request appears to be taking longer than expected.").fadeIn(NOTIF_DELAY);
}


function handle_no_results(content_key, use_generic_key) {
    if (use_generic_key) {
        var $div_id = "#content-notification";
    }
    else {
        var $div_id = "#" + content_key + "-notification";
    }

    if (content_key === "search_songs" || content_key === "search_artists") {
        var msg = "Your search did not match any music data."
    }
    else {
        var msg = "We could not find data for this item."
    }

    $($div_id).text(msg).fadeIn(NOTIF_DELAY);
}

// Send AJAX request for content status update.  
// @opts contain various request information and is defined in static_AJAX_OPTS.html template.
// On status = success, load the content according to its data type (table, string, etc).
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
                // Check if past failure threshold.
                if (opts.attempt > AJAX_FAIL_THRESHOLD) {
                    hide_spinner(opts.content_key, opts.use_generic_key);
                    handle_failed(opts.content_key, opts.use_generic_key);

                    break;
                }
                else {
                    // Check if past slow load threshold.
                    if (opts.attempt > AJAX_SLOW_THRESHOLD) {
                        handle_slow_results(opts.content_key, opts.use_generic_key);
                    }

                    // Continue AJAX requests.
                    opts.attempt++;
                    setTimeout(function() {
                            dispatch(opts);
                        }
                    , AJAX_SNOOZE);
                }

                break;

            case 'empty':
                hide_spinner(opts.content_key, opts.use_generic_key);
                handle_no_results(opts.content_key, opts.use_generic_key);

                break;

            case 'failed':
                hide_spinner(opts.content_key, opts.use_generic_key);
                handle_failed(opts.content_key, opts.use_generic_key);

                break;
            }  
        }
        // ,
        // error: function(o, stat, er) {},
        // complete: function(o, stat) {}
    });
}



