import tkinter as tk
from DataClasses import AllSplitNames

class Menu(tk.Menu):
    def __init__(self,parent,callback,isPractice=False):
        super().__init__(parent,tearoff=False)
        self.splits = AllSplitNames.Splits()
        self.fileMenu = tk.Menu(parent, tearoff=False)

        self.add_cascade(label="Run Reference", menu=self.fileMenu)
        if not isPractice:
            lambdas = [[lambda game=game, category=category: callback(game,category) for category in self.splits.getCategories(game)] for game in self.splits.getGames()]
        i = 0
        for game in self.splits.getGames():
            recentMenu = tk.Menu(parent, tearoff=False)
            self.fileMenu.add_cascade(label=game,menu=recentMenu)
            j = 0
            for category in self.splits.getCategories(game):
                recentMenu.add_command(label=category,command=lambdas[i][j])
                j = j + 1
            i = i + 1
