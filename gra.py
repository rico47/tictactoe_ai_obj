from flask import Flask, render_template, request, jsonify
from game.game import TicTacToeGame

app = Flask(__name__)

# Global game instance
# Initialize with default settings (3x3 board, Player vs. Player)
game = TicTacToeGame(board_size=3, vs_ai=False)


@app.route('/')
def index():
    """Renders the main game page."""
    return render_template('index.html', initial_game_state=game.get_game_state())


@app.route('/reset_game', methods=['POST'])
def reset_game():
    """Resets the game based on user-selected board size and AI option."""
    global game
    data = request.get_json()
    board_size = data.get('board_size', 3)
    vs_ai = data.get('vs_ai', False)
    game = TicTacToeGame(board_size, vs_ai)
    print(f"Wielkość planszy: {board_size}, vs_ai: {vs_ai}")
    return jsonify(game.get_game_state())


@app.route('/make_move', methods=['POST'])
def make_move():
    """Handles a player's move and, if applicable, the AI's move."""
    global game
    if game.game_over:
        return jsonify(game.get_game_state())

    data = request.get_json()
    cell_index = data['cell_index']

    if game.make_move(cell_index):
        # If playing against AI and it's AI's turn and the game isn't over
        if not game.game_over and game.vs_ai and game.current_player == 'O':
            ai_move_index = game.get_ai_move()
            if ai_move_index != -1:
                game.make_move(ai_move_index)  # AI makes its move

    return jsonify(game.get_game_state())


if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True)