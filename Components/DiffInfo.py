import tkinter as tk
from Components import Info
from util import timeHelpers as timeh

class DiffInfo(Info.Info):
    def __init__(self,parent,state,config):
        Info.Info.__init__(self,parent,state,config)
        self.header.configure(text="Last Split (vs Best):")

    def frameUpdate(self):
        if self.state.runEnded:
            return
        if not timeh.greater(self.state.comparisons[0].segments[self.state.splitnum],self.state.segmentTime)\
            and not timeh.isBlank(self.state.comparisons[0].segments[self.state.splitnum])\
            and not (self.state.splitnum and self.state.currentRun.segments[self.state.splitnum-1]):

            self.header.configure(text="Current Segment:")
            self.info.configure(text=timeh.timeToString(\
                timeh.difference(self.state.segmentTime,self.state.comparisons[0].segments[self.state.splitnum]),\
                {"showSign": True, "precision":2})\
            )
            self.info.configure(fg=self.setCurrentColour())

    def onSplit(self):
        self.splitEndUpdate()

    def onSplitSkipped(self):
        self.splitEndUpdate()

    def splitEndUpdate(self):
        if not self.state.splitnum:
            return
        self.header.configure(text="Last Split (vs Best):")
        self.info.configure(text=self.state.comparisons[0].getString("segmentDiffs",self.state.splitnum-1,{"showSign":True,"precision":2}))
        self.info.configure(fg=self.setPreviousColour())

    def setCurrentColour(self):
        split = self.state.splitnum
        if timeh.isBlank(self.state.currentComparison.segments[split]):
            return self.config["colours"]["skipped"]

        elif timeh.greater(self.state.currentComparison.segments[split],self.state.segmentTime):
            return self.config["colours"]["gaining"]
        else:
            return self.config["colours"]["losing"]

    def setPreviousColour(self):
        split = self.state.splitnum-1
        if timeh.isBlank(self.state.comparisons[0].segments[split])\
            or timeh.isBlank(self.state.currentRun.segments[split])\
            or timeh.isBlank(self.state.currentComparison.segments[split]):
            return self.config["colours"]["skipped"]

        if timeh.greater(self.state.comparisons[0].segments[split],self.state.currentRun.segments[split]):
            return self.config["colours"]["gold"]

        elif timeh.greater(self.state.currentComparison.segments[split],self.state.currentRun.segments[split]):
            return self.config["colours"]["gaining"]

        else:
            return self.config["colours"]["losing"]
