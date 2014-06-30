/* JSLint */
/* jslint browser: true */
/* global $, jQuery */
// TODO: move all 'use strict' to top of files

var TIMEOUT_MESSAGE = 'Unable to connect to the Echo Nest.',
    AJAX_SNOOZE = 1000,
    FADE_DELAY = 1000,
    ATTEMPT_LIMIT = 5,
    BANNER_HEIGHT = $(".image-banner").height;

/*
    event handlers
*/


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


/*
    id = artist / song id used to query data from redis cache.

    if user request was not served, run async call to retrieve music data.
*/
function fetch_request(id, attempt) {
    'use strict';

    $.ajax({
        url: '/artistjx/',
        data: {'q': id},
        dataType: 'json',
        type: 'GET',
        success: function(data, stat, o) {
            if (data['status'] === 'ready') {
                console.log('ajax.success: ' + stat)

                display_results(data);
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
    data = async music data from initial request.

    fill the page with request data.
*/
function display_results(data) {
    'use strict';

    $('#spinner').hide();

    // iterate over JSON and load data to divs
    $.each(data, function (key, value) {
        switch (key) {
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

            case 'songs':
                // append entire table so we traverse DOM once instead of len(songs) times if we append row by row
                var tb = $('<tbody />');
                $.each(value, function (rank, song) {
                    var row;
                    rank++;

                    if (rank > 15) {
                        return false;
                    }

                    if (rank % 2 == 0) {
                        row = $('<tr>', {id: 'hehe', class:"row-even"});
                    }
                    else {
                        row = $('<tr>', {id: 'hehe', class:"row-odd"});
                    }

                    row.append($('<td>').text(rank));
                    row.append($('<td>').text(song['title']));
                    row.append($('<td>').text(song['song_hotttnesss']));
                    tb.append(row).fadeIn(FADE_DELAY);
                });
                $("#song-table").append(tb).fadeIn(FADE_DELAY);
                break;

            default:
                $("#" + key).html(value).hide().fadeIn(FADE_DELAY);
                // console.log(key + ': ' + value);
        }
    });
}


function handle_timeout(message) {
    'use strict';

    $('#spinner').hide();
    $("#name").text(message).hide().fadeIn(FADE_DELAY);;
}
