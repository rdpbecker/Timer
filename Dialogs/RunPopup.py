import tkinter as tk
from tkinter import ttk
from DataClasses import AllSplitNames
from Dialogs import Popup
from util import layoutHelper as lh

class RunPopup(Popup.Popup):
    game = ""
    category = ""
    split = None
    gameVar = None
    cateVar = None
    cateCombo = None

    def __init__(self,master,callback):
        Popup.Popup.__init__(self,master,callback)
        self.splits = AllSplitNames.Splits()

    def show(self):
        self.retVal = {\
            "game": "",\
            "category": "",\
            "splitNames": []\
        }
        self.window.configure(bg="black")

        menubar = tk.Menu(self.window, tearoff=False)
        fileMenu = tk.Menu(self.window, tearoff=False)

        menubar.add_cascade(label="Run Reference", menu=fileMenu)
        lambdas = [[lambda game=game, category=category: self.setRun(game,category) for category in self.splits.getCategories(game)] for game in self.splits.getGames()]
        i = 0
        for game in self.splits.getGames():
            recentMenu = tk.Menu(self.window, tearoff=False)
            fileMenu.add_cascade(label=game,menu=recentMenu)
            j = 0
            for category in self.splits.getCategories(game):
                recentMenu.add_command(label=category,command=lambdas[i][j])
                j = j + 1
            i = i + 1
        self.window.configure(bg="black",menu=menubar)

        self.gameVar = tk.StringVar()
        self.gameVar.trace('w',self.setGame)
        gameCombo = tk.ttk.Combobox(self.window,values=self.splits.getGames(),textvariable=self.gameVar)
        gameLabel = tk.Label(self.window,bg="black",fg="white",text="Game:")
        gameCombo.grid(row=0,column=4,columnspan=8,sticky="WE")
        gameLabel.grid(row=0,column=0,columnspan=4,sticky="W")

        self.cateVar = tk.StringVar()
        self.cateVar.trace('w',self.setCate)
        self.cateCombo = tk.ttk.Combobox(self.window,values=self.splits.getCategories(self.game),textvariable=self.cateVar)
        cateLabel = tk.Label(self.window,bg="black",fg="white",text="Category:")
        self.cateCombo.grid(row=1,column=4,columnspan=8,sticky="WE")
        cateLabel.grid(row=1,column=0,columnspan=4,sticky="W")

        confirm = tk.Button(self.window,fg="black",bg="steel blue",text="Confirm Selection",command=self.accept)
        confirm.grid(row=3,column=0,columnspan=12,sticky="WE")

    def setRun(self,game,category):
        self.gameVar.set(game)
        self.cateVar.set(category)

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
