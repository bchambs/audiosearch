/* JSLint */
/* jslint browser: true */
/* global $, jQuery */


/**
    Iterate over artists object and inject into html.
    @param {list} data List of {name, id} containing suggested artist information.
*/
function display_similar(data, rtype) {
    'use strict';

    // append entire table so we traverse DOM once instead of len(songs) times if we append row by row
    var tb = $('<tbody />');
    $.each(data[rtype], function (index, artist) {
        var row, url, link, temp;

        index += data['offset'];

        if (index % 2 == 0) {
            row = $('<tr>', {class:"row-even"});
        }
        else {
            row = $('<tr>', {class:"row-odd"});
        }

        row.append($('<td>').text(index));
        url = "/artist/?q=" + artist['id'];
        link = $('<a>', {href: url});
        link.append(artist['name']);
        temp = $('<td>');
        temp.append(link);
        row.append(temp);

        tb.append(row).fadeIn(FADE_DELAY);
    });
    
    $("#similar-result-table").append(tb).fadeIn(FADE_DELAY);

    // display_page_nav(data, rtype);
    if (data['has_previous']) {
        var prev_url = "?q=" + data['q'] + "&page=" + data['previous_page_number'],
        prev_link = $('<a>', {href: prev_url});
        prev_link.append("previous");
        $("#previous").append(prev_link).fadeIn(FADE_DELAY);
    }

    $("#current").append("Page " + data['current_page'] + " of " + data['total_pages'] + ".");

    if (data['has_next']) {
        var next_url = "?q=" + data['q'] + "&page=" + data['next_page_number'],
        next_link = $('<a>', {href: next_url});
        next_link.append("next");
        $("#next").append(next_link).fadeIn(FADE_DELAY);
    }
}





