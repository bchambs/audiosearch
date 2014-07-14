/* JSLint */
/* jslint browser: true */
/* global $, jQuery */

    /*
        Load behavior
    */
var AJAX_SNOOZE = 1000,
    ATTEMPT_LIMIT = 10,

    /*
        Display behavior
    */
    FADE_DELAY = 1000,
    ROWS_TO_DISPLAY = 10,
    /*
        Debug
    */
    TIMEOUT_MESSAGE = "Unable to connect to the Echo Nest.",
    JS_DEBUG = true;
    


/**
    Attempt to load deferred Echo Nest requests.
    The artist id and rtype name are used as params to the jQuery AJAX function.
     If requested data is not ready (not in cache), sleep for AJAX_SNOOZE milliseconds.
     Request will timeout after ATTEMPT_LIMIT failed retrievals.
     AJAX calls switch on response status*: 
        On success: switch by rtype value to appropriate display function.
        On error: (pass)
     * This is the status of the AJAX request, not the status value in the returned json.
    @param {string} id Artist hash obtained from query string.
    @param {string} rtype Name of pending request item: profile, songs, or similar
    @param {integer} attempt Count of failed AJAX retrievals.
*/
function dispatch(id, rtype, page, attempt) {
    'use strict';
    if (JS_DEBUG) {
        console.log("dispatching request: ");
        console.log("----for rtype: " + rtype);
        console.log("----using id: " + id);
        if (page) {console.log("----page: " + page)};
    }

    var query = {
        'q': id,
        'rtype': rtype
    };

    if (page) {
        query['page'] = page;
    }

    // TODO: use AJAX fail instead of data['status']
    $.ajax({
        url: "/ajax/",
        data: query,
        dataType: 'json',
        type: 'GET',
        success: function(data, stat, o) {
            if (data['status'] === "ready") {
                if (JS_DEBUG) {console.log("ajax.success: " + stat);}

                switch(rtype) {
                    case 'profile':
                        display_profile(data, rtype);
                        break;

                    case 'artists':
                        display_artists(data, rtype);
                        break;

                    case 'songs':
                        display_songs(data, rtype);
                        break;

                    case 'similar':
                        display_similar(data, rtype);
                        break;
                }
            }
            else if (data['status'] === "pending") {
                attempt++;

                if (attempt > ATTEMPT_LIMIT) {
                    if (JS_DEBUG) {
                        console.log("timeout");
                        console.log(data['message']);
                    }
                    handle_timeout(rtype, data['status']);
                }
                else {
                    if (JS_DEBUG) {console.log("not ready, attempt: " + attempt);}

                    setTimeout(function() {
                        dispatch(id, rtype, page, attempt);
                    }
                    , AJAX_SNOOZE);
                }
            }
            else {
                if (JS_DEBUG) {console.log("could not serve request: " + data['message']);}
                handle_timeout(rtype, data['message']);
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


function display_page_nav(data, rtype) {
    if (data['has_previous']) {
        var prev_url = "?q=" + data['q'] + "&type=" + rtype + "&page=" + data['previous_page_number'],
        prev_link = $('<a>', {href: prev_url});
        prev_link.append("previous");
        $("#previous").append(prev_link).fadeIn(FADE_DELAY);
    }

    $("#current").append("Page " + data['current_page'] + " of " + data['total_pages'] + ".");

    if (data['has_next']) {
        var next_url = "?q=" + data['q'] + "&type=" + rtype + "&page=" + data['next_page_number'],
        next_link = $('<a>', {href: next_url});
        next_link.append("next");
        $("#next").append(next_link).fadeIn(FADE_DELAY);
    }
}


/**
    Display error message for failed AJAX retrievals.
    @param {string} message Error message.
*/
function handle_timeout(resource, message) {
    'use strict';

    $('#spinner').hide();
    $("#name").text(message).hide().fadeIn(FADE_DELAY);;
}
