import tkinter as tk
from Components import Info 
from util import timeHelpers as timeh

class PbInfo(Info.Info):
    def __init__(self,parent,state,config):
        Info.Info.__init__(self,parent,state,config)
        self.header.configure(text="Personal Best:")
        self.setInfo()

    def onSplit(self):
        if self.state.runEnded:
            self.setInfo(new=self.state.isPB())

    def setInfo(self,new=False):
        if new:
            time = self.state.currentRun.totals[-1]
        else:
            time = self.state.comparisons[2].totals[-1]
        self.info.configure(text=timeh.timeToString(time,{"precision":self.config["precision"]}))
