//header + search bar height
offset = 295;

function initCanvas(){
	var canvas = document.getElementById('album_matrix'),
	context = canvas.getContext('2d');

	canvas.width = window.innerWidth;

	//set canvas to remainder of screen
	canvas.height = window.innerHeight - offset;

	var sources = [];
	sources[0] = 'http://i.imgur.com/YsrGF9v.jpg';
	sources[1] = 'http://i.imgur.com/javIBwt.gif';
	sources[2] = 'http://i.imgur.com/g2EdwXp.jpg';

    loadImages(sources, function (images) {
        for (var i=0; i < 3; i++) {
            img = new Image();
            img.src = images[i];

            var sourceX = 0 + (200 * i);
            var sourceY = 0;
            var sourceWidth = img.width;
            var sourceHeight = img.height;
            var destWidth = 200;
            var destHeight = 200;
            var destX = 0  + (200 * i);
            var destY = 0;

            console.log(i);
            //context.drawImage (images[1], sourceX, sourceY, sourceWidth, sourceHeight, destX, destY, destWidth, destHeight);
            context.drawImage(images[i], 0 + (200 * i), 0);
        }
    });
}

//credit to html5canvastutorials.com
function loadImages(sources, callback){
    var images = [];
    var loadedImages = 0;
    var numImages = 0;

    for (var src in sources) {
        numImages++;
    }

    for (var src in sources) {
        images[src] = new Image();
        images[src].onload = function() {
            if (++loadedImages >= numImages) {
                callback(images);
            }
        };
        images[src].src = sources[src];
    }
}

function initMatrix() {
    var b_height = "innerHeight" in window 
               ? window.innerHeight
               : document.documentElement.offsetHeight; 
    var b_width = "innerWidth" in window 
               ? window.innerWidth
               : document.documentElement.offsetWidth; 
    var i_dimentions = b_height / 100;
    var table = document.getElementById("album_matrix");


    for (var i=0; i < b_height; i += 200){ 
        var tr = document.createElement("tr");

        for (var j=0; j < b_width; j += 110) {
            var td = document.createElement("td");
            td.innerHTML = "<img src=\"http://i.imgur.com/YsrGF9v.jpg\" class=\"cell_img\">";
            //td.innerHTML += "<img src=\"static/img/cell_fill.png\" class=\"cell_img\">";
            tr.appendChild(td);
        }

        table.appendChild(tr);
    }
}