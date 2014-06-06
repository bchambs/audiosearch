/* JSLint */
/*jslint browser: true*/
/*global $, jQuery, toggle_bio*/

var long_bio_js;
var short_bio_js;
var short_bio = true;
var bio_el = document.getElementById('bio-toggle');
bio_el.addEventListener('click', function () {
    'use strict';
    toggle_bio();
});


/*
    lbq = long bio escaped and surrounded by quotes
    sbq = short bio escaped and surrounded by quotes

    establish bio vars for toggle_bio()
*/
function init_bio(lbq, sbq) {
    'use strict';
    long_bio_js = lbq;
    short_bio_js = sbq;
}




/* 
    url = url for the artist image

    check width and height for image. if dominate element is too large resize to our limit
*/
function resize_image(url) {
    'use strict';

    $('#artist-image').attr('src', url).load(function () {    // it may be better to access the image url instead of waiting for page to load
        var dim_limit = 300;
        
        // find dominate dimension and resize if too large
        if (this.width > this.height) {
            if (this.width > dim_limit) {
                this.width = dim_limit;
            }
        } 
        else if (this.height > dim_limit) {
            this.height = dim_limit;
        }
    });
}




/*
    toggle to display short and long artist biography.  update toggle text. 
*/
function toggle_bio() {
    'use strict';

    var short_block = document.getElementById('short-bio-block'),
        long_block = document.getElementById('long-bio-block'),
        link_text = document.getElementById('bio-toggle');

    if (short_bio) {
        short_block.style.display = 'none';
        long_block.style.display = 'block';
        link_text.innerHTML = 'less';

        short_bio = !short_bio;
    }
    else {
        long_block.style.display = 'none';
        short_block.style.display = 'block';
        link_text.innerHTML = 'more';

        short_bio = !short_bio;
    }
}
