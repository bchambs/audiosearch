/* JSLint */
/*jslint browser: true*/
/*global $, jQuery*/

/*
    data = async music data from initial request.

    fill the page with request data.
*/
function display_results(data) {
    'use strict';

    $.each(data, function (i) {
        // alert (data[i]);
    });
}


/*
    id = artist / song id used to query data from Async_Map.

    if user request was not served, run async call to retrieve music data.
*/
function fetch_request(id) {
    'use strict';

    $.ajax({
        url: '/ajx/',
        data: {'id': id},
        dataType: 'json',
        type: 'GET',
        success: function(data) {
            display_results(data);
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
