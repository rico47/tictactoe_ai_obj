const gameBoard = document.getElementById('game-board');
const gameStatus = document.getElementById('game-status');
const resetButton = document.getElementById('reset-button');
const boardSizeSelect = document.getElementById('board-size');
const vsAiCheckbox = document.getElementById('vs-ai');

let currentGameState = {};

/**
 * Initializes the game board and state from the provided game state.
 * @param {object} gameState The current state of the game.
 */
function initializeGame(gameState) {
    currentGameState = gameState;
    renderBoard();
    updateStatus();
    setupEventListeners();
}

/**
 * Renders the Tic-Tac-Toe board based on the current game state.
 */
function renderBoard() {
    gameBoard.innerHTML = '';
    gameBoard.setAttribute('data-size', currentGameState.board_size); // Set data-size for CSS

    currentGameState.board.forEach((cellValue, index) => {
        const cell = document.createElement('div');
        cell.classList.add('cell');
        cell.setAttribute('data-index', index);
        cell.textContent = cellValue;

        if (cellValue !== '') {
            cell.classList.add('occupied');
            cell.classList.add(cellValue); // Add X or O class for styling
        }

        // Add event listener only if the game is not over and cell is empty
        if (!currentGameState.game_over && cellValue === '') {
            cell.addEventListener('click', handleCellClick);
        } else if (currentGameState.game_over) {
             // If game is over, remove click listener from all cells
             cell.removeEventListener('click', handleCellClick);
        }

        gameBoard.appendChild(cell);
    });
}

/**
 * Updates the game status message.
 */
function updateStatus() {
    if (currentGameState.game_over) {
        if (currentGameState.winner === 'Remis') {
            gameStatus.textContent = 'REMIS!';
            gameStatus.className = 'game-status draw';
        } else if (currentGameState.winner) {
            gameStatus.textContent = `${currentGameState.winner} Wygrywa!`;
            gameStatus.className = 'game-status winner';
        }
    } else {
        gameStatus.textContent = `Obecny gracz: ${currentGameState.current_player}`;
        gameStatus.className = 'game-status';
    }
}

/**
 * Handles a click on a game cell.
 * @param {Event} event The click event.
 */
async function handleCellClick(event) {
    if (currentGameState.game_over) {
        return;
    }

    const cellIndex = parseInt(event.target.getAttribute('data-index'));

    try {
        const response = await fetch('/make_move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ cell_index: cellIndex }),
        });
        const data = await response.json();
        currentGameState = data;
        renderBoard();
        updateStatus();
    } catch (error) {
        console.error('Błąd podczas ruchu:', error);
    }
}

/**
 * Sets up event listeners for control buttons.
 */
function setupEventListeners() {
    resetButton.addEventListener('click', async () => {
        const boardSize = parseInt(boardSizeSelect.value);
        const vsAi = vsAiCheckbox.checked;

        try {
            const response = await fetch('/reset_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ board_size: boardSize, vs_ai: vsAi }),
            });
            const data = await response.json();
            initializeGame(data); // Re-initialize with the new game state
        } catch (error) {
            console.error('Błąd, restart gry:', error);
        }
    });

    // Optional: Add listeners for board size/AI change if you want immediate updates without reset button
    // boardSizeSelect.addEventListener('change', () => { /* Logic to reset game */ });
    // vsAiCheckbox.addEventListener('change', () => { /* Logic to reset game */ });
}