import tkinter as tk

class Popup:
    # master = None
    # callback = None
    # window = None
    # retVal = None

    def __init__(self,master,callback):
        self.master = master
        self.callback = callback
        self.window = tk.Toplevel(self.master)
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.retVal = {"exitCode": ""}

    def show(self):
        pass

    def accept(self,_=None):
        self.setReturn()
        self.retVal["exitCode"] = "accept"
        self.finish()

    def close(self,_=None):
        self.setReturn()
        self.retVal["exitCode"] = "close"
        self.finish()

    def reject(self,_=None):
        self.setReturn()
        self.retVal["exitCode"] = "reject"
        self.finish()

    def finish(self,_=None):
        self.setReturn()
        self.window.destroy()
        if self.callback:
            self.callback(self.retVal)

    def setReturn(self):
        pass
