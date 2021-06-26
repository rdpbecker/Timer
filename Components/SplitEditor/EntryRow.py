import tkinter as tk
from Components import ValidationEntry as VE
from util import timeHelpers as timeh

class EntryRow(tk.Frame):
    cellWidth = 10
    blankIndex = 4
    def __init__(self,parent,parentObj,comparisonsRow):
        super().__init__(parent)
        self.parent = parentObj
        for i in range(len(comparisonsRow)):
            self.columnconfigure(i,weight=1)

        self.pairs = []
        for i in range(0,len(comparisonsRow),2):
            if not self.comparisonIndex(i) == self.blankIndex:
                pair = self.generalPair(i,comparisonsRow[i:i+2])
            else:
                pair = self.blankPair(comparisonsRow[i:i+2])
            pair[0].grid(row=0,column=i)
            pair[1].grid(row=0,column=i+1)
            self.pairs.append(pair)

    def generalPair(self,index,times):
        return [\
            VE.Entry(\
                self,\
                timeh.trimTime(times[0]),\
                {\
                    "validate": lambda time: timeh.validTime(time),\
                    "followup": lambda time, timeIndex=index: self.parent.updateComparisonValue(self,timeIndex,time)\
                },\
                width=self.cellWidth,justify="right"),\
            tk.Label(self,text=timeh.trimTime(times[1]),width=self.cellWidth,anchor="e")
        ]

    def blankPair(self,times):
        return [\
            tk.Label(self,text=timeh.trimTime(times[0]),width=self.cellWidth,anchor="e"),\
            tk.Label(self,text=timeh.trimTime(times[1]),width=self.cellWidth,anchor="e")\
        ]

    def shouldWarn(self):
        return not all([self.pairs[i][0].isValid() for i in filter(lambda x: not x == self.blankIndex, range(len(self.pairs)))])

    def updateEntry(self,index,time):
        if not index == self.blankIndex:
            self.pairs[index][0].setText(timeh.timeToString(time,{"precision":2}))

    def addComparison(self):
        pair = self.generalPair(len(self.pairs),['-','-'])
        i = self.columnIndex(len(self.pairs))
        pair[0].grid(row=0,column=i)
        pair[1].grid(row=0,column=i+1)
        self.pairs.append(pair)

    def removeComparison(self,num):
        for i in range(num):
            self.pairs[-1][0].grid_forget()
            self.pairs[-1][1].grid_forget()
            del self.pairs[-1]
        
    def updateLabel(self,index,time):
        self.pairs[index][1]["text"] = timeh.timeToString(time,{"precision":2})

    def columnIndex(self,index):
        return 2*index

    def comparisonIndex(self,index):
        return int(index/2)
