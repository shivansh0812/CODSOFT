import math


class TicAI:
    def __init__(self):
        # Initialize a 3x3 board
        self.board = [' ' for _ in range(9)]
        self.human = 'X'
        self.kimu = 'O'

    def print_board(self):
        """Display the current board state."""
        for i in range(0, 9, 3):
            print(f" {self.board[i]} | {self.board[i + 1]} | {self.board[i + 2]} ")
            if i < 6:
                print("---|---|---")
        print()

    def is_winner(self, player):
        """Check if the given player has won."""
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),      # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),      # Columns
            (0, 4, 8), (2, 4, 6)                  # Diagonals
        ]
        return any(self.board[a] == self.board[b] == self.board[c] == player
                   for a, b, c in win_conditions)

    def is_board_full(self):
        """Check if the board is full."""
        return ' ' not in self.board

    def get_available_moves(self):
        """Return indices of empty spots."""
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def minimax(self, depth, is_maximizing):
        """
        Minimax algorithm.
        +10 → Kimu wins
        -10 → Human wins
        0   → Tie
        """
        if self.is_winner(self.kimu):
            return 10 - depth
        if self.is_winner(self.human):
            return -10 + depth
        if self.is_board_full():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for move in self.get_available_moves():
                self.board[move] = self.kimu
                score = self.minimax(depth + 1, False)
                self.board[move] = ' '
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = math.inf
            for move in self.get_available_moves():
                self.board[move] = self.human
                score = self.minimax(depth + 1, True)
                self.board[move] = ' '
                best_score = min(best_score, score)
            return best_score

    def get_best_move(self):
        """Determine Kimu's best move."""
        best_score = -math.inf
        best_move = None

        print("Kimu is thinking...")

        for move in self.get_available_moves():
            self.board[move] = self.kimu
            score = self.minimax(0, False)
            self.board[move] = ' '

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def play_game(self):
        """Main game loop."""
        print("🎮 Welcome to Tic-Tac-Toe!")
        print("I’m Kimu 🤖 and I never miss a move.")
        print("You play as 'X', I play as 'O'.")
        print("Choose positions from 0 to 8 as shown below:\n")
        print(" 0 | 1 | 2 ")
        print("---|---|---")
        print(" 3 | 4 | 5 ")
        print("---|---|---")
        print(" 6 | 7 | 8 \n")

        self.print_board()

        while True:
            # --- Human Turn ---
            while True:
                try:
                    move = int(input("Your move (0-8): "))
                    if move in self.get_available_moves():
                        self.board[move] = self.human
                        break
                    else:
                        print("That spot is not available. Try again.")
                except ValueError:
                    print("Please enter a valid number between 0 and 8.")

            self.print_board()

            if self.is_winner(self.human):
                print("🎉 You won! Well played.")
                break
            if self.is_board_full():
                print("🤝 It's a tie! Looks like we're evenly matched.")
                break

            # --- Kimu's Turn ---
            ai_move = self.get_best_move()
            self.board[ai_move] = self.kimu
            print(f"Kimu chose position {ai_move}")
            self.print_board()

            if self.is_winner(self.kimu):
                print("🤖 Kimu wins! That was a good game.")
                break
            if self.is_board_full():
                print("🤝 It's a tie! Nobody wins this one.")
                break


if __name__ == "__main__":
    game = TicAI()
    game.play_game()
