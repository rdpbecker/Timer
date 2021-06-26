import tkinter as tk

class Popup:
    master = None
    callback = None
    window = None
    retVal = None

    def __init__(self,master,callback):
        self.master = master
        self.callback = callback
        self.window = tk.Toplevel(self.master)
        self.window.protocol("WM_DELETE_WINDOW", self.close)

    def show(self):
        pass

    def accept(self,event=None):
        self.finish()

    def close(self,event=None):
        self.finish()

    def reject(self,event=None):
        self.finish()

    def finish(self,event=None):
        self.window.destroy()
        if self.callback:
            self.callback(self.retVal)
