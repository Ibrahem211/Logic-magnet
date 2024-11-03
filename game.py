import tkinter as tk
from tkinter import messagebox
from board import create_board

class GameBoard(tk.Tk):
    def __init__(self, n, purple_magnet_pos, iron, zero, level_callback, red_magnet_pos=None):
        super().__init__()
        self.n = n
        self.board, self.purple_magnet_pos = create_board(n, purple_magnet_pos, iron, zero, red_magnet_pos)
        self.cell_size = 50
        self.canvas = tk.Canvas(self, width=n * self.cell_size, height=n * self.cell_size)
        self.canvas.pack()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)
        self.level_callback = level_callback
        self.selected_purple_magnet = None
        self.selected_red_magnet = None

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.n):
            for j in range(self.n):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = i * self.cell_size + self.cell_size
                cell_value = self.board[i][j]
                if cell_value == 'P':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='purple')
                elif cell_value == 'R':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='red')
                elif cell_value == 'H':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='grey')
                elif cell_value == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='blue')
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='white')
                self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(cell_value))

    def on_click(self, event):
        new_x = event.y // self.cell_size
        new_y = event.x // self.cell_size

        if self.board[new_x][new_y] == 'P':
            self.selected_purple_magnet = (new_x, new_y)
            print("purple Magnet selected at:", self.selected_purple_magnet)
            return 
        elif self.board[new_x][new_y] == 'R':
            self.selected_red_magnet = (new_x, new_y)
            print("red Magnet selected at:", self.selected_red_magnet)
            return
        
        if self.selected_purple_magnet:
            if self.move_purple_magnet(new_x, new_y):
                self.draw_board()
                self.check_win()
                self.selected_purple_magnet = None
        elif self.selected_red_magnet:
            if self.move_red_magnet(new_x, new_y):
                self.draw_board()
                self.check_win()
                self.selected_red_magnet = None 

    def move_purple_magnet(self, new_x, new_y):
        if 0 <= new_x < self.n and 0 <= new_y < self.n:
            if self.board[new_x][new_y] == 'H':
                print("Cannot move the purple magnet to that position! There is a piece of iron.")
                return False
            else:
                old_x, old_y = self.selected_purple_magnet
                self.board[old_x][old_y] = '*'
                self.board[new_x][new_y] = 'P'
                self.move_iron_toward_purple(new_x, new_y)
                return True

    def move_red_magnet(self, new_x, new_y):
        if 0 <= new_x < self.n and 0 <= new_y < self.n:
            if self.board[new_x][new_y] == 'H':
                print("Cannot move the red magnet to that position! There is a piece of iron.")
                return False
            else:
                old_x, old_y = self.selected_red_magnet
                self.board[old_x][old_y] = '*'
                self.board[new_x][new_y] = 'R'
                self.move_iron_toward_red(new_x, new_y) 
                return True

    def move_iron_toward_purple(self, magnet_x, magnet_y):
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1)
        ]
        moves = []

        for dx, dy in directions:
            x, y = magnet_x + dx, magnet_y + dy
            if 0 <= x < self.n and 0 <= y < self.n and self.board[x][y] == 'H':
                new_x = x + dx
                new_y = y + dy
                if 0 <= new_x < self.n and 0 <= new_y < self.n:
                    moves.append((x, y, new_x, new_y))

        for (x, y, new_x, new_y) in moves:
            self.board[new_x][new_y] = 'H'
            self.board[x][y] = '*'

    def move_iron_toward_red(self, magnet_x, magnet_y):
        directions = [
            (-2, 0), (2, 0), (0, -2), (0, 2)
        ]
        
        for dx, dy in directions:
            x, y = magnet_x + dx, magnet_y + dy
            if 0 <= x < self.n and 0 <= y < self.n and self.board[x][y] == 'H':
                new_x = magnet_x + dx // 2
                new_y = magnet_y + dy // 2
                if self.board[new_x][new_y] == '*'or self.board[new_x][new_y] == 0:
                    self.board[new_x][new_y] = 'H'
                    self.board[x][y] = '*'
                    print(f"Moved iron from ({x}, {y}) to ({new_x}, {new_y})")

    def check_win(self):
        for row in self.board:
            if 0 in row:  
                return
        messagebox.showinfo("Congratulations!", "You have covered all the zeros! You win!")
        self.after(1000, self.level_callback)