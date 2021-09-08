from Widgets import InfoBase
from util import timeHelpers as timeh

class ComparisonDiffInfo(InfoBase.InfoBase):
    def __init__(self,parent,state,config):
        super().__init__(parent,state,config)
        self.resetUI()

    def hide(self):
        self.info.configure(text="- / -",fg=self.config["colours"]["text"])

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

            self.header.configure(text="Current Split:")
            self.setTimes(self.state.segmentTime,False)

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
        self.header.configure(text="Last Split (Current/Best):")
        self.info.configure(text="")

    def splitEndUpdate(self):
        if not self.state.splitnum:
            return
        if self.shouldHide():
            self.hide()
            return
        self.header.configure(text="Last Split (Current/Best):")
        self.setTimes(self.state.currentRun.segments[self.state.splitnum-1])

    def setTimes(self,time,previous=True):
        if previous:
            splitnum = self.state.splitnum - 1
        else:
            splitnum = self.state.splitnum
        self.info.configure(text=\
            timeh.timeToString(\
                timeh.difference(
                    time,\
                    self.state.currentComparison.segments[splitnum]\
                ),\
                {\
                    "showSign": True, \
                    "precision": self.config["precision"],\
                    "noPrecisionOnMinute": self.config["noPrecisionOnMinute"]\
                }\
            )\
            +" / "\
            +timeh.timeToString(\
                timeh.difference(\
                    self.state.currentComparison.segments[splitnum],\
                    self.state.comparisons[0].segments[splitnum]\
                ),\
                {\
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
