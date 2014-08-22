/* JSLint */
/* jslint browser: true */
/* global $, jQuery */


function remove_resource(resource_id) {
    'use strict';

    $.ajax({
        url: "/ajax/clear/",
        data: {
            resource_id: resource_id,
        },
        dataType: 'json',
        type: 'GET'
    });
};



