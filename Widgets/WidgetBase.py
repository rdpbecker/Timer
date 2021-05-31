import tkinter as tk

class WidgetBase(tk.Frame):
    state = None
    config = None

    def __init__(self,parent,state,config):
        tk.Frame.__init__(self,parent)
        self.state = state
        self.config = config
        self.configureColumns()

    def configureColumns(self):
        for i in range(12):
            self.columnconfigure(i,minsize=27,weight=1)

    def shouldHide(self):
        if not "hideOnBlank" in self.config.keys():
            return False
        return self.state.currentComparison.totalHeader == "Blank" and self.config["hideOnBlank"]

    def hide(self):
        pass

    def frameUpdate(self):
        pass

    def preStart(self):
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

    def runChanged(self,**kwargs):
        self.state = kwargs["state"]
        self.resetUI()

    # Reset the UI on state change that requires it.
    def resetUI(self):
        pass
