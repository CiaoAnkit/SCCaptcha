const ball = document.querySelector("#ball");
const gameContainer = document.querySelector("#gameContainer");

let accx = 0;
let accy = 0;
const squareSize = 20;
const tlimit = 20;
let margin = 10;
let time = 0
let squares = document.getElementById("imgs").children
let captchaBox = []
// let captchaDone = false
let captchaid = 0
let inSquare = [false, false,false,false]

if ('Accelerometer' in window) {
	const acc = new Accelerometer({ frequency: 60 });
	acc.start();
	acc.addEventListener('reading', async function moveBall(e) {
		accx = acc.x;
		accy = acc.y;
		// console.log(x, y)
		let ballLeft = ball.offsetLeft - accx * 5;
		let ballTop = ball.offsetTop + accy * 5;
		let f = false;
		if (ballLeft <= 0 || ballLeft + ball.offsetWidth >= gameContainer.offsetWidth) {
			if ((ballTop <= 0 || ballTop + ball.offsetHeight >= gameContainer.offsetHeight) && !f) {
				return;
			}
			ball.style.top = ballTop + "px";
			f = true;

		}
		else if ((ballTop <= 0 || ballTop + ball.offsetHeight >= gameContainer.offsetHeight) && !f) {
			if (ballLeft <= 0 || ballLeft + ball.offsetWidth >= gameContainer.offsetWidth) {
				return;
			}
			ball.style.left = ballLeft + "px";
			f = true;
		}

		if (!f) {
			ball.style.left = ballLeft + "px";
			ball.style.top = ballTop + "px";
		}
	});
} else {
	console.error('Accelerometer not supported');
}


function checkSquare() {
	let square;
	let margin = squareSize;
	for (let i = 0; i < 4; i++) {
		if (inSquare[i] == true) {
			// console.log(i)
			if ((ball.style.left < captchaBox[i].right) && (ball.style.left > captchaBox[i].left)) {
				if ((ball.style.top < captchaBox[i].bottom) && (ball.style.top > captchaBox[i].top)) {
					time += 1;
				}
				else {
					time = 0;
					inSquare[i] = false;
				}
			}
			else {
				time = 0;
				inSquare[i] = false;
			}

			if (time > tlimit) {
				if (i == 0){
					alert("Captcha passed")
					clearInterval(captchaid)
					location.href = "https://iiit.ac.in"
				}
				else{
					// alert("Captcha failed, try again")
					if(confirm("Captcha failed, try again")) {
						clearInterval(captchaid)
						location.reload();
					}
				}
			}
		}
		else if ((ball.style.left < captchaBox[i].right) && (ball.style.left > captchaBox[i].left)) {
			if ((ball.style.top < captchaBox[i].bottom) && (ball.style.top > captchaBox[i].top)) {
				inSquare[i] = true
				time=0
			}
		}

	}
}



//place rotated images
for (let i = 0; i < 4; i++) {
	let square = squares[i];
	// square.style.width = squareSize + "px";
	// square.style.height = squareSize + "px";
	square.style.position = "absolute";
	square.style.left = Math.floor(Math.random() * (gameContainer.offsetWidth - 2*squareSize)) + "px";
	square.style.top = Math.floor(Math.random() * (gameContainer.offsetHeight - 2*squareSize)) + "px";
	let areaBox = {
		'left': (parseInt(square.style.left.replace(/px/,""))-margin)+"px",
		'right': (parseInt(square.style.left.replace(/px/,""))+squareSize+margin)+"px",
		'top': (parseInt(square.style.top.replace(/px/,""))-margin)+"px",
		'bottom': (parseInt(square.style.top.replace(/px/,""))+squareSize+margin)+"px"
	}
	console.log(areaBox)
	captchaBox.push(areaBox)
}

captchaid = setInterval(checkSquare, 16);
setTimeout(function() {
	location.reload();
}, 10000);
