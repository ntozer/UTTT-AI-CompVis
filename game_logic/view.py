import tkinter as tk


class View(tk.Frame):
    def __init__(self, parent):
               
        tk.Frame.__init__(self, parent)

        self.colors = ('gainsboro', 'gray58')
        self.valid_colors = ('SeaGreen2', 'SpringGreen3')
        self.p1_colors = ('brown1', 'firebrick3')
        self.p2_colors = ('RoyalBlue1', 'SlateBlue3')
        self.invalid_colors = ('gray15', 'gray10')

        self.board_spaces = [[tk.Label(self, text=chr(65+i)+str(j), font='Courier', bg=(self.colors[0] if i%2==0 else self.colors[1]), width=4, height=2) for j in range(9)] for i in range(9)]

        for i in range(9):
            for j in range(9):
                #calculation of converted row idx
                k = (6 if i > 5 else (3 if i > 2 else 0)) + (2 if j > 5 else (1 if j > 2 else 0))
                #calculation of converted col idx
                l = 3*(i%3) + (j%3)
                self.board_spaces[i][j].grid(row=k, column=l)
                

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x450")
    root.mainloop()