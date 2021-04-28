import tkinter as tk
from tkinter import ttk
from Dialogs import BaseDialog
from util import fileio
from util import layoutHelper as lh

class RunSelector(BaseDialog.Dialog):
    game = ""
    category = ""
    split = ""
    splits = None
    gameVar = None
    cateVar = None
    cateCombo = None

    def __init__(self,splits):
        BaseDialog.Dialog.__init__(self)
        self.root.title("Choose Run and Split")
        self.splits = splits
        self.retVal = {\
            "game": "",\
            "category": "",\
            "split": "",\
            "splitNames": [],\
        }

        menubar = tk.Menu(self.root, tearoff=False)
        fileMenu = tk.Menu(self.root, tearoff=False)

        menubar.add_cascade(label="Run Reference", menu=fileMenu)
        lambdas = [[[lambda game=game, category=category, name=name: self.setSplit(game,category,name) for name in splits.getSplitNames(game,category)] for category in splits.getCategories(game)] for game in splits.getGames()]
        i = 0
        for game in splits.getGames():
            recentMenu = tk.Menu(self.root, tearoff=False)
            fileMenu.add_cascade(label=game,menu=recentMenu)
            j = 0
            for category in splits.getCategories(game):
                splitsMenu = tk.Menu(self.root, tearoff=False)
                recentMenu.add_cascade(label=category,menu=splitsMenu)
                k = 0
                for name in splits.getSplitNames(game,category):
                    splitsMenu.add_command(label=name,command=lambdas[i][j][k])
                    k = k + 1
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

        self.splitVar = tk.StringVar()
        self.splitVar.trace('w',self.setName)
        self.splitCombo = tk.ttk.Combobox(self.root,values=splits.getSplitNames(self.game,self.category),textvariable=self.splitVar)
        splitLabel = tk.Label(self.root,bg="black",fg="white",text="Segment Name:")
        self.splitCombo.grid(row=2,column=4,columnspan=8,sticky="WE")
        splitLabel.grid(row=2,column=0,columnspan=4,sticky="W")

        confirm = tk.Button(self.root,fg="black",bg="steel blue",text="Confirm Selection",command=self.accept)
        confirm.grid(row=4,column=0,columnspan=12,sticky="WE")

    def setSplit(self,game,category,split):
        self.game = game
        self.gameVar.set(game)
        self.category = category
        self.cateVar.set(category)
        self.split = split
        self.splitVar.set(split)
        self.updateCateCombo()

    def setGame(self,*args):
        self.game = self.gameVar.get()
        self.updateCateCombo()
        self.category = ""
        self.split = ""
        self.retVal["game"] = self.game
        self.retVal["category"] = self.category
        self.retVal["split"] = self.split
        self.retVal["splitNames"] = self.splits.getSplitNames(self.game,self.category)

    def setCate(self,*args):
        self.category = self.cateVar.get()
        self.split = ""
        self.retVal["category"] = self.category
        self.retVal["split"] = self.split
        self.retVal["splitNames"] = self.splits.getSplitNames(self.game,self.category)

    def setName(self,*args):
        self.split = self.splitVar.get()
        self.retVal["split"] = self.split

    def updateCateCombo(self):
        self.cateCombo["values"] = self.splits.getCategories(self.game)

    def updateNameCombo(self):
        self.splitCombo["values"] = self.splits.getSplitNames(self.game,self.category)

    def accept(self):
        if not self.game or not self.category or not self.split:
            error = tk.Label(self.root,bg="black",fg="white",text="A game, category, and segment must all be selected.")
            error.grid(row=5,column=0,columnspan=12,sticky="WE")
            return
        self.root.destroy()

    def finish(self):
        self.accept()
