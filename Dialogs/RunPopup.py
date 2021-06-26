import tkinter as tk
from tkinter import ttk
from Components import GameSelector
from DataClasses import AllSplitNames
from Dialogs import Popup
from util import layoutHelper as lh

class RunPopup(Popup.Popup):
    game = ""
    category = ""
    splits = None
    gameVar = None
    cateVar = None
    cateCombo = None

    def __init__(self,master,callback,session):
        super().__init__(master,callback)
        self.session = session
        self.splits = AllSplitNames.Splits()
        self.game = session.game
        self.category = session.category

        self.window.configure(bg="black")
        self.window.title("Choose Run")

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

        self.selector = GameSelector.Selector(self.window)
        self.selector.pack()

        confirm = tk.Button(self.window,fg="black",bg="steel blue",text="Confirm Selection",command=self.accept)
        confirm.pack(fill="x")

    def setRun(self,game,category):
        self.selector.gameVar.set(game)
        self.selector.cateVar.set(category)

    def setReturn(self):
        self.retVal["game"] = self.selector.game
        self.retVal["category"] = self.selector.category
