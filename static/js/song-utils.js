/* JSLint */
/* jslint browser: true */
/* global $, jQuery */


/**
    Iterate over artists object and inject into html.
    @param {list} data List of {name, id} containing suggested artist information.
*/
function display_artists(data) {
    'use strict';

    // $('#spinner').hide();

    $.each(data, function (key, value) {
        switch(key) {
            case 'tiles':
                // prepare banner images: wrap, resize, append
                $.each(value, function () {

                    // create image, set class, run on load
                    var image = $('<img />', {
                        id: this[0],
                        class: 'tile-image'
                        }).attr('src', this[1]).load(function () {
                        var wrapper = $('<div />', {
                            class: 'tile-wrapper'
                        });

                        wrapper.append(image);
                        $("#image-banner").append(wrapper);
                    });
                });
                break;

            default:
                $("#" + key).html(value).hide().fadeIn(FADE_DELAY);
        }
    });
}




