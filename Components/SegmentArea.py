import tkinter as tk
from Components import Component
from Components import SegmentRow
import timeHelpers as timeh

class SegmentArea(Component.Component):
    rows = []
    topRowSplitnum = 0
    activeIndex = 0

    def __init__(self,parent,state):
        Component.Component.__init__(self,parent,state)
        self.numRows = state.config["numSplits"]
        for i in range(self.numRows):
            row = SegmentRow.SegmentRow(self, state.config["root"]["colours"]["bg"], state.config["root"]["font"], state.config["root"]["colours"]["text"])
            row.grid(row=i,column=0,columnspan=12,sticky='NSWE')
            self.rows.append(row)
        self.setAllHeaders()
        self.setAllComparisons()
        self.setHighlight()
        self.rows[-1].setHeader(fg=state.config["endColour"])
        self.rows[-1].setComparison(fg=state.config["endColour"])

    def frameUpdate(self):
        if not self.state.runEnded\
            and (not timeh.greater(self.state.currentComparison.totals[self.state.splitnum],self.state.totalTime)\
            or not timeh.greater(self.state.comparisons[0].segments[self.state.splitnum],self.state.segmentTime)):

            self.showCurrentSplitDiff()

    def onSplit(self):
        self.toNextSplit()

    def onSplitSkipped(self):
        self.toNextSplit()

    def onComparisonChanged(self):
        self.setMainHeaders()
        self.setAllDiffs()
        self.setAllComparisons()

    def getTopSplitIndex(self):
        if self.state.splitnum <= self.state.config["activeSplit"] - 1:
            return 0
        if self.state.splitnum >= self.state.numSplits - (self.state.config["numSplits"]-self.state.config["activeSplit"]):
            return self.state.numSplits - self.state.config["numSplits"]
        return self.state.splitnum - (self.state.config["activeSplit"] - 1)

    def toNextSplit(self):
        self.topRowSplitnum = self.getTopSplitIndex()
        if not (self.state.splitnum - self.topRowSplitnum == self.activeIndex):
            self.activeIndex = self.state.splitnum - self.topRowSplitnum
            self.setHighlight()
        self.setMainHeaders()
        self.setAllDiffs()
        self.setMainComparisons()

    def setMainHeaders(self):
        for i in range(self.numRows-1):
            self.rows[i].setHeader(text=self.state.splitnames[i+self.topRowSplitnum])

    def setLastHeader(self):
        self.rows[-1].setHeader(text=self.state.splitnames[-1])

    def setAllHeaders(self):
        self.setMainHeaders()
        self.setLastHeader()

    def setMainDiffs(self):
        for i in range(self.numRows-1):
            if (i+self.topRowSplitnum < self.state.splitnum):
                self.rows[i].setDiff(\
                    text=timeh.timeToString(self.state.currentComparison.totalDiffs[i+self.topRowSplitnum],{"showSign":True,"precision":2}),\
                    fg=self.findDiffColour(i+self.topRowSplitnum)\
                )
            else:
                self.rows[i].setDiff(text="")

    def setLastDiff(self):
        if self.state.runEnded:
            self.rows[-1].setDiff(\
                text=timeh.timeToString(self.state.currentComparison.totalDiffs[-1],{"showSign":True,"precision":2}),\
                fg=self.findDiffColour(-1)\
            )
        else:
            self.rows[-1].setDiff(text="")

    def setAllDiffs(self):
        self.setMainDiffs()
        self.setLastDiff()

    def setMainComparisons(self):
        for i in range(self.numRows-1):
            if (i+self.topRowSplitnum < self.state.splitnum):
                self.rows[i].setComparison(\
                    text=timeh.timeToString(self.state.currentRun.totals[i+self.topRowSplitnum],{"precision":2})\
                )
            else:
                self.rows[i].setComparison(\
                    text=timeh.timeToString(self.state.currentComparison.totals[i+self.topRowSplitnum],{"precision":2})\
                )

    def setLastComparison(self):
        if self.state.runEnded:
            self.rows[-1].setComparison(text=timeh.timeToString(self.state.currentRun.totals[-1],{"precision":2}))
        else:
            self.rows[-1].setComparison(text=timeh.timeToString(self.state.currentComparison.totals[-1],{"precision":2}))

    def setAllComparisons(self):
        self.setMainComparisons()
        self.setLastComparison()

    def showCurrentSplitDiff(self):
        self.rows[self.activeIndex].setDiff(\
            text=timeh.timeToString(\
                timeh.difference(self.state.totalTime,self.state.currentComparison.totals[self.state.splitnum]),\
                {"showSign":True,"precision": 2}\
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
                return self.state.config["diff"]["colours"]["aheadGaining"]
            else:
                return self.state.config["diff"]["colours"]["aheadLosing"]
        else:
            # if comparison segment is blank or current segment is
            # behind
            if timeh.greater(segmentDiff,0):
                return self.state.config["diff"]["colours"]["behindLosing"]
            else:
                return self.state.config["diff"]["colours"]["behindGaining"]

    def findDiffColour(self,splitIndex):
        # Either the split in this run is blank, or we're comparing
        # to something that's blank
        if \
            timeh.isBlank(self.state.currentRun.totals[splitIndex]) \
            or timeh.isBlank(self.state.currentComparison.totals[splitIndex]):
            return self.state.config["diff"]["colours"]["skipped"]
        # This split is the best ever. Mark it with the gold colour
        elif not timeh.isBlank(self.state.comparisons[0].segmentDiffs[splitIndex]) \
            and timeh.greater(0,self.state.comparisons[0].segmentDiffs[splitIndex]):
            return self.state.config["diff"]["colours"]["gold"]
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
        if(index == self.activeIndex):
            colour = self.state.config["activeHighlight"]["colours"]["bg"]
        else:
            colour = self.state.config["root"]["colours"]["bg"]
        self.rows[index].configure(bg=colour)
        self.rows[index].setHeader(bg=colour)
        self.rows[index].setDiff(bg=colour)
        self.rows[index].setComparison(bg=colour)

    def setTextColour(self,index):
        if(index == self.activeIndex):
            colour = self.state.config["activeHighlight"]["colours"]["text"]
        elif index < self.numRows-1:
            colour = self.state.config["root"]["colours"]["text"]
        else:
            colour = self.state.config["endColour"]
        self.rows[index].setHeader(fg=colour)
        self.rows[index].setComparison(fg=colour)
