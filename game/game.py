import random

class TicTacToeGame:
    def __init__(self, board_size=3, vs_ai=False, player_mark='X'):
        self.board_size = board_size
        self.vs_ai = vs_ai
        self.board = [''] * (self.board_size * self.board_size)
        self.human_player_mark = player_mark
        self.current_player = player_mark
        self.game_over = False
        self.winner = None
        self.winning_combinations = self._generate_winning_combinations()

    def _generate_winning_combinations(self):
        """Generuje wszystkie możliwe zwycięskie kombinacje dla bieżącego rozmiaru planszy."""
        combinations = []
        # Wiersze
        for i in range(self.board_size):
            combinations.append([i * self.board_size + j for j in range(self.board_size)])
        # Kolumny
        for j in range(self.board_size):
            combinations.append([i * self.board_size + j for i in range(self.board_size)])
        # Przekątne
        combinations.append([i * self.board_size + i for i in range(self.board_size)])
        combinations.append([i * self.board_size + (self.board_size - 1 - i) for i in range(self.board_size)])
        return combinations

    def check_winner(self):
        """Sprawdza, czy jest zwycięzca na bieżącej planszy."""
        for combo in self.winning_combinations:
            first_cell_value = self.board[combo[0]]
            if first_cell_value and all(self.board[i] == first_cell_value for i in combo):
                return first_cell_value
        return None

    def check_draw(self):
        """Sprawdza, czy gra zakończyła się remisem."""
        return all(cell != '' for cell in self.board) and not self.winner

    def make_move(self, cell_index):
        """
        Próbuje wykonać ruch na planszy.
        Zwraca True, jeśli ruch się powiódł, w przeciwnym razie False.
        """
        if self.game_over or not (0 <= cell_index < len(self.board)) or self.board[cell_index] != '':
            return False

        self.board[cell_index] = self.current_player
        self.winner = self.check_winner()
        if self.winner:
            self.game_over = True
        elif self.check_draw():
            self.game_over = True
            self.winner = 'Remis' # <--- Zmieniono na polski
        else:
            # Zmień gracza
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def get_ai_move(self):
        """Określa następny ruch AI na podstawie prostej strategii."""
        # AI gra jako przeciwieństwo ludzkiego gracza
        player = 'X' if self.human_player_mark == 'O' else 'O'
        opponent = self.human_player_mark

        # 1. Sprawdź, czy AI może wygrać w następnym ruchu
        for combo in self.winning_combinations:
            ai_can_win_count = 0
            empty_cell = -1
            for cell_idx in combo:
                if self.board[cell_idx] == player:
                    ai_can_win_count += 1
                elif self.board[cell_idx] == '':
                    empty_cell = cell_idx
            if ai_can_win_count == self.board_size - 1 and empty_cell != -1:
                return empty_cell

        # 2. Sprawdź, czy AI musi zablokować gracza
        for combo in self.winning_combinations:
            opponent_can_win_count = 0
            empty_cell = -1
            for cell_idx in combo:
                if self.board[cell_idx] == opponent:
                    opponent_can_win_count += 1
                elif self.board[cell_idx] == '':
                    empty_cell = cell_idx
            if opponent_can_win_count == self.board_size - 1 and empty_cell != -1:
                return empty_cell

        # 3. Zajmij środek planszy (jeśli jest wolny)
        center_index = (self.board_size * self.board_size) // 2
        if self.board_size % 2 == 1 and self.board[center_index] == '':
            return center_index

        # 4. Zajmij róg (jeśli jest wolny) - losowo, aby zwiększyć różnorodność
        corners = [0, self.board_size - 1, self.board_size * (self.board_size - 1), self.board_size * self.board_size - 1]
        random.shuffle(corners)
        for corner in corners:
            if self.board[corner] == '':
                return corner

        # 5. Zajmij dowolne wolne pole
        available_moves = [i for i, cell in enumerate(self.board) if cell == '']
        if available_moves:
            return random.choice(available_moves)

        return -1 # Powinno wystąpić tylko w remisie, gdy nie ma więcej ruchów

    def get_game_state(self):
        """Zwraca słownik reprezentujący bieżący stan gry."""
        return {
            'board': self.board,
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner,
            'board_size': self.board_size,
            'vs_ai': self.vs_ai,
            'human_player_mark': self.human_player_mark
        }