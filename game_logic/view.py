import tkinter as tk



class View(tk.Frame):
    def __init__(self, parent):
        self.game_state = 1
        
        tk.Frame.__init__(self, parent)

        self.board_spaces = [[tk.Label(self, text=chr(65+i)+str(j), font='Courier', bg='gainsboro', borderwidth=1, relief='solid', width=4, height=2) for j in range(9)] for i in range(9)]


        # event handling should happen in controller
        def handle_enter(event):
            if event.widget['bg'] == "gainsboro":
                event.widget.configure(bg="SeaGreen3")


        def handle_leave(event):
            if event.widget['bg'] == "SeaGreen3":
                event.widget.configure(bg="gainsboro")


        def handle_click(event):
            if event.widget['bg'] not in ['pink', 'lightblue']:
                if self.game_state == 1:
                    event.widget.configure(bg='pink')
                    self.game_state = 2
                else:
                    event.widget.configure(bg='lightblue')
                    self.game_state = 1

        # pink
        # lightblue


        for i in range(9):
            for j in range(9):
                self.board_spaces[i][j].bind("<Enter>", handle_enter)
                self.board_spaces[i][j].bind("<Leave>", handle_leave)
                self.board_spaces[i][j].bind("<Button-1>", handle_click)


        for i in range(9):
            for j in range(9):
                #calculation of converted row idx
                k = (6 if i > 5 else (3 if i > 2 else 0)) + (2 if j > 5 else (1 if j > 2 else 0))
                #calculation of converted col idx
                l = 3*(i%3) + (j%3)
                self.board_spaces[i][j].grid(row=k, column=l)

        

if __name__ == "__main__":
    root = tk.Tk()
    View(root).pack(fill="both", expand=True)
    root.geometry("700x450")
    root.mainloop()