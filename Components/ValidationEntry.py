import tkinter as tk

class Entry(tk.Entry):
    followup = None
    def __init__(self,parent,val,cbs,**kwargs):
        super().__init__(parent,**kwargs)
        self.var = tk.StringVar(self,val)
        self["textvariable"] = self.var
        self.trace = self.var.trace('w',self.doValidation)
        self.val = val
        self.validate = cbs["validate"]
        if "followup" in cbs.keys():
            self.followup = cbs["followup"]

    def doValidation(self,*args):
        val = self.var.get()
        if self.validate(val):
            self.val = val
            self["bg"] = "white"
            if self.followup:
                self.followup(val)
        else:
            self["bg"] = "#ff6666"

    def setText(self,text):
        self.val = text
        self.var.trace_vdelete("w",self.trace)
        self.var.set(text)
        self.trace = self.var.trace('w',self.doValidation)
