import tkinter as tk

class Popup:
    # master = None
    # callback = None
    # window = None
    # retVal = None
    # closeAction = None

    def __init__(self,master,callbacks,closeAction="rejected"):
        self.master = master
        self.callbacks = callbacks
        self.window = tk.Toplevel(self.master)
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.retVal = {"exitCode": ""}
        self.closeAction = closeAction

    def show(self):
        pass

    def accept(self,_=None):
        self.setReturn()
        self.retVal["exitCode"] = "accepted"
        self.finish()

    def close(self,_=None):
        self.setReturn()
        self.retVal["exitCode"] = self.closeAction
        self.finish()

    def reject(self,_=None):
        self.setReturn()
        self.retVal["exitCode"] = "rejected"
        self.finish()

    def finish(self,_=None):
        self.setReturn()
        self.window.destroy()
        if self.retVal["exitCode"] in self.callbacks.keys():
            if len(list(self.retVal.keys())) == 1:
                self.callbacks[self.retVal["exitCode"]]()
            else:
                self.callbacks[self.retVal["exitCode"]](self.retVal)

    def setReturn(self):
        pass
