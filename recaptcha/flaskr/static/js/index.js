const deviceWidth = window.innerWidth;
const deviceHeight = window.innerHeight;
let squares = document.getElementById("imgs").children
let bricks = document.getElementById("blocks").children

let captchaBox = [];
let collisonBox = [];
let path = [];
const ball = document.querySelector("#ball");
const gameContainer = document.querySelector("#gameContainer");
let accx = 0;
let accy = 0;
let accz = 0;
const squareSize = 20;
const tlimit = 1;
let brickWidth = 70;
let brickHeight = 70;
let margin = 10;
let time = 0
// let squares = document.getElementById("imgs").children
// let captchaBox = []
// let captchaDone = false
let captchaid = 0
let inSquare = [false, false, false, false]

if ('Accelerometer' in window) {

	let gy = new Gyroscope({ frequency: 60 });
	const acc = new Accelerometer({ frequency: 60 });
	console.log('Accelerometer and Gyroscope supported');

	acc.start();
	let ae = acc.addEventListener('reading', async function moveBall(e) {

		accx = acc.x;
		accy = acc.y;

		let ballLeft = ball.offsetLeft - accx * 5;
		let ballTop = ball.offsetTop + accy * 5;
		console.log(ballLeft, ballTop)
		console.log(gameContainer.offsetWidth)
		let f = false;
		// collision with container handling
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
		//collision handling with bricks
		for (var i = 0; i < 4; i++) {
			b = bricks[i]

			ballTop = ball.offsetTop;
			if (ballLeft + ball.offsetWidth > b.offsetLeft && ballLeft < b.offsetLeft + brickWidth &&
				ballTop + ball.offsetHeight > b.offsetTop && ballTop < b.offsetTop + brickHeight) {
				// console.log(b);
				ballLeft = ball.offsetLeft + acc.x;
				ball.style.left = ballLeft + "px";
				f = true;
				break;

			}
			ballTop = ball.offsetTop + accy * 5;
			ballLeft = ball.offsetLeft;
			if (ballLeft + ball.offsetWidth > b.offsetLeft && ballLeft < b.offsetLeft + brickWidth &&
				ballTop + ball.offsetHeight > b.offsetTop && ballTop < b.offsetTop + brickHeight) {
				ballTop = ball.offsetTop - acc.y;
				ball.style.top = ballTop + "px";
				f = true;
				break;

			}
			ballLeft = ball.offsetLeft - accx * 5;
		}
		if (!f) {
			ball.style.left = ballLeft + "px";
			ball.style.top = ballTop + "px";
			// console.log("ball left top", ballLeft, ballTop)
		}

	});
} else {
	console.error('Accelerometer or Gryroscope not supported');
}

function responseHandler(data) {
	console.log(data);
	if (data['bool'] == "true") {

		alert("Captcha passed")
		// clearInterval(captchaid)
		ball.style.left = 150;
		ball.offsetTop = 150;
		captchaid = setInterval(checkSquare, 6);
		window.location.href = "https://www.google.com"
	}

	else {
		// alert("Captcha failed, try again")
		// if (confirm("Captcha failed, try again")) {
		// clearInterval(captchaid)
		// location.reload();
		// }
		ball.style.left = 150;
		ball.offsetTop = 150;
		captchaid = setInterval(checkSquare, 6);
	}


}

function checkSquare() {
	let square;
	let margin = squareSize;
	for (let i = 0; i < 4; i++) {
		let bool = ((ball.offsetLeft < captchaBox[i].right) && (ball.offsetLeft > captchaBox[i].left) && (ball.offsetTop < captchaBox[i].bottom) && (ball.offsetTop > captchaBox[i].top));
		if (inSquare[i] == true) {
			console.log("hit", i)
			if (bool) {
				time += 1;
			}
			else {
				time = 0;
				inSquare[i] = false;
			}


			if (time > tlimit) {
				console.log("PASSED TIME LIMIT")
				const requestOptions = {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({
						guess: i,
						path: path
					})
				};
				fetch("guess", requestOptions)
					.then(response => response.json())
					.then(data => responseHandler(data))
					.catch(error => console.error('Error:', error));
				console.log(i, captchaBox[i]);
				console.log(ball);
				clearInterval(captchaid);

			}

		}
		else if (bool) {
			inSquare[i] = true
			console.log("box ", i);
			time = 0
		}


	}
}

box_pos = JSON.parse('{{ box_pos | tojson }}');
obs_pos = JSON.parse('{{ obs_pos | tojson }}');
for (let i = 0; i < 4; i++) {

	let square = squares[i];
	// square.style.width = squareSize + "px";
	// square.style.height = squareSize + "px";
	square.style.position = "absolute";
	square.style.left = (box_pos[i][0]) - JSON.parse('{{ offset }}') + "px";
	square.style.top = (box_pos[i][1]) - - JSON.parse('{{ offset }}') + "px";
	// square.style.left = (box_pos[i][0] * (gameContainer. - 2 * squareSize)) + "px";
	// square.style.top = (box_pos[i][1] * (gameContainer.offsetHeight - 2 * squareSize)) + "px";
	let areaBox = {
		'left': (parseInt(square.style.left.replace(/px/, "")) - margin),
		'right': (parseInt(square.style.left.replace(/px/, "")) + squareSize + margin),
		'top': (parseInt(square.style.top.replace(/px/, "")) - margin),
		'bottom': (parseInt(square.style.top.replace(/px/, "")) + squareSize + margin)
	}
	console.log(square);
	captchaBox.push(areaBox)
}
let brickSize = 70;
for (let i = 0; i < 4; i++) {
	let b = bricks[i]

	b.style.position = "absolute";
	b.style.left = (obs_pos[i][0]) - JSON.parse('{{ offset }}') + "px";
	b.style.top = (obs_pos[i][1]) - JSON.parse('{{ offset }}') + "px";

	let brickBox = {
		'left': (parseInt(b.style.left.replace(/px/, ""))) + "px",
		'right': (parseInt(b.style.left.replace(/px/, "")) + brickSize) + "px",
		'top': (parseInt(b.style.top.replace(/px/, ""))) + "px",
		'bottom': (parseInt(b.style.top.replace(/px/, "")) + brickSize) + "px"
	}
	collisonBox.push(brickBox);
}
console.log(bricks)
captchaid = setInterval(checkSquare, 3);
setTimeout(function () {
	location.reload();
}, 100000);
setInterval(function () {
	path.push([(parseFloat(ball.style.left.replace(/px/, ""))), (parseFloat(ball.style.top.replace(/px/, "")))])
}, 62)