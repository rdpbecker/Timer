import tkinter as tk
from Components import Info

class CompareInfo(Info.Info):
    def __init__(self,parent,state):
        Info.Info.__init__(self,parent,state)
        self.header.configure(text="Comparing Against:")
        self.info.configure(text=state.currentComparison.totalHeader)

    def onComparisonChanged(self):
        self.info.configure(text=self.state.currentComparison.totalHeader)
