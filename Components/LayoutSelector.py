import tkinter as tk
from util import layoutHelper as lh

class Selector(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        for i in range(3):
            self.columnconfigure(i,weight=1)

        self.layoutName = "System Default"
        self.layoutVar = tk.StringVar()
        self.layoutVar.set(self.layoutName)
        self.layoutVar.trace('w',self.setLayout)
        self.layoutCombo = tk.ttk.Combobox(self,values=lh.getLayouts(),textvariable=self.layoutVar)
        layoutLabel = tk.Label(self,text="Layout:")
        self.layoutCombo.grid(row=0,column=1,columnspan=2,sticky="WE")
        layoutLabel.grid(row=0,column=0,sticky="W")

    def setLayout(self,*args):
        self.layoutName = self.layoutVar.get()
