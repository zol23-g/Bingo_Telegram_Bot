import random

class BingoGame:
    def __init__(self):
        self.players = {}
        self.boards = {}
    
    def generate_board(self):
        # Generate a random BINGO board (5x5 grid)
        board = []
        for col in range(5):
            start, end = col * 15 + 1, col * 15 + 15
            board.append(random.sample(range(start, end + 1), 5))
        return list(map(list, zip(*board)))  # Transpose for columns
    
    def add_player(self, player_id):
        if player_id not in self.players:
            board = self.generate_board()
            self.players[player_id] = {"board": board, "marked": [[False] * 5 for _ in range(5)]}
            self.boards[player_id] = board
            return board
        return None
    
    def mark_number(self, player_id, number):
        if player_id not in self.players:
            return False
        board = self.players[player_id]["board"]
        marked = self.players[player_id]["marked"]
        for i in range(5):
            for j in range(5):
                if board[i][j] == number:
                    marked[i][j] = True
                    return True
        return False

    def check_bingo(self, player_id):
        marked = self.players[player_id]["marked"]
        # Check rows, columns, and diagonals
        for row in marked:
            if all(row):
                return True
        for col in zip(*marked):
            if all(col):
                return True
        if all(marked[i][i] for i in range(5)) or all(marked[i][4 - i] for i in range(5)):
            return True
        return False
