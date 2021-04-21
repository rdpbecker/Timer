import tkinter as tk
from Components import Info
from util import timeHelpers as timeh

class TimeSaveInfo(Info.Info):
    def __init__(self,parent,state,config):
        Info.Info.__init__(self,parent,state,config)
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
            {\
                "precision": self.config["precision"],\
                "noPrecisionOnMinute": self.config["noPrecisionOnMinute"]\
            }\
        ))
