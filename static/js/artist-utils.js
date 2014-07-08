/* JSLint */
/* jslint browser: true */
/* global $, jQuery */
// TODO: move all 'use strict' to top of files

/**
    Utility functions for loading and displaying artist resources.
*/

var TIMEOUT_MESSAGE = 'Unable to connect to the Echo Nest.',
    AJAX_SNOOZE = 1000,
    ATTEMPT_LIMIT = 10,
    FADE_DELAY = 1000,

    q = get_query_string();


/**
    @return {string} q Query string.
*/
function get_query_string() {
    'use strict';

    var query = window.location.search.split("="),
        regex = /^[a-z0-9]+$/i;

    if (query.length === 2) {
        if (regex.test(query[1])) {
            return query[1];
        }
    }

    return '';
}


/**
    Attempt to load deferred Echo Nest requests.
    The artist id and resource name are used as params to the jQuery AJAX function.
     If requested data is not ready (not in cache), sleep for AJAX_SNOOZE milliseconds.
     Request will timeout after ATTEMPT_LIMIT failed retrievals.
     AJAX calls switch on response status*: 
        On success: switch by resource value to appropriate display function.
        On error: (pass)
     * This is the status of the AJAX request, not the status value in the returned json.
    @param {string} id Artist hash obtained from query string.
    @param {string} resource Name of pending request item: profile, songs, or similar
    @param {integer} attempt Count of failed AJAX retrievals.
*/
function dispatch(id, resource, attempt) {
    'use strict';

    // TODO: use AJAX fail instead of data['status']
    $.ajax({
        url: '/artistjx/',
        data: {
            'q': id,
            'resource': resource
        },
        dataType: 'json',
        type: 'GET',
        success: function(data, stat, o) {
            if (data['status'] === 'ready') {
                console.log('ajax.success: ' + stat)

                switch(resource) {
                    case 'profile':
                        display_profile(data[resource]);
                        break;

                    case 'songs':
                        display_songs(data[resource]);
                        break;

                    case 'similar':
                        display_similar(data[resource]);
                        break;
                }
            }
            else if (data['status'] === 'pending') {
                attempt++;

                if (attempt > ATTEMPT_LIMIT) {
                    console.log('timeout')
                    handle_timeout(TIMEOUT_MESSAGE);
                }
                else {
                    console.log('not ready, attempt: ' + attempt)

                    setTimeout(function() {
                        dispatch(id, resource, attempt)
                    }
                    , AJAX_SNOOZE);
                }
            }
            else {
                console.log('could not serve request: ' + data['message'])
                handle_timeout(data['message']);
            }
        },
        error: function(o, stat, er) {
            // console.log('ajax.failed: ' + er);
        },
        complete: function(o, stat) {
            // console.log('ajax.complete: ' + stat);
        }
    });
}


/**
    Iterate over profile object and inject into html.
    @param {string} data Object containing artist profile information.
*/
function display_profile(data) {
    'use strict';

    $('#spinner').hide();

    $.each(data, function (key, value) {
        switch(key) {
            case 'tiles':
                // prepare banner images: wrap, resize, append
                $.each(value, function () {

                    // create image, set class, run on load
                    var image = $('<img />', {
                        id: this[0],
                        class: 'tile-image'
                        }).attr('src', this[1]).load(function () {
                        var wrapper = $('<div />', {
                            class: 'tile-wrapper'
                        });

                        wrapper.append(image);
                        $("#image-banner").append(wrapper);
                    });
                });
                break;

            default:
                $("#" + key).html(value).hide().fadeIn(FADE_DELAY);
        }
    });
}


/**
    Iterate over songs object and inject into html.
    @param {string} data Object containing songs information.
*/
function display_songs(data) {
    'use strict';

    // append entire table so we traverse DOM once instead of len(songs) times if we append row by row
    var tb = $('<tbody />');
    $.each(data, function (rank, song) {
        var row;

        if (++rank > 15) {
            return false;
        }

        if (rank % 2 == 0) {
            row = $('<tr>', {class:"row-even"});
        }
        else {
            row = $('<tr>', {class:"row-odd"});
        }

        row.append($('<td>').text(rank));
        row.append($('<td>').text(song['title']));
        row.append($('<td>').text(song['song_hotttnesss']));
        tb.append(row).fadeIn(FADE_DELAY);
    });
    
    $("#song-table").append(tb).fadeIn(FADE_DELAY);
}


/**
    Iterate over similar artists object and inject into html.
    @param {string} data Object containing similar artists information.
*/
function display_similar(data) {
    'use strict'
    var tb = $('<tbody />');

    $.each(data, function (index, artist) {
        if (index > 5) {
            return false;
        }
        var row,
            td_ = $('<td>', {class:"preview-image-width"}), 
            out_div = $('<div>', {class:"preview-container"}), 
            image = $('<img>', {
                class:"preview-image",
                src: artist['preview_url']
            }), 
            in_div = $('<div>', {class:"preview-text"}), 
            span = $('<span>', {class:"preview-terms"}).text(artist['terms']);

        if (++index % 2 == 0) {
            row = $('<tr>', {class:"row-even"});
        }
        else {
            row = $('<tr>', {class:"row-odd"});
        }

        // preview image col
        in_div.append(span);
        out_div.append(image);
        out_div.append(in_div);
        td_.append(out_div);
        row.append(td_);

        // info col
        var info_table_ = $('<table />', {class:"preview-songs-table"}),
            info_tbody_ = $('<tbody>'),
            info_row1 = $('<tr />'),
            info_row2 = $('<tr />');

        info_row1.append($('<th>', {class:"preview-name-title"}).text(artist['name']));

        $.each(artist['songs'], function (nested_index, song) {
            var nested = ($('<tr>'));
            nested.append($('<td>').text(song));
            info_row2.append(nested);
        });
        info_tbody_.append(info_row1);
        info_tbody_.append(info_row2);
        info_table_.append(info_tbody_);
        var temp_td = $('<td>');
        temp_td.append(info_table_);
        row.append(temp_td);

        tb.append(row).fadeIn(FADE_DELAY);
    });
    $("#similar-table").append(tb).fadeIn(FADE_DELAY);
}


/**
    Display error message for failed AJAX retrievals.
    @param {string} message Error message.
*/
function handle_timeout(message) {
    'use strict';

    $('#spinner').hide();
    $("#name").text(message).hide().fadeIn(FADE_DELAY);;
}

