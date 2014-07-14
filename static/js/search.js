/* JSLint */
/* jslint browser: true */
/* global $, jQuery */


/**
    Iterate over artists object and inject into html.
    @param {list} data List of {name, id} containing suggested artist information.
*/
function display_artists(data, rtype) {
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
    
    $("#artist-result-table").append(tb).fadeIn(FADE_DELAY);

    if (data['total_pages'] > 1) {
        var more_url = "/search/?q=" + data['q'] + "&type=artists&page=" + data['current_page'],
        more_link = $('<a>', {href: more_url});
        more_link.append("more");
        $("#artist-view-more").append(more_link).fadeIn(FADE_DELAY);
    }

    display_page_nav(data, rtype);
}


/**
    Iterate over songs object and inject into html.
    @param {list} data List of {title, id} containing searched song information.
*/
function display_songs(data, rtype) {
    'use strict';

    // append entire table so we traverse DOM once instead of len(songs) times if we append row by row
    var tb = $('<tbody />');
    $.each(data[rtype], function (index, song) {
        var row, url, link, temp;

        index += data['offset'];

        if (index % 2 == 0) {
            row = $('<tr>', {class:"row-even"});
        }
        else {
            row = $('<tr>', {class:"row-odd"});
        }

        row.append($('<td>').text(index));
        url = "/song/?q=" + song['id'];
        link = $('<a>', {href: url});
        link.append(song['title']);
        temp = $('<td>');
        temp.append(link);
        row.append(temp);

        tb.append(row).fadeIn(FADE_DELAY);
    });
    
    $("#song-result-table").append(tb).fadeIn(FADE_DELAY);

    if (data['total_pages'] > 1) {
        var more_url = "/search/?q=" + data['q'] + "&type=songs&page=" + data['current_page'],
        more_link = $('<a>', {href: more_url});
        more_link.append("view more");
        $("#song-view-more").append(more_link).fadeIn(FADE_DELAY);
    }

    display_page_nav(data, rtype);
}










