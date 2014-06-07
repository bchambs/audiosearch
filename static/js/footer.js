$(function() {
    'use strict';
    var x = 0;
    setInterval(function () {
        x -= 1;
        $('.wave-far').css('background-position', x + 'px 0');
    }, 10);
})