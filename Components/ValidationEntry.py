import tkinter as tk

class Entry(tk.Entry):
    def __init__(self,parent,val,cb,**kwargs):
       super().__init__(parent,**kwargs)
       self.var = tk.StringVar(self,val)
       self["textvariable"] = self.var
       self.var.trace('w',self.doValidation)
       self.val = val
       self.callback = cb

    def doValidation(self,*args):
        val = self.var.get()
        if self.callback(val):
            self.val = val
            self["bg"] = "white"
        else:
            self["bg"] = "#ff6666"

    def setText(self,text):
        self.val = text
        self.var.set(text)
