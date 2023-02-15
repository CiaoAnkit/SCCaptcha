const ball = document.querySelector("#ball");
const gameContainer = document.querySelector("#gameContainer");

let accx = 0;
let accy = 0;
const squareSize = 20;
const tlimit = 2;
let time = 0
let squares = document.getElementById("imgs").children
let inSquare = [true, true, true, true]

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
		// console.log(i, squares[i].style.left, ball.style)
		// console.log(inSquare)
		if (inSquare[i] == true) {
			square = squares[i]
			// console.log(i)
			if ((ball.style.left < square.style.left + margin) && (ball.style.left > square.style.left - margin)) {
				if ((ball.style.top < square.style.top + margin) && (ball.style.top > square.style.top - margin)) {
					time += 1;
					alert("Captcha passed")
					console.log(time)
				}
				else {
					time = 0;
				}
			}
			else {
				time = 0;
			}

			if (time > tlimit) {
				if (i == 1)
					alert("Captcha passed")
				else alert("Captcha failed, try again")
			}
		}
		else if ((ball.style.left < squares[i].style.left + margin) && (ball.style.left > squares[i].style.left - margin)) {
			if ((ball.style.top < squares[i].style.top + margin) && (ball.style.top > squares[i].style.top - margin)) {
				inSquare[i] = true
			}
		}

	}
}
setInterval(checkSquare, 16);



//place rotated images
for (let i = 0; i < 4; i++) {
	let square = squares[i];
	// square.style.width = squareSize + "px";
	// square.style.height = squareSize + "px";
	square.style.position = "absolute";
	square.style.left = Math.floor(Math.random() * (gameContainer.offsetWidth - squareSize)) + "px";
	square.style.top = Math.floor(Math.random() * (gameContainer.offsetHeight - squareSize)) + "px";
}
