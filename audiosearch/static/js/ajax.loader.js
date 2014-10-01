/* JSLint */
/* jslint browser: true */
/* global $, jQuery */
'use strict';


var AJAX_SNOOZE = 2000,             // Time in ms between failed AJAX requests.
    AJAX_INITIAL_SNOOZE = 1500,     // Initial delay in ms before beginning AJAX requests.
    AJAX_SLOW_THRESHOLD = 6,        // Number of failed attempts before displaying 'slow results' message.
    AJAX_FAIL_THRESHOLD = 5,       // Number of failed attempts before displaying 'failed' message and halting AJAX requests.
    FADEIN = 700;   // Milliseconds.


function dispatch(opts) {
    var id = opts.id,
        url = opts.url,
        data = opts.data,
        attempt = (opts.attempt || 1);

    console.log('dispatching... ' + attempt);

    $.get(url, data, function(context) {
        if (context['status'] === 'complete') {

            var $spinner = '#' + id + '-spinner',
                $table = '#' + id + '-table';

            $($spinner).hide();
            $($table).append(context['template']).hide().fadeIn(FADEIN);
            
            console.log(id);
            console.log($table);
            console.log("loaded");
            console.log(context['template']);


        }
        else if (context['status'] === 'pending' && attempt < AJAX_FAIL_THRESHOLD) {
            opts.attempt = ++attempt;

            setTimeout(function() {dispatch(opts);}, AJAX_SNOOZE);
        }
        else {
            console.log('failed');
        }
    });
}
