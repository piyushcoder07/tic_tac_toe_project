import tkinter as tk
from tkinter import messagebox
import random

# Function to check if the board is full
def is_full(board):
    return " " not in [cell for row in board for cell in row]

# Function to check if a player has won
def check_winner(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True

    for i in range(3):
        if all([board[j][i] == player for j in range(3)]):
            return True

    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True

    return False

# Minimax algorithm for the computer player
def minimax(board, depth, is_maximizing):
    if check_winner(board, "X"):
        return -1
    if check_winner(board, "O"):
        return 1
    if is_full(board):
        return 0

    if is_maximizing:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    min_eval = min(min_eval, eval)
        return min_eval

# Function to handle computer's move
def computer_move():
    best_move = None
    best_eval = float('-inf')
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                eval = minimax(board, 0, False)
                board[i][j] = " "
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    return best_move

# Function to handle player's move
def handle_click(row, col):
    global current_player

    if board[row][col] == " ":
        board[row][col] = current_player
        buttons[row][col].config(text=current_player, state="disabled")

        if check_winner(board, current_player):
            messagebox.showinfo("Game Over", f"Player {current_player} wins!")
            reset_game()
        elif is_full(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_game()
        else:
            current_player = "O"
            label.config(text="Current Player: O")
            row, col = computer_move()
            board[row][col] = current_player
            buttons[row][col].config(text=current_player, state="disabled")

            if check_winner(board, current_player):
                messagebox.showinfo("Game Over", f"Player {current_player} wins!")
                reset_game()
            elif is_full(board):
                messagebox.showinfo("Game Over", "It's a draw!")
                reset_game()
            else:
                current_player = "X"
                label.config(text="Current Player: X")

# Function to reset the game
def reset_game():
    global board, current_player
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    label.config(text="Current Player: X")
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=" ", state="active")

# Create main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Create buttons for the Tic-Tac-Toe board
buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text=" ", font=("Helvetica", 20), width=4, height=2,
                                 command=lambda row=i, col=j: handle_click(row, col))
        buttons[i][j].grid(row=i, column=j)

# Create label to display current player
label = tk.Label(root, text="Current Player: X", font=("Helvetica", 14))
label.grid(row=3, columnspan=3)

# Initialize game variables
board = [[" " for _ in range(3)] for _ in range(3)]
current_player = "X"

# Run the game
root.mainloop()
