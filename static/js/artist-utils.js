/* JSLint */
/* jslint browser: true */
/* global $, jQuery */

/*
    data = async music data from initial request.

    fill the page with request data.
*/
function display_results(data) {
    'use strict';

    console.log('displaying');

    $.each(data, function (key, value) {
        $("#" + key).html(value).hide().fadeIn(1000);
    });
}


function handle_timeout() {
    $("#name").text(":(").hide().fadeIn(1000);;
}


/*
    id = artist / song id used to query data from redis cache.

    if user request was not served, run async call to retrieve music data.
*/
function fetch_request(id, timeout) {
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
                $('#spinner').hide();
            }
            else if (data['status'] === 'retry') {
                timeout += 1;

                if (timeout > 5) {
                    console.log('timeout')
                    $('#spinner').hide();
                    handle_timeout();
                }
                else {
                    console.log('not ready, attempt: ' + timeout)

                    setTimeout(function() {
                        fetch_request(id, timeout)
                    }
                    , 1000);
                }
            }
        },
        error: function(o, stat, er) {
            console.log('ajax.failed: ' + er);
        },
        complete: function(o, stat) {
            console.log('ajax.complete: ' + stat);
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
