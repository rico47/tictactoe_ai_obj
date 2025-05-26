from flask import Flask, render_template, request, jsonify
from game.game import TicTacToeGame

app = Flask(__name__)

# Globalna instancja gry
# Inicjalizacja z domyślnymi ustawieniami (plansza 3x3, Gracz vs. Gracz, Gracz to X)
game = TicTacToeGame(board_size=3, vs_ai=False, player_mark='X')


@app.route('/')
def index():
    """Renderuje główną stronę gry."""
    return render_template('index.html', initial_game_state=game.get_game_state())


@app.route('/reset_game', methods=['POST'])
def reset_game():
    """Resetuje grę na podstawie wybranego przez użytkownika rozmiaru planszy, opcji AI i znaku gracza."""
    global game
    data = request.get_json()
    board_size = data.get('board_size', 3)
    vs_ai = data.get('vs_ai', False)
    player_mark = data.get('player_mark', 'X')
    game = TicTacToeGame(board_size, vs_ai, player_mark)
    print(
        f"Zainicjowano grę o rozmiarze planszy: {board_size}, vs_ai: {vs_ai}, znak gracza: {player_mark}")  # <--- Polski komunikat
    return jsonify(game.get_game_state())


@app.route('/make_move', methods=['POST'])
def make_move():
    """Obsługuje ruch gracza, a jeśli dotyczy, również ruch AI."""
    global game
    if game.game_over:
        return jsonify(game.get_game_state())

    data = request.get_json()
    cell_index = data['cell_index']

    if game.make_move(cell_index):
        # Jeśli gra przeciwko AI i jest tura AI oraz gra nie jest zakończona
        # AI gra przeciwnym znakiem niż gracz.
        if not game.game_over and game.vs_ai and game.current_player != game.human_player_mark:
            ai_move_index = game.get_ai_move()
            if ai_move_index != -1:
                game.make_move(ai_move_index)  # AI wykonuje swój ruch

    return jsonify(game.get_game_state())


if __name__ == '__main__':
    # Uruchom serwer deweloperski Flask
    app.run(debug=True)