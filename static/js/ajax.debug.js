/* JSLint */
/* jslint browser: true */
/* global $, jQuery */


function remove_resource(resource) {
    'use strict';

    $.ajax({
        url: "/ajax/clear/",
        data: {
            resource: resource,
        },
        dataType: 'json',
        type: 'GET'
    });
};



