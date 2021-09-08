import tkinter as tk
from tkinter import ttk
from Components import GameSelector

class Selector(GameSelector.Selector):
    def __init__(self,parent):
        super().__init__(parent)
        self.splitVar = tk.StringVar()
        self.splitVar.trace('w',self.setName)
        self.splitCombo = ttk.Combobox(self,values=self.splits.getSplitNames(self.game,self.category),textvariable=self.splitVar)
        splitLabel = tk.Label(self,text="Segment Name:")
        self.splitCombo.grid(row=2,column=1,columnspan=2,sticky="WE")
        splitLabel.grid(row=2,column=0,sticky="W")
        self.split = ""

    def setGame(self,*args):
        super().setGame(args)
        self.updateNameCombo()
        self.splitVar.set("")

    def setCate(self,*args):
        super().setCate(args)
        self.updateNameCombo()
        self.splitVar.set("")

    def setName(self,*_):
        split = self.splitVar.get()
        if split in self.splits.getSplitNames(self.game,self.category):
            self.split = split
        else:
            self.split = ""

    def updateNameCombo(self):
        self.splitCombo["values"] = self.splits.getSplitNames(self.game,self.category)
