import tkinter as tk
from game import GameBoard

class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Logic Magnets")
        self.geometry("300x200")

        title_label = tk.Label(self, text="Logic Magnets", font=("Helvetica", 24))
        title_label.pack(pady=20)

        play_button = tk.Button(self, text="Play", command=self.open_levels, font=("Helvetica", 16))
        play_button.pack(pady=10)

    def open_levels(self):
        self.destroy()  
        GameLevels()  

class GameLevels(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Select Level")
        self.geometry("600x600")

        title_label = tk.Label(self, text="Select Level", font=("Helvetica", 24))
        title_label.grid(row=0, column=0, columnspan=5, pady=20)

        # مشان حدد مكان الاحجار بكل مرحلة
        self.levels = {
            1: {
                'size': 4,
                'purple_magnet_pos': (2, 0),
                'iron': [(1, 2)],
                'zero': [(1, 1), (1,3)]
            },
            2: {
                'size': 5,
                'purple_magnet_pos': (4, 0),
                'iron': [(2, 1), (1, 2), (2,3), (3,2)],
                'zero': [(0, 2), (2, 0), (2,2), (2,4), (4,2)]
            },
            3: {
                'size': 4,
                'purple_magnet_pos': (2, 0),
                'iron': [(1, 2)],
                'zero': [(0, 3), (2,3)]
            },
            4: {
                'size': 5,
                'purple_magnet_pos': (2, 0),
                'iron': [(1, 1), (3, 1)],
                'zero': [(0, 0), (0, 2), (4, 1)]
            },

             5: {
                'size': 4,
                'purple_magnet_pos': (3, 1),
                'iron': [(1, 0), (2, 0), (1, 2), (2, 2)],
                'zero': [(0, 0), (0, 2), (3, 0)]
            },
             6: {
                'size': 5,
                'purple_magnet_pos': (2, 0),
                'iron': [(1, 1), (1, 3),],
                'zero': [(0, 3), (1, 2), (2, 3)]
            },
             7: {
                'size': 5,
                'purple_magnet_pos': (2, 1),
                'iron': [(1, 0), (2, 0),(3,1),(3,2)],
                'zero': [(0, 0), (2, 3), (4, 3)]
            },
            8: {
                'size': 4,
                'purple_magnet_pos': (2, 0),
                'iron': [(1, 1), (1, 2)],
                'zero': [(0, 0), (0, 2), (2, 2)]
            },
             9: {
                'size': 7,
                'purple_magnet_pos': (0, 0),
                'iron': [(0, 3), (0, 5)],
                'zero': [(0, 1), (0, 6)]
            },
             10: {
                'size': 4,
                'purple_magnet_pos': (0, 0),
                'iron': [(2, 2), (2, 3),(3,1)],
                'zero': [(1, 1), (1, 3) , (3,0),(3,3)]
            },
             11: {
                'size': 5,
                'purple_magnet_pos': None,
                'iron': [(0, 0), (0, 4)],
                'zero': [(0, 1), (0, 2), (0,3)],
                'red_magnet_pos': (1, 3) 
            },
            12: {
                'size': 5,
                'purple_magnet_pos': None,
                'iron': [(0, 0), (1, 0),(4,4)],
                'zero': [(2, 0), (4, 0), (4,3)],
                'red_magnet_pos': (3, 1) 
            },
             13: {
                'size': 5,
                'purple_magnet_pos': None,
                'iron': [(0, 0), (1, 0),(4,4)],
                'zero': [(2, 0), (4, 0), (4,3)],
                'red_magnet_pos': (3, 1) 
            },
            14: {
                'size': 4,
                'purple_magnet_pos': None,
                'iron': [(0, 3), (2, 0),(3,0)],
                'zero': [(1, 0), (1, 2), (2,1),(2,2)],
                'red_magnet_pos': (3, 3) 
            },
            15: {
                'size': 5,
                'purple_magnet_pos': (1,2),
                'iron': [(0, 1), (0, 3)],
                'zero': [(0, 0), (0, 2), (1,4),(2,4)],
                'red_magnet_pos': (2, 2) 
            },
            16: {
                'size': 5,
                'purple_magnet_pos': (2,4),
                'iron': [(1, 2), (3, 2)],
                'zero': [(0, 3), (0, 4), (4,0),(4,3)],
                'red_magnet_pos': (2, 0) 
            },
             17: {
                'size': 4,
                'purple_magnet_pos': (3,3),
                'iron': [(0, 2), (2, 0)],
                'zero': [(1, 1), (1, 3), (2,2),(3,1)],
                'red_magnet_pos': (0, 0) 
            },
            18: {
                'size': 6,
                'purple_magnet_pos': (4,3),
                'iron': [(0, 3), (2, 0), (2,5)],
                'zero': [(1, 3), (2, 1), (2,2),(2,3)],
                'red_magnet_pos': (4, 2) 
            },
             19: {
                'size': 5,
                'purple_magnet_pos': (0,2),
                'iron': [(0, 1), (0, 3), (4,1),(4,3)],
                'zero': [(1, 3), (2, 1), (2,2),(2,3)],
                'red_magnet_pos': (3, 2) 
            },
            20: {
                'size': 5,
                'purple_magnet_pos': (4,2),
                'iron': [(0, 1), (0, 2), (4,0)],
                'zero': [(1, 0), (0, 4), (2,0),(3,0)],
                'red_magnet_pos': (4, 4) 
            },
            21:{
                'size': 4,
                'purple_magnet_pos': (2,1),
                'iron': [(1, 2)],
                'zero': [(1, 3), (0, 2)],
                'red_magnet_pos': (2, 0)
                }
        }

        for i in range(1, len(self.levels) + 1):
            level_button = tk.Button(self, text=f"Level {i}", font=("Helvetica", 14),
                                     command=lambda level=i: self.start_game(level))

            level_button.grid(row=(i-1)//5 + 1, column=(i-1)%5, padx=10, pady=10)

            level_button.config(state=tk.NORMAL)

    def start_game(self, level):
        level_data = self.levels[level]
        n = level_data['size']
        purple_magnet_pos = level_data['purple_magnet_pos']
        iron = level_data['iron']
        zero = level_data['zero']
        red_magnet_pos = level_data.get('red_magnet_pos')

        self.destroy() 
        app = GameBoard(n, purple_magnet_pos, iron, zero, self.open_levels, red_magnet_pos)
        app.title("Magnet Game")
        app.mainloop()

    def open_levels(self):
        new_window = GameLevels()
        new_window.mainloop()
