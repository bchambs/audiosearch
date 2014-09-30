/* JSLint */
/* jslint browser: true */
/* global $, jQuery */
'use strict';


var AJAX_SNOOZE = 2000,             // Time in ms between failed AJAX requests.
    AJAX_INITIAL_SNOOZE = 1500,     // Initial delay in ms before beginning AJAX requests.
    AJAX_SLOW_THRESHOLD = 6,        // Number of failed attempts before displaying 'slow results' message.
    AJAX_FAIL_THRESHOLD = 5,       // Number of failed attempts before displaying 'failed' message and halting AJAX requests.
    FADEIN = 700;   // Milliseconds.


function dispatch(url, id, attempt) {
    console.log('dispatching... ' + attempt);
    $.get(url, function(context) {
        if (context['status'] === 'complete') {
            var $table = '#' + id + '-table';
            $(template_id + '-spinner').hide();
            $($table).append(context['template']).hide().fadeIn(FADEIN);
            console.log("loaded");
        }
        else if (context['status'] === 'pending' && attempt < AJAX_FAIL_THRESHOLD) {
            setTimeout(function() {
                dispatch(url, template_id, ++attempt);
            }, AJAX_SNOOZE);
        }
        else {
            console.log('failed');
        }
    });
}
