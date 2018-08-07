import tkinter as tk
from GameMVC import Controller

if __name__ == '__main__':
    root = tk.Tk()
    app = Controller(root)
    app.bind_actions()
    root.geometry('600x378')
    root.title('Tic Tac Katsu')
    root.mainloop()