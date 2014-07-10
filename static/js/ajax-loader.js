/* JSLint */
/* jslint browser: true */
/* global $, jQuery */


var TIMEOUT_MESSAGE = 'Unable to connect to the Echo Nest.',
    AJAX_SNOOZE = 1000,
    ATTEMPT_LIMIT = 10,
    FADE_DELAY = 1000,
    JS_DEBUG = true;


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
    if (JS_DEBUG) {
        console.log("dispatching request for: " + resource);
        console.log("\t using id: " + id);
    }

    // TODO: use AJAX fail instead of data['status']
    $.ajax({
        url: '/ajax/',
        data: {
            'q': id,
            'resource': resource
        },
        dataType: 'json',
        type: 'GET',
        success: function(data, stat, o) {
            if (data['status'] === 'ready') {
                if (JS_DEBUG) {console.log('ajax.success: ' + stat);}

                switch(resource) {
                    case 'profile':
                        display_profile(data[resource]);
                        break;

                    case 'artists':
                        display_artists(data[resource]);
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
                    if (JS_DEBUG) {console.log('timeout');}
                    handle_timeout(TIMEOUT_MESSAGE);
                }
                else {
                    if (JS_DEBUG) {console.log('not ready, attempt: ' + attempt);}

                    setTimeout(function() {
                        dispatch(id, resource, attempt)
                    }
                    , AJAX_SNOOZE);
                }
            }
            else {
                if (JS_DEBUG) {console.log('could not serve request: ' + data['message']);}
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
    Display error message for failed AJAX retrievals.
    @param {string} message Error message.
*/
function handle_timeout(message) {
    'use strict';

    $('#spinner').hide();
    $("#name").text(message).hide().fadeIn(FADE_DELAY);;
}
