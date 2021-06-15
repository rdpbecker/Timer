import tkinter as tk
from DataClasses import AllSplitNames

class Selector(tk.Frame):
    game = ""
    category = ""
    splits = None
    gameVar = None
    cateVar = None
    cateCombo = None

    def __init__(self,parent):
        super().__init__(parent)
        self.splits = AllSplitNames.Splits()

        self.gameVar = tk.StringVar()
        self.gameVar.trace('w',self.setGame)
        gameCombo = tk.ttk.Combobox(self,values=self.splits.getGames(),textvariable=self.gameVar)
        gameLabel = tk.Label(self,text="Game:")
        gameCombo.grid(row=0,column=4,columnspan=8,sticky="WE")
        gameLabel.grid(row=0,column=0,columnspan=4,sticky="W")

        self.cateVar = tk.StringVar()
        self.cateVar.trace('w',self.setCate)
        self.cateCombo = tk.ttk.Combobox(self,values=self.splits.getCategories(self.game),textvariable=self.cateVar)
        cateLabel = tk.Label(self,text="Category:")
        self.cateCombo.grid(row=1,column=4,columnspan=8,sticky="WE")
        cateLabel.grid(row=1,column=0,columnspan=4,sticky="W")

    def setGame(self,*args):
        self.game = self.gameVar.get()
        self.updateCateCombo()
        self.category = ""
        self.cateVar.set("")

    def setCate(self,*args):
        self.category = self.cateVar.get()

    def updateCateCombo(self):
        self.cateCombo["values"] = self.splits.getCategories(self.game)
