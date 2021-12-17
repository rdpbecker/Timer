from Widgets import WidgetBase
from Components import SegmentRow
from DataClasses import Splits
from util import timeHelpers as timeh

class SegmentArea(WidgetBase.WidgetBase):
    rows = []
    numRows = 0
    activeIndex = 0
    updateFrame = 0

    def __init__(self,parent,state,config):
        super().__init__(parent,state,config)
        self.rows = []
        self.resetUI()

    def resetUI(self):
        self.splits = Splits.SplitList(self.state)
        oldNumSplits = len(self.rows)
        self.splits.setVisualConfig(self.config["numSplits"],self.config["activeSplit"],self.config["setOpenOnEnd"])
        self.splits.updateCurrent(self.state.splitnum)
        self.numRows = self.splits.visibleSplits

        if oldNumSplits < self.numRows:
            for i in range(oldNumSplits,self.numRows):
                row = SegmentRow.SegmentRow(self, self.config["main"]["colours"]["bg"], self.config["main"]["font"], self.config["main"]["colours"]["text"], self.state.config["padx"])
                row.grid(row=i,column=0,columnspan=12,sticky='NSWE')
                self.rowconfigure(i,weight=1)
                self.rows.append(row)
        elif oldNumSplits > self.numRows:
            for i in range(oldNumSplits-1,self.numRows-1,-1):
                self.rows[i].grid_forget()
                self.rows[i].destroy()
                self.rows.pop(-1)

        self.setAllHeaders()
        self.setAllComparisons()
        self.setHighlight()
        self.rows[-1].setHeader(fg=self.config["endColour"])
        self.rows[-1].setComparison(fg=self.config["endColour"])

    def onRestart(self):
        self.splits.updateCurrent(0)
        self.updateFrame = 0
        self.setAllHeaders()
        self.setAllDiffs()
        self.setAllComparisons()
        self.setHighlight()

    def preStart(self):
        # Before the run is started, set the header texts every few
        # frames so that the length is adjusted appropriately. The
        # assumption here is that the user isn't resizing during
        # the run.
        if not self.updateFrame%6:
            self.setAllHeaders()
        self.updateFrame = self.updateFrame + 1

    def frameUpdate(self):
        if not self.state.runEnded\
            and (not timeh.greater(self.state.currentComparison.totals[self.state.splitnum],self.state.totalTime)\
            or not timeh.greater(self.state.comparisons[0].segments[self.state.splitnum],self.state.segmentTime)):

            self.showCurrentSplitDiff()
        if not self.state.runEnded:
            self.updateGroupTimer()

    def onSplit(self):
        self.toNextSplit()

    def onSplitSkipped(self):
        self.toNextSplit()

    def onComparisonChanged(self):
        self.setMainHeaders()
        self.setAllDiffs()
        self.setAllComparisons()

    def toNextSplit(self):
        self.splits.updateCurrent(self.state.splitnum)
        self.setHighlight()
        self.setAllHeaders()
        self.setAllDiffs()
        self.setMainComparisons()
        if self.state.runEnded:
            self.setLastComparison()

    def subAdjuster(self,isSub):
        if not isSub:
            return ""
        return "    "

    def setMainHeaders(self):
        try:
            for i in range(self.numRows-1):
                split = self.splits.currentSplits[i]
                if self.splits.typeChecker.isEmpty(split):
                    self.rows[i].setHeaderText("")
                else:
                    if self.splits.typeChecker.isNormal(split):
                        isSub = split.subsplit
                    else:
                        isSub = False
                    self.rows[i].setHeaderText(self.subAdjuster(isSub)+split.name)
        except:
            pass

    def setLastHeader(self):
        try:
            split = self.splits.currentSplits[-1]
            if self.splits.typeChecker.isNormal(split):
                isSub = split.subsplit
            else:
                isSub = False
            self.rows[-1].setHeaderText(self.subAdjuster(isSub)+self.splits.currentSplits[-1].name)
        except:
            pass

    def setAllHeaders(self):
        self.setMainHeaders()
        self.setLastHeader()

    def formatDiff(self,time):
        return timeh.timeToString(\
            time,\
            {
                "showSign": True,\
                "precision": self.config["diff"]["precision"],\
                "noPrecisionOnMinute": self.config["diff"]["noPrecisionOnMinute"]\
            }\
        ),\

    def setMainDiffs(self):
        for i in range(self.numRows-1):
            split = self.splits.currentSplits[i]
            if self.splits.typeChecker.isEmpty(split):
                self.rows[i].setDiff(text="")
            elif self.splits.typeChecker.isGroup(split):
                if (split.end < self.state.splitnum):
                    if split.start > 0:
                        groupChange = timeh.difference(\
                            timeh.difference(\
                                self.state.currentRun.totals[split.end],\
                                self.state.currentRun.totals[split.start]\
                            ),\
                            timeh.difference(\
                                self.state.currentComparison.totals[split.end],\
                                self.state.currentComparison.totals[split.start]\
                            )\
                        )
                    else:
                        groupChange = timeh.blank()
                    if timeh.isBlank(groupChange):
                        diffColour = self.config["diff"]["colours"]["skipped"]
                    else:
                        diffColour=self.getCurrentDiffColour(\
                            groupChange,\
                            self.state.currentComparison.totalDiffs[split.end]\
                        )
                    self.rows[i].setDiff(\
                        text=self.formatDiff(self.state.currentComparison.totalDiffs[split.end]),\
                        fg=diffColour\
                    )
                else:
                    self.rows[i].setDiff(text="")
            else:
                if (split.index < self.state.splitnum):
                    self.rows[i].setDiff(\
                        text=self.formatDiff(self.state.currentComparison.totalDiffs[split.index]),\
                        fg=self.findDiffColour(split.index)\
                    )
                else:
                    self.rows[i].setDiff(text="")

    def setLastDiff(self):
        if self.state.runEnded:
            self.rows[-1].setDiff(\
                text=\
                    timeh.timeToString(\
                        self.state.currentComparison.totalDiffs[-1],\
                        {\
                            "showSign": True,\
                            "precision": self.config["diff"]["precision"],\
                            "noPrecisionOnMinute": self.config["diff"]["noPrecisionOnMinute"]\
                        }\
                    ),\
                fg=self.findDiffColour(-1)\
            )
        else:
            self.rows[-1].setDiff(text="")

    def setAllDiffs(self):
        self.setMainDiffs()
        self.setLastDiff()

    def formatComparison(self,time):
        return timeh.timeToString(\
            time,\
            {\
                "precision": self.config["main"]["precision"],\
                "noPrecisionOnMinute": self.config["main"]["noPrecisionOnMinute"]\
            }\
       )\

    def updateGroupTimer(self):
        for i in range(len(self.splits.currentSplits)):
            split = self.splits.currentSplits[i]
            if self.splits.typeChecker.isGroup(split) and split.open:
                self.rows[i].setComparison(\
                    text=self.formatComparison(timeh.difference(self.state.totalTime,self.splits.groupStart)),\
                    fg="grey"
                )
                break

    def setMainComparisons(self):
        for i in range(self.numRows-1):
            split = self.splits.currentSplits[i]

            if self.splits.typeChecker.isEmpty(split):
                self.rows[i].setComparison(text="")

            elif self.splits.typeChecker.isGroup(split):
                if (split.end < self.state.splitnum):
                    self.rows[i].setComparison(\
                        text=self.formatComparison(self.state.currentRun.totals[split.end])\
                    )
                else:
                    self.rows[i].setComparison(\
                        text=self.formatComparison(self.state.currentComparison.totals[split.end])\
                    )
            else:
                if (split.index < self.state.splitnum):
                    self.rows[i].setComparison(\
                        text=self.formatComparison(self.state.currentRun.totals[split.index])\
                    )
                else:
                    self.rows[i].setComparison(\
                        text=self.formatComparison(self.state.currentComparison.totals[split.index])\
                    )

    def setLastComparison(self):
        if self.state.runEnded:
            self.rows[-1].setComparison(\
                text=\
                    timeh.timeToString(\
                        self.state.currentRun.totals[-1],\
                        {\
                            "precision": self.config["main"]["precision"],\
                            "noPrecisionOnMinute": self.config["main"]["noPrecisionOnMinute"]\
                        }\
                    )\
            )
        else:
            self.rows[-1].setComparison(\
                text=\
                    timeh.timeToString(\
                        self.state.currentComparison.totals[-1],\
                        {\
                            "precision": self.config["main"]["precision"],\
                            "noPrecisionOnMinute": self.config["main"]["noPrecisionOnMinute"]\
                        }\
                    )\
            )

    def setAllComparisons(self):
        self.setMainComparisons()
        self.setLastComparison()

    def showCurrentSplitDiff(self):
        self.rows[self.splits.activeIndex].setDiff(\
            text=timeh.timeToString(\
                timeh.difference(self.state.totalTime,self.state.currentComparison.totals[self.state.splitnum]),\
                {\
                    "showSign": True,\
                    "precision": self.config["diff"]["precision"],\
                    "noPrecisionOnMinute": self.config["diff"]["noPrecisionOnMinute"]\
                }\
            ),\
            fg=self.getCurrentDiffColour(\
                timeh.difference(self.state.segmentTime,self.state.currentComparison.segments[self.state.splitnum]), \
                timeh.difference(self.state.totalTime,self.state.currentComparison.totals[self.state.splitnum])\
            )\
        )

    def getCurrentDiffColour(self,segmentDiff,totalDiff):
        if timeh.greater(0,totalDiff):
            # if comparison segment is blank or current segment is
            # ahead
            if timeh.greater(0,segmentDiff):
                return self.config["diff"]["colours"]["aheadGaining"]
            else:
                return self.config["diff"]["colours"]["aheadLosing"]
        else:
            # if comparison segment is blank or current segment is
            # behind
            if timeh.greater(segmentDiff,0):
                return self.config["diff"]["colours"]["behindLosing"]
            else:
                return self.config["diff"]["colours"]["behindGaining"]

    def findDiffColour(self,splitIndex):
        # Either the split in this run is blank, or we're comparing
        # to something that's blank
        if \
            timeh.isBlank(self.state.currentRun.totals[splitIndex]) \
            or timeh.isBlank(self.state.currentComparison.totals[splitIndex]):
            return self.config["diff"]["colours"]["skipped"]
        # This split is the best ever. Mark it with the gold colour
        elif not timeh.isBlank(self.state.comparisons[0].segmentDiffs[splitIndex]) \
            and timeh.greater(0,self.state.comparisons[0].segmentDiffs[splitIndex]):
            return self.config["diff"]["colours"]["gold"]
        else:
            return self.getCurrentDiffColour(\
                self.state.currentComparison.segmentDiffs[splitIndex],\
                self.state.currentComparison.totalDiffs[splitIndex]\
            )

    def setHighlight(self):
        for i in range(self.numRows):
            self.setBackground(i)
            self.setTextColour(i)

    def setBackground(self,index):
        if(index == self.splits.activeIndex):
            colour = self.config["activeHighlight"]["colours"]["bg"]
        else:
            colour = self.config["main"]["colours"]["bg"]
        if self.splits.typeChecker.isGroup(self.splits.currentSplits[index]) and self.splits.currentSplits[index].open:
            relief = "sunken"
            borderwidth = 1
        else:
            relief = "flat"
            borderwidth = 0
        self.rows[index].configure(bg=colour,borderwidth=borderwidth,relief=relief)
        self.rows[index].setHeader(bg=colour)
        self.rows[index].setDiff(bg=colour)
        self.rows[index].setComparison(bg=colour)

    def setTextColour(self,index):
        if(index == self.splits.activeIndex):
            colour = self.config["activeHighlight"]["colours"]["text"]
        elif index < self.numRows-1:
            colour = self.config["main"]["colours"]["text"]
        else:
            colour = self.config["endColour"]
        self.rows[index].setHeader(fg=colour)
        self.rows[index].setComparison(fg=colour)
