const boardElement = document.getElementById("game-board");
const scoreElement = document.getElementById("score");
const bestScoreElement = document.getElementById("best-score");
const newGameButton = document.getElementById("new-game-button");

const leaderboardElement =
    document.getElementById("leaderboard-list");


let board = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
];

let score = 0;
let winAnnounced = false;


// Add a new 2 or 4 tile
function addTile() {
    const emptyCells = [];

    for (let row = 0; row < 4; row++) {
        for (let column = 0; column < 4; column++) {

            if (board[row][column] === 0) {
                emptyCells.push([row, column]);
            }
        }
    }

    if (emptyCells.length > 0) {

        const randomIndex = Math.floor(
            Math.random() * emptyCells.length
        );

        const [row, column] = emptyCells[randomIndex];

        board[row][column] =
            Math.random() < 0.1 ? 4 : 2;
    }
}


// Merge one row toward the left
function mergeRowLeft(row) {

    const numbers = row.filter(
        number => number !== 0
    );

    const merged = [];

    let i = 0;

    while (i < numbers.length) {

        if (
            i + 1 < numbers.length &&
            numbers[i] === numbers[i + 1]
        ) {

            const newValue = numbers[i] * 2;

            merged.push(newValue);

            score += newValue;

            i += 2;

        } else {

            merged.push(numbers[i]);

            i += 1;
        }
    }

    while (merged.length < 4) {
        merged.push(0);
    }

    return merged;
}


// Move left
function moveLeft() {

    for (let row = 0; row < 4; row++) {
        board[row] = mergeRowLeft(board[row]);
    }
}


// Move right
function moveRight() {

    for (let row = 0; row < 4; row++) {

        const reversedRow =
            [...board[row]].reverse();

        const mergedRow =
            mergeRowLeft(reversedRow);

        board[row] =
            mergedRow.reverse();
    }
}


// Move up
function moveUp() {

    for (let column = 0; column < 4; column++) {

        const values = [];

        for (let row = 0; row < 4; row++) {
            values.push(board[row][column]);
        }

        const merged = mergeRowLeft(values);

        for (let row = 0; row < 4; row++) {
            board[row][column] = merged[row];
        }
    }
}


// Move down
function moveDown() {

    for (let column = 0; column < 4; column++) {

        const values = [];

        for (let row = 0; row < 4; row++) {
            values.push(board[row][column]);
        }

        values.reverse();

        const merged = mergeRowLeft(values);

        merged.reverse();

        for (let row = 0; row < 4; row++) {
            board[row][column] = merged[row];
        }
    }
}


// Check whether two boards are different
function boardsAreDifferent(oldBoard) {

    for (let row = 0; row < 4; row++) {

        for (let column = 0; column < 4; column++) {

            if (
                oldBoard[row][column] !==
                board[row][column]
            ) {
                return true;
            }
        }
    }

    return false;
}

// Check whether the player has reached 2048
function hasWon() {

    for (let row = 0; row < 4; row++) {

        for (let column = 0; column < 4; column++) {

            if (board[row][column] === 2048) {
                return true;
            }
        }
    }

    return false;
}

// Check whether there are any moves remaining
function gameOver() {

    // Check for empty cells
    for (let row = 0; row < 4; row++) {

        for (let column = 0; column < 4; column++) {

            if (board[row][column] === 0) {
                return false;
            }
        }
    }

    // Check horizontal neighbours
    for (let row = 0; row < 4; row++) {

        for (let column = 0; column < 3; column++) {

            if (
                board[row][column] ===
                board[row][column + 1]
            ) {
                return false;
            }
        }
    }

    // Check vertical neighbours
    for (let row = 0; row < 3; row++) {

        for (let column = 0; column < 4; column++) {

            if (
                board[row][column] ===
                board[row + 1][column]
            ) {
                return false;
            }
        }
    }

    return true;
}


// Handle a move
function move(direction) {

    const oldBoard = board.map(
        row => [...row]
    );

    if (direction === "left") {
        moveLeft();

    } else if (direction === "right") {
        moveRight();

    } else if (direction === "up") {
        moveUp();

    } else if (direction === "down") {
        moveDown();
    }

    if (boardsAreDifferent(oldBoard)) {
        addTile();
        updateDisplay();

        // Check for 2048
        if (hasWon() && !winAnnounced) {

            winAnnounced = true;

            const startAgain = confirm(
                `You reached 2048!\n\n` +
                `Score: ${score}\n\n` +
                `Start a new game?\n\n` +
                `Press Cancel to continue playing.`
            );

            if (startAgain) {
                newGame(false);
                return;
            }
        }

    } else {
        updateDisplay();
    }

    // Check game over even if the attempted move
    // did not change the board
    if (gameOver()) {

        checkHighScore();

        const startAgain = confirm(
            `Game Over!\n\n` +
            `Final Score: ${score}\n\n` +
            `Start a new game?`
        );

        if (startAgain) {
            newGame(false);
        }
    }
}


// Draw the board
function updateDisplay() {

    boardElement.innerHTML = "";

    for (let row = 0; row < 4; row++) {

        for (let column = 0; column < 4; column++) {

            const tile =
                document.createElement("div");

            tile.classList.add("tile");

            const value =
                board[row][column];

            if (value !== 0) {
                tile.textContent = value;
                tile.classList.add(
                    `tile-${value}`
                );
            }

            boardElement.appendChild(tile);
        }
    }

    scoreElement.textContent = score;

    updateBestScore();
}

// Load the Top 3 scores from the browser
function loadHighScores() {

    const savedScores =
        localStorage.getItem("highScores");

    if (savedScores) {
        return JSON.parse(savedScores);
    }

    return [];
}


// Display the Top 3 scores
function updateLeaderboard() {

    const highScores = loadHighScores();

    leaderboardElement.innerHTML = "";

    for (let i = 0; i < 3; i++) {

        const item =
            document.createElement("li");

        if (i < highScores.length) {

            item.textContent =
                `${highScores[i].name} - ${highScores[i].score}`;

        } else {

            item.textContent = "---";
        }

        leaderboardElement.appendChild(item);
    }
}


// Check whether the completed game made the Top 3
function checkHighScore() {

    const highScores = loadHighScores();

    const qualifies =
        highScores.length < 3 ||
        score > highScores[highScores.length - 1].score;

    if (!qualifies) {
        return;
    }

    let name = prompt(
        `Your score of ${score} made the Top 3!\n\n` +
        "Enter your name:"
    );

    if (!name || !name.trim()) {
        name = "Anonymous";
    }

    highScores.push({
        name: name.trim(),
        score: score
    });

    highScores.sort(
        (a, b) => b.score - a.score
    );

    const topThree =
        highScores.slice(0, 3);

    localStorage.setItem(
        "highScores",
        JSON.stringify(topThree)
    );

    updateLeaderboard();
}

// Update BEST score
function updateBestScore() {

    let bestScore =
        Number(localStorage.getItem("bestScore")) || 0;

    if (score > bestScore) {

        bestScore = score;

        localStorage.setItem(
            "bestScore",
            bestScore
        );
    }

    bestScoreElement.textContent =
        bestScore;
}


// Start a new game
function newGame(confirmRestart = true) {

    if (confirmRestart && score > 0) {

        const restart = confirm(
            "Are you sure you want to start a new game?\n\n" +
            "Your current game will be lost."
        );

        if (!restart) {
            return;
        }
    }

    board = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ];

    score = 0;
    winAnnounced = false;

    addTile();
    addTile();

    updateDisplay();
}


// Keyboard controls
document.addEventListener(
    "keydown",
    function (event) {

        const key = event.key.toLowerCase();

        if (
            key === "arrowleft" ||
            key === "a"
        ) {
            event.preventDefault();
            move("left");
        }

        else if (
            key === "arrowright" ||
            key === "d"
        ) {
            event.preventDefault();
            move("right");
        }

        else if (
            key === "arrowup" ||
            key === "w"
        ) {
            event.preventDefault();
            move("up");
        }

        else if (
            key === "arrowdown" ||
            key === "s"
        ) {
            event.preventDefault();
            move("down");
        }
    }
);

// Touch / swipe controls for mobile devices

let touchStartX = 0;
let touchStartY = 0;

boardElement.addEventListener(
    "touchstart",
    function (event) {

        const touch = event.changedTouches[0];

        touchStartX = touch.screenX;
        touchStartY = touch.screenY;
    },
    { passive: true }
);


boardElement.addEventListener(
    "touchend",
    function (event) {

        const touch = event.changedTouches[0];

        const touchEndX = touch.screenX;
        const touchEndY = touch.screenY;

        const differenceX =
            touchEndX - touchStartX;

        const differenceY =
            touchEndY - touchStartY;

        const minimumSwipeDistance = 30;

        // Ignore very small movements
        if (
            Math.abs(differenceX) < minimumSwipeDistance &&
            Math.abs(differenceY) < minimumSwipeDistance
        ) {
            return;
        }

        // Horizontal swipe
        if (
            Math.abs(differenceX) >
            Math.abs(differenceY)
        ) {

            if (differenceX > 0) {
                move("right");
            } else {
                move("left");
            }

        }

        // Vertical swipe
        else {

            if (differenceY > 0) {
                move("down");
            } else {
                move("up");
            }
        }
    },
    { passive: true }
);

// New Game button
newGameButton.addEventListener(
    "click",
    newGame
);

// Load saved leaderboard
updateLeaderboard();

// Start the first game
newGame(false);