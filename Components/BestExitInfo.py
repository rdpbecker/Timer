import tkinter as tk
from Components import Info
from util import timeHelpers as timeh

class BestExitInfo(Info.Info):
    def __init__(self,parent,state,config):
        Info.Info.__init__(self,parent,state,config)
        self.header.configure(text="Best Exit?")

    def onSplit(self):
        self.updateBestExit(self.state.splitnum-1)

    def onRestart(self):
        self.info.configure(text="")

    def updateBestExit(self,splitnum):
        if not timeh.greater(self.state.comparisons[3].totalDiffs[splitnum],0)\
            or\
            (timeh.isBlank(self.state.comparisons[3].totals[splitnum])\
            and not timeh.isBlank(self.state.currentRun.totals[splitnum])):
            self.info.configure(text="Yes",fg=self.config["colours"]["yes"])
        else:
            self.info.configure(text="No",fg=self.config["colours"]["no"])
