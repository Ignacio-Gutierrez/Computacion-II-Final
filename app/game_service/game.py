class Connect_4:
    
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.turns = 0

    def player_turn(self):
        return ['X', 'O'][self.turns % 2]

    def put_token(self, col):
        col -= 1
        for row in range(7, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = self.player_turn()
                self.turns += 1
                return True
        return False  # Columna llena

    def winner(self):
        directions = {
            (0, 1): "Horizontal",    # Horizontal
            (1, 0): "Vertical",      # Vertical
            (1, 1): "Diagonal Negativa",  # Diagonal negativa
            (1, -1): "Diagonal Positiva"  # Diagonal positiva
        }

        for row in range(8):
            for col in range(8):
                if self.board[row][col] != ' ':
                    for direction, name in directions.items():
                        if self.check_direction(row, col, *direction):
                            return f'El Jugador {self.board[row][col]} ganó con 4 en {name}'

        if not any(' ' in row for row in self.board):
            return 'Empate'

        return True

    def check_direction(self, row, col, d_row, d_col):
        initial = self.board[row][col]
        for i in range(1, 4):
            r, c = row + i * d_row, col + i * d_col
            if r < 0 or r >= 8 or c < 0 or c >= 8 or self.board[r][c] != initial:
                return False
        return True
