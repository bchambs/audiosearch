/* JSLint */
/* jslint browser: true */
/* global $, jQuery */


function remove_resource(resource) {
    'use strict';

    $.ajax({
        url: "/ajax/clear/",
        data: {
            key: rkey,
        },
        dataType: 'json',
        type: 'GET'
    });
};



