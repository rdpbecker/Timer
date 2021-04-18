import tkinter as tk

class Component(tk.Frame):
    state = None
    config = None

    def __init__(self,parent,state,config={}):
        tk.Frame.__init__(self,parent)
        self.state = state
        self.config = config
        self.configureColumns()

    def configureColumns(self):
        for i in range(12):
            self.columnconfigure(i,minsize=25,weight=1)

    def frameUpdate(self):
        pass

    def onStarted(self):
        pass

    def onSplit(self):
        pass

    def onComparisonChanged(self):
        pass

    def onPaused(self):
        pass

    def onSplitSkipped(self):
        pass

    def onReset(self):
        pass

    def onRestart(self):
        pass
