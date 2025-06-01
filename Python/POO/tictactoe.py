#%%
class tic_tac_toe():
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # A list to hold the board state
        self.current_player = 'X'  # The current player, either 'X' or 'O'

    def print_board(self):
        # Print the board in a 3x3 grid format
        print(f"{self.board[0]} | {self.board[1]} | {self.board[2]}")
        print("-" * 9)
        print(f"{self.board[3]} | {self.board[4]} | {self.board[5]}")
        print("-" * 9)
        print(f"{self.board[6]} | {self.board[7]} | {self.board[8]}")
        print("\n")

    def make_move(self, position):
        # Place the current player's mark on the board at the specified position
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            return True
        else:
            print("Invalid move. Try again.")
            return False
    def check_winner(self): 
        # Check all possible winning combinations
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
            (0, 4, 8), (2, 4, 6)              # Diagonal
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return True
        return False
    def check_draw(self):
        # Check if the board is full and there is no winner
        return ' ' not in self.board and not self.check_winner()
    def switch_player(self):
        # Switch the current player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    def play_game(self):
        # Main game loop
        while True:
            self.print_board()
            try:
                position = int(input(f"Player {self.current_player}, enter your move (0-8): "))
                if position < 0 or position > 8:
                    print("Invalid input. Please enter a number between 0 and 8.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 8.")
                continue

            if self.make_move(position):
                if self.check_winner():
                    self.print_board()
                    print(f"Player {self.current_player} wins!")
                    break
                elif self.check_draw():
                    self.print_board()
                    print("It's a draw!")
                    break
                self.switch_player()

# %%
if __name__ == "__main__":
    game = tic_tac_toe()
    game.play_game()
# %%
