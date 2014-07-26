/* JSLint */
/* jslint browser: true */
/* global $, jQuery */


function remove_resource(id) {
    'use strict';
    
    $.ajax({
        url: "/ajax/clear/",
        data: {id: id},
        dataType: 'json',
        type: 'GET'
    });
};


function debug_template() {
    'use strict';
    
    $.ajax({
        url: "/ajax/debug_template/",
        dataType: 'json',
        type: 'GET'
    });
}
