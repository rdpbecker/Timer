import tkinter as tk

class Dialog():
    root = None
    retVal = None

    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.finish)

    def show(self):
        self.root.mainloop()
        return self.retVal

    def accept(self):
        self.retVal = True
        self.root.quit()

    def reject(self):
        self.retVal = False
        self.root.quit()

    def finish(self):
        self.root.quit()
