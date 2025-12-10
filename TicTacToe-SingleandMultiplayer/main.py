# Imports for Tkinter GUI application and random decider
import tkinter as tk
from tkinter import ttk
import random

# Const variable colors
BG_COLOR = "#0f1724"
BOARD_BG = "#1b2a41"
BTN_BG = "#243b55"
BTN_FG = "#e0e6ed"
BTN_ACTIVEBG = "#2d4d73"
TIE_BG = "#555555"
HIGHLIGHT = "#00c9a7"
TEXT_COLOR = "#ffffff"

# Main game function
class TicTacToe:
    # Constructor called when function is called initially
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe Game")
        # Sets background to const variable color
        self.root.config(bg=BG_COLOR)
        self.current_player = "X"
        self.game_active = True

        # Scores
        self.score_x = 0
        self.score_o = 0

        # Mode
        self.single_player = False

        # Board data
        self.board = [""] * 9

        # Functions to create initial game by creating UI and setting up board
        self.create_ui()
        self.setup_board()

    # Creates UI with single/multiplayer changer and reset button
    def create_ui(self):
        # Initial scoreboard setup
        self.score_label = tk.Label(self.root, text="X: 0   O: 0", font=("Helvetica", 20, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        self.score_label.pack(pady=10)

        # Mode selector (single/multiplayer)
        self.mode_var = tk.StringVar(value="Multiplayer")
        mode_menu = ttk.Combobox(self.root, textvariable=self.mode_var, values=["Multiplayer", "Single Player"], width=15)
        # Changes mode and resets board
        mode_menu.bind("<<ComboboxSelected>>", self.change_mode)
        mode_menu.pack(pady=5)

        # Board frame
        self.frame = tk.Frame(self.root, bg=BOARD_BG, bd=0)
        self.frame.pack(pady=20)

        # Reset button
        self.reset_btn = tk.Button(self.root, text="Reset Game", command=self.reset, bg=BTN_BG, fg=BTN_FG, font=("Helvetica", 14, "bold"), width=15, height=1, relief="ridge")
        self.reset_btn.pack(pady=10)

    # Setup board to start game
    def setup_board(self):
        self.buttons = []
        # Creates each button box in grid
        for i in range(9):
            btn = tk.Button(self.frame, text="", font=("Helvetica", 32, "bold"), width=4, height=1, bg=BTN_BG, fg=BTN_FG, activebackground=BTN_ACTIVEBG, command=lambda index=i: self.on_click(index))
            btn.grid(row=i // 3, column=i % 3, padx=8, pady=8)
            self.buttons.append(btn)

    # Called whenever the user clicks a space/button during the game
    def on_click(self, index):

        # Checks if the game is still active
        if not self.game_active:
            return

        # Checks if the space is empty to put the user's symbol there
        if self.board[index] == "":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)

            # Checks if a winner can be determined
            if self.check_winner():
                self.declare_winner(self.current_player)
                return

            # Checks if there are any available spots to determine a cats game
            if "" not in self.board:
                self.declare_draw()
                return

            # Switches turns
            self.switch_player()

            # For single player, calls CPU function to make a move
            if self.single_player and self.current_player == "O":
                self.root.after(300, self.ai_move)

    # Switches turns
    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    # For single player, CPU makes a move
    def ai_move(self):
        # Creates list of only the empty spots from 'board'
        empty = [i for i, v in enumerate(self.board) if v == ""]
        if not empty:
            return

        #Uses random import to select randomly from list 'empty'
        choice = random.choice(empty)
        #Prepares for on-click
        self.on_click(choice)

    # Checks if a winner can be determined
    def check_winner(self):
        # Win conditions by index
        wins = [
            (0,1,2), (3,4,5), (6,7,8),  # rows
            (0,3,6), (1,4,7), (2,5,8),  # cols
            (0,4,8), (2,4,6)]            # diagonals

        # Checks the wins list above for a win possibility, highlights winner
        for a,b,c in wins:
            if (self.board[a] == self.current_player and self.board[b] == self.current_player and self.board[c] == self.current_player):
                self.highlight_win([a,b,c])
                return True
        return False

    # Highlights the boxes of the winning player with const variable
    def highlight_win(self, indices):
        for i in indices:
            self.buttons[i].config(bg=HIGHLIGHT)

    # Declares the winner based on the check winner function, updates score
    def declare_winner(self, winner):
        self.game_active = False
        if winner == "X":
            self.score_x += 1
        else:
            self.score_o += 1
        #Updates scoreboard to play multiple rounds
        self.update_scoreboard()

    # Declares a cats game
    def declare_draw(self):
        self.game_active = False
        for btn in self.buttons:
            btn.config(bg=TIE_BG)

    # Updates scoreboard in UI
    def update_scoreboard(self):
        self.score_label.config(text=f"X: {self.score_x}   O: {self.score_o}")

    # Resets the board, similar to the set board function, used for all rounds after the first one
    def reset(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.game_active = True
        for btn in self.buttons:
            btn.config(text="", bg=BTN_BG)

    # Changing between single and multiplayer
    def change_mode(self, event):
        self.single_player = (self.mode_var.get() == "Single Player")
        self.reset()


# Main function / creation of root
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()