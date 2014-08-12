/* JSLint */
/* jslint browser: true */
/* global $, jQuery */


function space_to_plus(url) {
    'use strict';

    return url.replace(/ /g,'+');
}


$(".as-form").on('submit', function (event) {
    var q = document.forms["search-form"]["q"].value.trim();

    if (!q) {
        return false;
    }
});


function show_content(content_key) {
    $(".content").hide();
    $("#" + content_key + "-content").show();
}
