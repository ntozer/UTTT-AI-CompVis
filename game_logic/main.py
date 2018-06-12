from controller import Controller
import tkinter as tk

root = tk.Tk()
app = Controller(root)
app.bind_actions()
root.geometry("700x450")
root.mainloop()