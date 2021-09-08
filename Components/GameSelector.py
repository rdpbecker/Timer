import tkinter as tk
from tkinter import ttk
from DataClasses import AllSplitNames

class Selector(tk.Frame):
    # game = ""
    # category = ""
    # splits = None
    # gameVar = None
    # cateVar = None
    # cateCombo = None
    followup = None

    def __init__(self,parent,allowInvalid=False):
        super().__init__(parent)
        for i in range(3):
            self.columnconfigure(i,weight=1)

        self.game = ""
        self.category = ""
        self.splits = AllSplitNames.Splits()
        self.allowInvalid = allowInvalid

        self.gameVar = tk.StringVar()
        self.gameVar.trace('w',self.setGame)
        gameCombo = ttk.Combobox(self,values=self.splits.getGames(),textvariable=self.gameVar)
        gameLabel = tk.Label(self,text="Game:")
        gameCombo.grid(row=0,column=1,columnspan=2,sticky="WE")
        gameLabel.grid(row=0,column=0,sticky="W")

        self.cateVar = tk.StringVar()
        self.cateVar.trace('w',self.setCate)
        self.cateCombo = ttk.Combobox(self,values=self.splits.getCategories(self.game),textvariable=self.cateVar)
        cateLabel = tk.Label(self,text="Category:")
        self.cateCombo.grid(row=1,column=1,columnspan=2,sticky="WE")
        cateLabel.grid(row=1,column=0,sticky="W")

    def setGame(self,*_):
        if self.allowInvalid or self.gameVar.get() in self.splits.getGames():
            self.game = self.gameVar.get()
        else:
            self.game = ""
        self.updateCateCombo()
        self.cateVar.set("")

    def setCate(self,*args):
        cate = self.cateVar.get()
        if self.allowInvalid or not cate or self.splits.validPair(self.game,cate):
            self.category = cate
            if self.followup:
                self.followup(*args)

    def updateCateCombo(self):
        self.cateCombo["values"] = self.splits.getCategories(self.game)
