import tkinter as tk
from Widgets import Info
from util import timeHelpers as timeh

class GoldDiffInfo(Info.Info):
    def __init__(self,parent,state,config):
        Info.Info.__init__(self,parent,state,config)
        self.header.configure(text="Last Split (vs Best):")

    def hide(self):
        self.info.configure(text="-",fg=self.config["colours"]["text"])

    def frameUpdate(self):
        if self.state.runEnded:
            return
        if self.state.splitnum and self.shouldHide():
            self.hide()
            return
        if not timeh.greater(self.state.comparisons[0].segments[self.state.splitnum],self.state.segmentTime)\
            and not timeh.isBlank(self.state.comparisons[0].segments[self.state.splitnum])\
            and not (self.state.splitnum and timeh.isBlank(self.state.currentRun.segments[self.state.splitnum-1])):

            if self.state.splitnum and self.shouldHide():
                self.hide()
                return

            self.header.configure(text="Current Segment:")
            self.setTimes(self.state.segmentTime,previous=False)

    def onSplit(self):
        self.splitEndUpdate()

    def onSplitSkipped(self):
        self.splitEndUpdate()

    def onComparisonChanged(self):
        if self.state.splitnum:
            if self.shouldHide():
                self.hide()
                return
            self.setTimes(self.state.currentRun.segments[self.state.splitnum-1])

    def onRestart(self):
        self.resetUI()

    def resetUI(self):
        self.header.configure(text="Last Split (vs Best):")
        self.info.configure(text="")

    def splitEndUpdate(self):
        if not self.state.splitnum:
            return
        self.header.configure(text="Last Split (vs Best):")
        if self.shouldHide():
            self.hide()
            return
        self.setTimes(self.state.currentRun.segments[self.state.splitnum-1])

    def setTimes(self,time,previous=True):
        if previous:
            splitnum = self.state.splitnum - 1
        else:
            splitnum = self.state.splitnum
        self.info.configure(text=\
            timeh.timeToString(\
                timeh.difference(\
                    time,\
                    self.state.comparisons[0].segments[splitnum]\
                ),\
                {\
                    "showSign": True,\
                    "precision": self.config["precision"],\
                    "noPrecisionOnMinute": self.config["noPrecisionOnMinute"]\
                }\
                )\
        )
        if previous:
            self.info.configure(fg=self.setPreviousColour())
        else:
            self.info.configure(fg=self.setCurrentColour())

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
