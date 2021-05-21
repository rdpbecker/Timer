# Run tkinter code in another thread

import tkinter as tk
import threading
from Variance import VarianceColumn
from DataClasses import AllSplitNames
import varianceCalculator as varcalc

class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    ##########################################################
    ## Creates the window with the destruction callback, and
    ## sets control callbacks.
    ##########################################################
    def setupGui(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.root.title("Variance Calculator")
        for i in range(12):
            self.root.columnconfigure(i,weight=1)
        self.base = VarianceColumn.VarianceColumn(self.root,"In Order")
        self.sort = VarianceColumn.VarianceColumn(self.root,"Sorted")
        self.base.pack(side="left")
        self.sort.pack(side="right")

        self.splits = AllSplitNames.Splits()
        menubar = tk.Menu(self.root, tearoff=False)
        fileMenu = tk.Menu(self.root, tearoff=False)

        menubar.add_cascade(label="Run Reference", menu=fileMenu)
        lambdas = [[lambda game=game, category=category: self.setRun(game,category) for category in self.splits.getCategories(game)] for game in self.splits.getGames()]
        i = 0
        for game in self.splits.getGames():
            recentMenu = tk.Menu(self.root, tearoff=False)
            fileMenu.add_cascade(label=game,menu=recentMenu)
            j = 0
            for category in self.splits.getCategories(game):
                recentMenu.add_command(label=category,command=lambdas[i][j])
                j = j + 1
            i = i + 1
        self.root.configure(bg="black",menu=menubar)

    ##########################################################
    ## Show the window, and call the first update after one
    ## frame.
    ##########################################################
    def startGui(self):
        self.root.mainloop()

    def showVariances(self,variance,sort):
        self.base.update(variance)
        self.sort.update(sort)

    def setRun(self,game,category):
        variances = varcalc.computeVariances(game,category,self.splits)
        self.showVariances(variances["order"],variances["sorted"])
