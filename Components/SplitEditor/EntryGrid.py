import tkinter as tk
from Components.SplitEditor import EntryRow
from Components.SplitEditor import HeaderRow
from Components.SplitEditor import LeftFrame
from Components import ScrollableFrame
from DataClasses import SumList
from util import timeHelpers as timeh
from util import dataManip

class EntryGrid(ScrollableFrame.ScrollableFramePin):
    def __init__(self,parent,comparisons):
        super().__init__(parent,width=600,height=300)
        self.leftFrame = LeftFrame.LeftFrame(self.pinnedX(),comparisons[1:])
        self.leftFrame.pack(side="left",fill="both")

        self.rightFrame = tk.Frame(self.main())
        self.rightFrame.pack(side="left",fill="y")
        self.headers = comparisons[0][1:]

        self.cornerLabel = tk.Label(self.corner(),text=comparisons[0][0])
        self.cornerLabel.pack(side="right",fill="both")

        self.rows = []
        self.originals = list(range(len(comparisons)-1))
        for i in range(1,len(comparisons)):
            row = EntryRow.EntryRow(self.rightFrame,self,comparisons[i][1:])
            row.pack(side="top",fill="both")
            self.rows.append(row)

        self.comparisons = []
        for i in range(1,len(comparisons[0]),2):
            self.comparisons.append(SumList.SumList([timeh.stringToTime(comparisons[j][i]) for j in range(1,len(comparisons))]))

    def insertPinnedX(self,*args):
        self.headerRow = HeaderRow.HeaderRow(self.pinnedY(),self.headers)
        self.headerRow.pack(side="top",fill="both")

    def addSplit(self):
        index = self.leftFrame.currentSplit
        if index < 0:
            index = len(self.rows)
        self.leftFrame.addSplit(index)
        newComparisons = []
        for comparison in self.comparisons:
            comparison.insertNewSegment(index)
            newComparisons.extend(['-',timeh.timeToString(comparison.totalBests[index],{"precision":5})])
        self.rows.insert(index,EntryRow.EntryRow(self.rightFrame,self,newComparisons))

        for i in range(index+1,len(self.rows)):
            self.rows[i].pack_forget()
        for i in range(index,len(self.rows)):
            self.rows[i].pack(side="top",fill="both")
        for i in range(len(self.originals)):
            if self.originals[i] >= index:
                self.originals[i] = self.originals[i] + 1

    def removeSplit(self):
        currentSplit = self.leftFrame.currentSplit
        if currentSplit < 0:
            return
        self.leftFrame.removeSplit()
        self.rows[currentSplit].pack_forget()
        del self.rows[currentSplit]
        for comparison in range(len(self.comparisons)):
            self.comparisons[comparison].removeSegment(currentSplit)
            self.updateComparison(comparison,["entry"])

        for i in range(len(self.originals)):
            if self.originals[i] > currentSplit:
                self.originals[i] = self.originals[i] - 1
            elif self.originals[i] == currentSplit:
                self.originals[i] = -1

    def addComparison(self):
        self.headerRow.addHeaders(["New Split","New Comparison"])
        for row in self.rows:
            row.addComparison()
        self.comparisons.append(SumList.SumList([timeh.blank() for row in self.rows]))

    def removeComparison(self):
        if len(self.comparisons) <= 5:
            return
        del self.comparisons[-1]
        self.headerRow.removeHeaders(2)
        for row in self.rows:
            row.removeComparison(1)

    def updateComparisonValue(self,row,comparison,time):
        self.comparisons[comparison].update(timeh.stringToTime(time),self.rows.index(row))
        self.updateComparison(comparison,["label"])

    def updateComparison(self,comparison,columns=[]):
        for i in range(len(self.rows)):
            if "label" in columns:
                self.rows[i].updateLabel(comparison,self.comparisons[comparison].totalBests[i])
            if "entry" in columns:
                self.rows[i].updateEntry(comparison,self.comparisons[comparison].bests[i])

    def generateCsvs(self):
        current = [[] for i in range(len(self.rows))]
        for i in range(len(self.comparisons)):
            dataManip.insertSumList(self.comparisons[i],0,2*i,current,{"precision":5})
        for i in range(len(self.rows)):
            current[i].insert(0,self.leftFrame.splitNames()[i])
        current.insert(0,[self.cornerLabel["text"]] + self.headerRow.headers())
        retVal = {"comparisons": current}
        retVal["names"] = self.leftFrame.splitNames()
        return retVal
