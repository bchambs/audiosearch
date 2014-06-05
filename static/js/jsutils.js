/* 
	url = url for the artist image

	check width and height for image. if dominate element is too large resize to our limit
*/
function resize_image(url) {

	$('#artist-image').attr('src',url).load(function() {	// it may be better to access the image url instead of waiting for page to load
		var dim_limit = 300;
		var size = {
			w:this.width,
			h:this.height
		}
		
		// find dominate dimension and resize if too large
		if (size.w > size.h) {
			if (size.w > dim_limit) {
				this.width = dim_limit;
			}
		}
		else if (size.h > dim_limit) {
			this.height = dim_limit;
		}
	})
}
