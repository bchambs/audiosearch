/* JSLint */
/* jslint browser: true */
/* global $, jQuery */

function space_to_plus(url) {
    'use strict';

    return url.replace(/ /g,'+');
}


function show_content(content_key) {
    $(".content").hide();
    $("#" + content_key + "-content").show();
}
