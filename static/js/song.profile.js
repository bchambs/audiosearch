/* JSLint */
/* jslint browser: true */
/* global $, jQuery */


/**
    Iterate over profile object and inject into html.
    @param {object} data Object containing artist profile information.
*/
function display_profile(data, rtype) {
    'use strict';

    $.each(data[rtype], function (key, value) {
        console.log(key + " : " + value);

        switch(key) {
            case 'audio_summary':
                $.each(value, function (key, value) {
                    console.log("\t" + key + " : " + value);
                });
                console.log(key + " : " + value);

                break;

            default:
                
        }
    });

    console.log("out of js");
}




