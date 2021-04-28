import tkinter as tk
from tkinter import ttk
from Dialogs import BaseDialog
from util import fileio
from util import layoutHelper as lh

class RunSelector(BaseDialog.Dialog):
    game = ""
    category = ""
    layoutName = "System Default"
    splits = None
    gameVar = None
    cateVar = None
    layoutVar = None
    cateCombo = None

    def __init__(self,splits):
        BaseDialog.Dialog.__init__(self)
        self.splits = splits
        self.retVal = {\
            "game": "",\
            "category": "",\
            "layoutName": "System Default"\
        }

        menubar = tk.Menu(self.root, tearoff=False)
        fileMenu = tk.Menu(self.root, tearoff=False)

        menubar.add_cascade(label="Run Reference", menu=fileMenu)
        lambdas = [[lambda game=game, category=category: self.setRun(game,category) for category in splits.getCategories(game)] for game in splits.getGames()]
        i = 0
        for game in splits.getGames():
            recentMenu = tk.Menu(self.root, tearoff=False)
            fileMenu.add_cascade(label=game,menu=recentMenu)
            j = 0
            for category in splits.getCategories(game):
                recentMenu.add_command(label=category,command=lambdas[i][j])
                j = j + 1
            i = i + 1
        self.root.configure(bg="black",menu=menubar)

        self.gameVar = tk.StringVar()
        self.gameVar.trace('w',self.setGame)
        gameCombo = tk.ttk.Combobox(self.root,values=splits.getGames(),textvariable=self.gameVar)
        gameLabel = tk.Label(self.root,bg="black",fg="white",text="Game:")
        gameCombo.grid(row=0,column=4,columnspan=8,sticky="WE")
        gameLabel.grid(row=0,column=0,columnspan=4,sticky="W")

        self.cateVar = tk.StringVar()
        self.cateVar.trace('w',self.setCate)
        self.cateCombo = tk.ttk.Combobox(self.root,values=splits.getCategories(self.game),textvariable=self.cateVar)
        cateLabel = tk.Label(self.root,bg="black",fg="white",text="Category:")
        self.cateCombo.grid(row=1,column=4,columnspan=8,sticky="WE")
        cateLabel.grid(row=1,column=0,columnspan=4,sticky="W")

        self.layoutVar = tk.StringVar()
        self.layoutVar.set("System Default")
        self.layoutVar.trace('w',self.setLayout)
        self.layoutCombo = tk.ttk.Combobox(self.root,values=lh.getLayouts(),textvariable=self.layoutVar)
        layoutLabel = tk.Label(self.root,bg="black",fg="white",text="Layout:")
        self.layoutCombo.grid(row=2,column=4,columnspan=8,sticky="WE")
        layoutLabel.grid(row=2,column=0,columnspan=4,sticky="W")

        confirm = tk.Button(self.root,fg="black",bg="steel blue",text="Confirm Selection",command=self.accept)
        confirm.grid(row=3,column=0,columnspan=12,sticky="WE")

    def setRun(self,game,category):
        self.game = game
        self.gameVar.set(game)
        self.category = category
        self.cateVar.set(category)
        self.updateCateCombo()

    def setGame(self,*args):
        self.game = self.gameVar.get()
        self.updateCateCombo()
        self.category = ""
        self.retVal["game"] = self.game
        self.retVal["category"] = self.category
        self.retVal["splitNames"] = self.splits.getSplitNames(self.game,self.category)

    def setCate(self,*args):
        self.category = self.cateVar.get()
        self.retVal["category"] = self.category
        self.retVal["splitNames"] = self.splits.getSplitNames(self.game,self.category)

    def updateCateCombo(self):
        self.cateCombo["values"] = self.splits.getCategories(self.game)

    def setLayout(self,*args):
        self.layoutName = self.layoutVar.get()
        self.retVal["layoutName"] = self.layoutName

    def accept(self):
        if not self.game or not self.category or not self.layoutName:
            error = tk.Label(self.root,bg="black",fg="white",text="A game and category must both be selected.")
            error.grid(row=4,column=0,columnspan=12,sticky="WE")
            return
        self.root.destroy()

    def finish(self):
        self.accept()
