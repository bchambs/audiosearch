var long_bio_js;
var short_bio_js;
var short_bio = true;
var bio_el = document.getElementById('bio-toggle');
bio_el.addEventListener("click", function() {
	toggle_bio();
});



function init_bio (lbq, sbq) {
	long_bio_js = lbq;
	short_bio_js = sbq;
}




/* 
	url = url for the artist image

	check width and height for image. if dominate element is too large resize to our limit
*/
function resize_image(url) {

	$('#artist-image').attr('src',url).load(function() {	// it may be better to access the image url instead of waiting for page to load
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
	})
}




/*
	toggle to display short and long artist biography.  update toggle text.
*/
function toggle_bio() {
	var text = document.getElementById ("bio-block");

	if (short_bio) {
		short_bio = !short_bio;
	}
	else {
		short_bio = !short_bio;
	}
}