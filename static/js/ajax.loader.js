/* JSLint */
/* jslint browser: true */
/* global $, jQuery */

var AJAX_SNOOZE = 1000,
    ATTEMPT_LIMIT = 10,
    FADE_DELAY = 1000;


function dispatch(resource, pending_content, page) {
    'use strict';

    var content_key;

    for (content_key in pending_content) {
        retrieve_content(resource, content_key, 0, page);
    }
}


function load_content(content_key, data) {
    'use strict';

    console.log("in load_content: " + content_key);
}


// remove loader image, display sad face, display error notification
function handle_timeout(content_key, message) {
    'use strict';

    console.log("in handle_timeout: " + content_key);
}


function retrieve_content(resource, content_key, attempt, page) {
    'use strict';

    $.ajax({
        url: "/ajax/retrieval",
        data: {
            'resource': resource,
            'content_key': content_key,
            'page': page
        },
        dataType: 'json',
        type: 'GET',
        success: function(data, stat, o) {
           load_content(content_key, data);
        },
        error: function(o, stat, er) {
            if (attempt > ATTEMPT_LIMIT) {
                handle_timeout(content_key, er);
            }
            else {
                retrieve_content(resource, content_key, ++attempt, page);
            }
        }
        // complete: function(o, stat) {}
    });
}



