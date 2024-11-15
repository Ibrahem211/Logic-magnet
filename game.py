import tkinter as tk
from tkinter import messagebox
from board import create_board
from bfs import bfs_solve
from dfs import dfs_solve
import time

class GameBoard(tk.Tk):
    def __init__(self, n, purple_magnet_pos, iron, zero, level_callback, red_magnet_pos=None):
        super().__init__()
        self.n = n
        self.board, self.purple_magnet_pos = create_board(n, purple_magnet_pos, iron, zero, red_magnet_pos)
        self.red_magnet_pos = red_magnet_pos 
        self.cell_size = 50
        self.canvas = tk.Canvas(self, width=n * self.cell_size, height=n * self.cell_size)
        self.canvas.pack()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)
        self.level_callback = level_callback
        self.selected_purple_magnet = None
        self.selected_red_magnet = None
        self.original_zero_positions = [(i, j) for i in range(self.n) for j in range(self.n) if self.board[i][j] == 0]
        
        solve_button_bfs = tk.Button(self, text="حل باستخدام bfs", command=self.solve_bfs)
        solve_button_bfs.pack(pady=10)
        
        solve_button_dfs = tk.Button(self, text="حل باستخدام dfs", command=self.solve_dfs)
        solve_button_dfs.pack(pady=10)

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

    def animate_solution(self, solution_steps):
        if solution_steps:
            for step in solution_steps:
                magnet_type, new_pos = step
                if magnet_type == 'P':
                    self.selected_purple_magnet = self.purple_magnet_pos
                    self.move_purple_magnet(*new_pos)
                    self.purple_magnet_pos = new_pos
                elif magnet_type == 'R' and self.red_magnet_pos is not None:
                    self.selected_red_magnet = self.red_magnet_pos
                    self.move_red_magnet(*new_pos)
                    self.red_magnet_pos = new_pos

                self.update_zeros()
                self.draw_board()
                self.update()
                time.sleep(0.5)

                if self.check_win():
                    print("win!")
                    return
                else:
                    print("The current state is not winning.")



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
                self.update_zeros()
                self.draw_board()
                self.check_win()
                self.selected_purple_magnet = None
        elif self.selected_red_magnet:
            if self.move_red_magnet(new_x, new_y):
                self.update_zeros()
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
        iron_in_row = []
        for x in range(self.n):
            if self.board[x][magnet_y] == 'H':
                iron_in_row.append((x, magnet_y))
        
        for (x, y) in iron_in_row:
            direction = 1 if x > magnet_x else -1
            new_x = x + direction
            if 0 <= new_x < self.n and (self.board[new_x][y] == '*' or self.board[new_x][y] == 0):
                self.board[new_x][y] = 'H'
                self.board[x][y] = '*'
                print(f"Moved iron in row from ({x}, {y}) to ({new_x}, {y})")

        iron_in_column = []
        for y in range(self.n):
            if self.board[magnet_x][y] == 'H':
                iron_in_column.append((magnet_x, y))

        for (x, y) in iron_in_column:
            direction = 1 if y > magnet_y else -1
            new_y = y + direction
            if 0 <= new_y < self.n and (self.board[x][new_y] == '*' or self.board[x][new_y] == 0):
                self.board[x][new_y] = 'H'
                self.board[x][y] = '*'
                print(f"Moved iron in column from ({x}, {y}) to ({x}, {new_y})")

    def update_zeros(self):
        for (x, y) in self.original_zero_positions:
            if self.board[x][y] == '*':
                self.board[x][y] = 0


    def move_iron_toward_red(self, magnet_x, magnet_y):
        iron_in_row = []
        for x in range(self.n):
            if self.board[x][magnet_y] == 'H':
                iron_in_row.append((x, magnet_y))

        for (x, y) in iron_in_row:
            direction = 1 if x > magnet_x else -1
            new_x = x - direction 
            if 0 <= new_x < self.n and (self.board[new_x][y] == '*' or self.board[new_x][y] == 0):
                self.board[new_x][y] = 'H'
                self.board[x][y] = '*'
                print(f"Moved iron in row from ({x}, {y}) to ({new_x}, {y})")

        iron_in_column = []
        for y in range(self.n):
            if self.board[magnet_x][y] == 'H':
                iron_in_column.append((magnet_x, y))

        for (x, y) in iron_in_column:
            direction = 1 if y > magnet_y else -1
            new_y = y - direction
            if 0 <= new_y < self.n and (self.board[x][new_y] == '*' or self.board[x][new_y] == 0):
                self.board[x][new_y] = 'H'
                self.board[x][y] = '*'
                print(f"Moved iron in column from ({x}, {y}) to ({x}, {new_y})")

    def solve_bfs(self):
        solution_steps = bfs_solve(self.board, self.purple_magnet_pos, self.n, self.red_magnet_pos)
        if solution_steps is None:
            messagebox.showinfo("No Solution", "لا يوجد حل لهذا المستوى.")
        else:
            self.animate_solution(solution_steps)

    def solve_dfs(self):
        solution_steps = dfs_solve(self.board, self.purple_magnet_pos, self.n, self.red_magnet_pos)
        if solution_steps is None:
            messagebox.showinfo("No Solution", "لا يوجد حل لهذا المستوى.")
        else:
            self.animate_solution(solution_steps)


    def check_win(self):
        for row in self.board:
            if 0 in row:
                print("Victory has not been achieved yet. There are empty cells")
                return False
        print("Get the win!")
        messagebox.showinfo("Congratulations!", "You have covered all the zeros! You win!")
        self.after(1000, self.level_callback)
        return True
