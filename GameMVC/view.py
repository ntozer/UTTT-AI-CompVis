import tkinter as tk
from GameMVC import Coord

class View(tk.Frame):
    def __init__(self, parent):
               
        tk.Frame.__init__(self, parent)

        self.colors = ('gainsboro', 'gray58')
        self.valid_colors = ('SeaGreen2', 'SpringGreen3')
        self.p1_colors = ('brown1', 'firebrick3')
        self.p2_colors = ('RoyalBlue1', 'SlateBlue3')
        self.invalid_colors = ('gray15', 'gray10')

        # creating game board interface
        self.board_spaces = [[tk.Label(self, text=chr(65+i)+str(j), font='Courier', bg=(self.colors[0] if i%2==0 else self.colors[1]), width=4, height=2) for j in range(9)] for i in range(9)]
        for i in range(9):
            for j in range(9):
                # calculation of converted row idx
                k = (6 if i > 5 else (3 if i > 2 else 0)) + (2 if j > 5 else (1 if j > 2 else 0))
                # calculation of converted col idx
                l = 3*(i%3) + (j%3)
                self.board_spaces[i][j].grid(row=k, column=l)
                
        # placing restart button
        self.restart_btn = tk.Button(self, text='Restart')
        self.restart_btn.grid(row=1, column=9, padx=10)

        # placing simulation button
        self.simulate_btn = tk.Button(self, text='Simulate')
        self.simulate_btn.grid(row=2, column=9, padx=10)
        # placing simulation count box
        self.simulate_txt = tk.Text(self, height=1, width=10)
        self.simulate_txt.insert('end', '100000')
        self.simulate_txt.grid(row=3, column=9, padx=10)

        # placing AI make move button
        self.ai_move_btn = tk.Button(self, text='AI Move')
        self.ai_move_btn.grid(row=4, column=9, padx=10)

    def reset_board(self):
        for i in range(9):
            for j in range(9):
                color_idx = 1
                if i%2 == 0:
                    color_idx = 0
                self.board_spaces[i][j].configure(bg=self.colors[color_idx])

    def update_visuals(self, coord, player):
        def get_active_board_tile(coord):
            return self.board_spaces[coord.x][coord.y]

        active_tile = get_active_board_tile(coord)

        if active_tile['bg'] not in self.p1_colors and active_tile['bg'] not in self.p2_colors:
            color_idx = 1
            if active_tile['bg'] == self.valid_colors[0] or active_tile['bg'] == self.colors[0]:
                color_idx = 0
            if player == 1:
                active_tile.configure(bg=self.p1_colors[color_idx])
            else:
                active_tile.configure(bg=self.p2_colors[color_idx])

    def popup_msg(self, msg):
        popup = tk.Tk()
        popup.wm_title()
        label = tk.Label(popup, text=msg)
        label.pack(side='top', fill='x', pady=10)
        btn = tk.Button(popup, text='Okay', command=popup.destroy)
        btn.pack()
        popup.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x450")
    root.mainloop()
