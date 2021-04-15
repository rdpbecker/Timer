import tkinter as tk
from Components import Info
import timeHelpers as timeh

class TimeSaveInfo(Info.Info):
    def __init__(self,parent,state):
        Info.Info.__init__(self,parent,state)
        self.header.configure(text="Possible Time Save:")
        self.setInfo()

    def onSplit(self):
        self.updateIfNecessary()
    
    def onComparisonChanged(self):
        self.updateIfNecessary()

    def onSplitSkipped(self):
        self.updateIfNecessary()

    def updateIfNecessary(self):
        if self.state.runEnded:
            return
        self.setInfo()

    def setInfo(self):
        self.info.configure(text=timeh.timeToString(\
            timeh.difference(\
                self.state.currentComparison.segments[self.state.splitnum],\
                self.state.comparisons[0].segments[self.state.splitnum]\
            ),\
            {"precision":2})\
        )
