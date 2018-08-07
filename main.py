import tkinter as tk
from GameLogic.controller import Controller

if __name__ == '__main__':
    root = tk.Tk()
    app = Controller(root)
    app.bind_actions()
    root.geometry("700x450")
    root.mainloop()