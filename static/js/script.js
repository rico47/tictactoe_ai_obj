const gameBoard = document.getElementById('game-board');
const gameStatus = document.getElementById('game-status');
const resetButton = document.getElementById('reset-button');
const boardSizeSelect = document.getElementById('board-size');
const playerMarkSelect = document.getElementById('player-mark');
const vsAiCheckbox = document.getElementById('vs-ai');

let currentGameState = {};

/**
 * Inicjalizuje planszę gry i stan na podstawie dostarczonego stanu gry.
 * @param {object} gameState Bieżący stan gry.
 */
function initializeGame(gameState) {
    currentGameState = gameState;
    // Ustawia kontrolki tak, aby odpowiadały bieżącemu stanowi gry
    boardSizeSelect.value = currentGameState.board_size;
    vsAiCheckbox.checked = currentGameState.vs_ai;
    playerMarkSelect.value = currentGameState.human_player_mark;

    renderBoard();
    updateStatus();
    setupEventListeners();
}

/**
 * Renderuje planszę Kółko i Krzyżyk na podstawie bieżącego stanu gry.
 */
function renderBoard() {
    gameBoard.innerHTML = '';
    gameBoard.setAttribute('data-size', currentGameState.board_size); // Ustawia data-size dla CSS

    currentGameState.board.forEach((cellValue, index) => {
        const cell = document.createElement('div');
        cell.classList.add('cell');
        cell.setAttribute('data-index', index);
        cell.textContent = cellValue;

        if (cellValue !== '') {
            cell.classList.add('occupied');
            cell.classList.add(cellValue); // Dodaje klasę X lub O do stylizacji
        }

        // Dodaje nasłuch zdarzeń tylko, jeśli gra nie jest zakończona, a komórka jest pusta
        if (!currentGameState.game_over && cellValue === '') {
            cell.addEventListener('click', handleCellClick);
        } else if (currentGameState.game_over) {
             // Jeśli gra jest zakończona, upewnij się, że nasłuch zdarzeń kliknięcia jest usunięty ze wszystkich komórek
             cell.removeEventListener('click', handleCellClick); // Dobra praktyka usuwania, jeśli istnieje
        }

        gameBoard.appendChild(cell);
    });
}

/**
 * Aktualizuje komunikat o stanie gry.
 */
function updateStatus() {
    if (currentGameState.game_over) {
        if (currentGameState.winner === 'Remis') {
            gameStatus.textContent = 'Remis!'; // <--- Polski komunikat
            gameStatus.className = 'game-status draw';
        } else if (currentGameState.winner) {
            gameStatus.textContent = `${currentGameState.winner} wygrywa!`; // <--- Polski komunikat
            gameStatus.className = 'game-status winner';
        }
    } else {
        gameStatus.textContent = `Aktualny gracz: ${currentGameState.current_player}`; // <--- Polski komunikat
        gameStatus.className = 'game-status';
    }
}

/**
 * Obsługuje kliknięcie na komórkę gry.
 * @param {Event} event Zdarzenie kliknięcia.
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
        console.error('Błąd podczas wykonywania ruchu:', error); // <--- Polski komunikat
    }
}

/**
 * Ustawia nasłuch zdarzeń dla przycisków sterowania.
 */
function setupEventListeners() {
    resetButton.addEventListener('click', async () => {
        const boardSize = parseInt(boardSizeSelect.value);
        const vsAi = vsAiCheckbox.checked;
        const playerMark = playerMarkSelect.value;

        try {
            const response = await fetch('/reset_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ board_size: boardSize, vs_ai: vsAi, player_mark: playerMark }),
            });
            const data = await response.json();
            initializeGame(data); // Ponowna inicjalizacja nowym stanem gry
        } catch (error) {
            console.error('Błąd podczas resetowania gry:', error); // <--- Polski komunikat
        }
    });
}