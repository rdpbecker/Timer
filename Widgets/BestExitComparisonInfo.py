import tkinter as tk
from Widgets import InfoBase
from util import timeHelpers as timeh

class BestExitComparisonInfo(InfoBase.InfoBase):
    def __init__(self,parent,state,config):
        InfoBase.InfoBase.__init__(self,parent,state,config)
        self.resetUI()

    def hide(self):
        self.info.configure(text="-",fg=self.config["colours"]["text"])

    def frameUpdate(self):
        if self.state.runEnded:
            return
        if self.state.splitnum and self.shouldHide():
            self.hide()
            return
        if (not timeh.greater(self.state.comparisons[0].segments[self.state.splitnum],self.state.segmentTime)\
            and not timeh.isBlank(self.state.comparisons[0].segments[self.state.splitnum]))\
            or (not timeh.greater(self.state.comparisons[3].totals[self.state.splitnum],self.state.totalTime)\
            and not timeh.isBlank(self.state.comparisons[3].totals[self.state.splitnum]))\
            and not (self.state.splitnum and timeh.isBlank(self.state.currentRun.totals[self.state.splitnum-1])):

            if self.shouldHide():
                self.hide()
                return

            self.setTimes(self.state.totalTime,previous=False)

    def onSplit(self):
        self.splitEndUpdate()

    def onSplitSkipped(self):
        self.splitEndUpdate()

    def onComparisonChanged(self):
        if self.state.splitnum:
            if self.shouldHide():
                self.hide()
                return
            self.setTimes(self.state.currentRun.totals[self.state.splitnum-1])

    def onRestart(self):
        self.resetUI()

    def resetUI(self):
        self.header.configure(text="Vs Best Exit:")
        self.info.configure(text="")

    def splitEndUpdate(self):
        if not self.state.splitnum:
            return
        if self.shouldHide():
            self.hide()
            return
        self.header.configure(text="Vs Best Exit:")
        self.setTimes(self.state.currentRun.totals[self.state.splitnum-1])

    def setTimes(self,time,previous=True):
        if previous:
            splitnum = self.state.splitnum - 1
        else:
            splitnum = self.state.splitnum
        self.info.configure(text=\
            timeh.timeToString(\
                timeh.difference(\
                    time,\
                    self.state.comparisons[3].totals[splitnum]\
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

        else:
            return self.setColour(self.state.segmentTime,self.state.totalTime,split)

    def setPreviousColour(self):
        split = self.state.splitnum-1
        if timeh.isBlank(self.state.comparisons[3].totals[split])\
            or timeh.isBlank(self.state.currentRun.totals[split])\
            or timeh.isBlank(self.state.currentComparison.totals[split]):
            return self.config["colours"]["skipped"]

        if timeh.greater(self.state.comparisons[3].totals[split],self.state.currentRun.totals[split]):
            return self.config["colours"]["gold"]
        else:
            return self.setColour(self.state.currentRun.segments[split],self.state.currentRun.totals[split],split)

    def setColour(self,segment,total,split):
        if timeh.greater(self.state.comparisons[3].totals[split],total):

            if timeh.greater(self.state.comparisons[3].segments[split],segment):
                return self.config["colours"]["aheadGaining"]

            else:
                return self.config["colours"]["aheadLosing"]

        else:
            if timeh.greater(self.state.comparisons[3].segments[split],segment):
                return self.config["colours"]["behindGaining"]

            else:
                return self.config["colours"]["behindLosing"]
