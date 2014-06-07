/* JSLint */
/*jslint browser: true*/
/*global $, jQuery, toggle_bio*/

var short_bio = true;

/*
    toggle to display short and long artist biography.  update toggle text. 
*/
$('#bio-toggle').on('click', function () {
    'use strict';
    if (short_bio) {
        $('short-bio-block').style.display = 'none';
        $('long-bio-block').style.display = 'inline';
        $('bio-toggle').innerHTML = 'less';

        short_bio = !short_bio;
    } else {
        $('long-bio-block').style.display = 'none';
        $('short-bio-block').style.display = 'inline';
        $('bio-toggle').innerHTML = 'more';

        short_bio = !short_bio;
    }
});


/* 
    check width and height for image. if dominate element is too large resize to our limit
*/
$('#artist-image').load(function () {
    'use strict';
    var dim_limit = 300;
    
    // find dominate dimension and resize if too large
    if (this.width > this.height) {
        if (this.width > dim_limit) {
            this.width = dim_limit;
        }
    } else if (this.height > dim_limit) {
        this.height = dim_limit;
    }
});
