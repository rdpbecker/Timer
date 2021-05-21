# Run tkinter code in another thread

import tkinter as tk
import threading
from PracticeComponents import VarianceColumn

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

    ##########################################################
    ## Show the window, and call the first update after one
    ## frame.
    ##########################################################
    def startGui(self):
        self.root.mainloop()

    def showVariances(self,variance,sort):
        self.base.update(variance)
        self.sort.update(sort)
