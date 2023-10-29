import tkinter as tk
from tkinter import messagebox, Toplevel
import random

def create_board(rows, cols, mines):
    board = [[' ' for _ in range(cols)] for _ in range(rows)]

    # Place mines randomly
    for _ in range(mines):
        while True:
            x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)
            if board[x][y] != 'X':
                board[x][y] = 'X'
                break

    return board

def count_adjacent_mines(board, x, y):
    rows, cols = len(board), len(board[0])
    count = 0

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if 0 <= x + dx < rows and 0 <= y + dy < cols and board[x + dx][y + dy] == 'X':
                count += 1

    return count

def uncover_cell(x, y):
    if 0 <= x < rows and 0 <= y < cols and not revealed[x][y]:
        revealed[x][y] = True

        if board[x][y] == 'X':
            canvas.create_oval(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill='red')
            game_over()
        else:
            mine_count = count_adjacent_mines(board, x, y)
            if mine_count > 0:
                canvas.create_text(x * cell_size + cell_size / 2, y * cell_size + cell_size / 2, text=str(mine_count), fill='blue', font=("Helvetica", 12, "bold"))
            else:
                canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill='white')
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        uncover_cell(x + dx, y + dy)

def left_click(event):
    x, y = event.x // cell_size, event.y // cell_size
    uncover_cell(x, y)

def right_click(event):
    x, y = event.x // cell_size, event.y // cell_size
    if not revealed[x][y]:
        if flags[x][y]:
            canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill='gray')
            flags[x][y] = False
        else:
            canvas.create_text(x * cell_size + cell_size / 2, y * cell_size + cell_size / 2, text='F', fill='black', font=("Helvetica", 12, "bold"))
            flags[x][y] = True

def game_over():
    for x in range(rows):
        for y in range(cols):
            if board[x][y] == 'X':
                canvas.create_oval(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill='red')
            else:
                if flags[x][y]:
                    canvas.create_text(x * cell_size + cell_size / 2, y * cell_size + cell_size / 2, text='F', fill='black', font=("Helvetica", 12, "bold"))
    messagebox.showinfo("Game Over", "You lost! Try again.")
    restart_game()

def restart_game():
    global board, revealed, flags
    board = create_board(rows, cols, num_mines)
    revealed = [[False for _ in range(cols)] for _ in range(rows)]
    flags = [[False for _ in range(cols)] for _ in range(rows)]
    canvas.delete("all")
    for x in range(rows):
        for y in range(cols):
            canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill='gray')

def show_rules():
    rules_window = Toplevel(root)
    rules_window.title("Rules")
    rules_text = """
    Welcome to Minesweeper!

    Rules:
    1. Click a cell to uncover it.
    2. Numbers indicate how many mines are adjacent to that cell.
    3. Right-click to place or remove flags on suspected mines.
    4. The game is won when all safe cells are uncovered.
    5. The game is lost if you uncover a mine.

    Have fun and good luck!
    """
    rules_label = tk.Label(rules_window, text=rules_text, font=("Helvetica", 12))
    rules_label.pack()

rows, cols, num_mines = 10, 10, 10
cell_size = 30

board = create_board(rows, cols, num_mines)
revealed = [[False for _ in range(cols)] for _ in range(rows)]
flags = [[False for _ in range(cols)] for _ in range(rows)]

root = tk.Tk()
root.title('Minesweeper')

canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size, bg='lightgray')
canvas.pack()

canvas.bind("<Button-1>", left_click)
canvas.bind("<Button-3>", right_click)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
menu_bar.add_command(label="Rules", command=show_rules)

for x in range(rows):
    for y in range(cols):
        canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill='gray')

restart_button = tk.Button(root, text="Play Again", command=restart_game)
restart_button.pack()

root.mainloop()