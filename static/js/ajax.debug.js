/* JSLint */
/* jslint browser: true */
/* global $, jQuery */


function remove_resource(resource_id) {
    'use strict';

    $.ajax({
        url: "/ajax/clear/",
        data: {
            resource_id: resource_id,
            'content_key': "debug"
        },
        dataType: 'json',
        type: 'GET'
    });
};



