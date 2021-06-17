import tkinter as tk

class Dialog():
    root = None
    retVal = None

    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.finish)
        self.retVal = {"exitType": ""}

    def show(self):
        self.root.mainloop()
        return self.retVal

    def accept(self):
        self.setReturn()
        self.retVal["exitType"] = "accept"
        self.root.destroy()

    def reject(self):
        self.setReturn()
        self.retVal["exitType"] = "reject"
        self.root.destroy()

    def finish(self):
        self.setReturn()
        self.root.destroy()

    def setReturn(self):
        pass
