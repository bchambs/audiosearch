//header + search bar height
offset = 295;

function initCanvas(){
	var canvas = document.getElementById('album_matrix'),
	context = canvas.getContext('2d');

	canvas.width = window.innerWidth;

	//set canvas to remainder of screen
	canvas.height = window.innerHeight - offset;

	base_image = new Image();
  	base_image.src = 'http://i.imgur.com/j1APaQ1.png';

  	base_image.css('width', '50');

  	base_image.onload = function(){
    	context.drawImage(base_image, 0, 0);
	}
}