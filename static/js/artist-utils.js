/* JSLint */
/* jslint browser: true */
/* global $, jQuery */

var TIMEOUT_MESSAGE = 'Unable to connect to the Echo Nest.',
    AJAX_SNOOZE = 1000,
    FADE_DELAY = 1000,
    ATTEMPT_LIMIT = 5;

/*
    data = async music data from initial request.

    fill the page with request data.
*/
function display_results(data) {
    'use strict';

    $('#spinner').hide();

    $.each(data, function (key, value) {
        if (key === 'title-image') {
            $("#" + key).attr("src", value).hide().fadeIn(FADE_DELAY);;
        }
        else if (key === 'songs') {
            $.each(value, function (rank, song) {
                $("#" + key).append(rank + 1 + '. ' + song['title']);
                $("#" + key).append("<p />").hide().fadeIn(FADE_DELAY);
            });
        }
        else {
            $("#" + key).html(value).hide().fadeIn(FADE_DELAY);
        }
    });
}


function handle_timeout(message) {
    'use strict';

    $('#spinner').hide();
    $("#name").text(message).hide().fadeIn(FADE_DELAY);;
}


/*
    id = artist / song id used to query data from redis cache.

    if user request was not served, run async call to retrieve music data.
*/
function fetch_request(id, attempt) {
    'use strict';

    $.ajax({
        url: '/ajax/',
        data: {'q': id},
        dataType: 'json',
        type: 'GET',
        success: function(data, stat, o) {
            if (data['status'] === 'ready') {
                console.log('ajax.success: ' + stat)

                display_results(data);
            }
            else if (data['status'] === 'pending') {
                attempt += 1;

                if (attempt > ATTEMPT_LIMIT) {
                    console.log('timeout')
                    handle_timeout(TIMEOUT_MESSAGE);
                }
                else {
                    console.log('not ready, attempt: ' + attempt)

                    setTimeout(function() {
                        fetch_request(id, attempt)
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

/*
    retrieve query string param 'q'.
*/
function fetch_query_string() {
    'use strict';

    var query = window.location.search.split("="),
        regex = /^[a-z0-9]+$/i;

    // check for alphanumeric
    if (query.length === 2) {
        if (regex.test(query[1])) {
            return query[1];
        }
    }

    return '';
}
