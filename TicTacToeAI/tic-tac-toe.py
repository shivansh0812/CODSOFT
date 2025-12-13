import math


class TicAI:
    def __init__(self):
        # Initialize a 3x3 board with empty spaces
        self.board = [' ' for _ in range(9)]
        self.human = 'X'
        self.ai = 'O'

    def print_board(self):
        """Displays the current state of the board."""
        for i in range(0, 9, 3):
            row = f" {self.board[i]} | {self.board[i + 1]} | {self.board[i + 2]} "
            print(row)
            if i < 6:
                print("---|---|---")
        print("\n")

    def is_winner(self, player):
        """Checks if a specific player has won."""
        # Winning combinations: rows, columns, diagonals
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)  # Diagonals
        ]
        for a, b, c in win_conditions:
            if self.board[a] == self.board[b] == self.board[c] == player:
                return True
        return False

    def is_board_full(self):
        """Checks if there are no empty spots left."""
        return ' ' not in self.board

    def get_available_moves(self):
        """Returns a list of indices where the board is empty."""
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def minimax(self, depth, is_maximizing):
        """
        The Minimax algorithm.
        Returns +10 if Kimu (AI) wins, -10 if Human wins, 0 for Tie.
        """
        # Base cases: Check for terminal states (win/loss/draw)
        if self.is_winner(self.ai):
            return 10 - depth  # Prefer winning sooner
        if self.is_winner(self.human):
            return -10 + depth  # Prefer losing later
        if self.is_board_full():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for move in self.get_available_moves():
                self.board[move] = self.ai
                score = self.minimax(depth + 1, False)
                self.board[move] = ' '  # Undo move
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for move in self.get_available_moves():
                self.board[move] = self.human
                score = self.minimax(depth + 1, True)
                self.board[move] = ' '  # Undo move
                best_score = min(score, best_score)
            return best_score

    def get_best_move(self):
        """Finds the optimal move for the AI using Minimax."""
        best_score = -math.inf
        move = None

        print("Kimu is thinking...")
        # Check all available moves and pick the one with the highest minimax score
        for i in self.get_available_moves():
            self.board[i] = self.ai
            score = self.minimax(0, False)
            self.board[i] = ' '  # Undo move

            if score > best_score:
                best_score = score
                move = i
        return move

    def play_game(self):
        """Main game loop."""
        print("Welcome to Tic-Tac-Toe AI- me Kimu!")
        print("You are 'X' and I choose 'O'.")
        print("Enter positions 0-8 (0 is top-left, 8 is bottom-right).\n")

        self.print_board()

        while True:
            # --- Human Turn ---
            while True:
                try:
                    move = int(input("Enter your move (0-8): "))
                    if move in self.get_available_moves():
                        self.board[move] = self.human
                        break
                    else:
                        print("Invalid move. Spot already taken or is out of range.")
                except ValueError:
                    print("Please enter a number.")

            self.print_board()

            if self.is_winner(self.human):
                print("Congratulations! You won!")
                break
            if self.is_board_full():
                print("It's a Tie! Don't know if it's good for you or bad for me ;)")
                break

            # --- (Kimu's) AI Turn ---
            ai_move = self.get_best_move()
            self.board[ai_move] = self.ai
            print(f"Kimu chose position {ai_move}")
            self.print_board()

            if self.is_winner(self.ai):
                print("Kimu Wins! Better luck next time.")
                break
            if self.is_board_full():
                print("It's a Tie!, Don't know if it's good for you or bad for me ;)")
                break


if __name__ == "__main__":
    game = TicAI()
    game.play_game()