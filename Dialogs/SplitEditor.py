import tkinter as tk
import copy
from Dialogs import Popup
from Components import ScrollableFrame
from DataClasses import SumList
from util import timeHelpers as timeh

class SplitEditor(Popup.Popup):
    def __init__(self,master,callback,state):
        super().__init__(master,callback)
        self.localComparisons = copy.deepcopy(state.comparesCsv)

        self.entries = EntryGrid(self.window,self.localComparisons)
        self.entries.pack(side="left")

class EntryGrid(ScrollableFrame.ScrollableFrame):
    def __init__(self,parent,comparisons):
        super().__init__(parent,width=600,height=300)
        self.headerRow = HeaderRow(self.scrollable_frame,comparisons[0])
        self.headerRow.grid(row=0,column=0,sticky="NSEW")
        self.rows = []
        for i in range(1,len(comparisons)):
            row = EntryRow(self.scrollable_frame,self,comparisons[i],i-1)
            row.grid(row=i,column=0,sticky="NSEW")
            self.rows.append(row)
        self.comparisons = []
        for i in range(1,len(comparisons[0]),2):
            self.comparisons.append(SumList.SumList([timeh.stringToTime(comparisons[j][i]) for j in range(1,len(comparisons))]))

    def updateComparison(self,splitIndex,comparison,time):
        self.comparisons[comparison].update(timeh.stringToTime(time),splitIndex)
        for i in range(len(self.rows)):
            self.rows[i].updateLabel(comparison,self.comparisons[comparison].totalBests[i])

class HeaderRow(tk.Frame):
    cellWidth = 10
    def __init__(self,parent,headerRow):
        super().__init__(parent)
        self.entries = []
        self.entryvars = []
        for i in range(len(headerRow)):
            entryvar = tk.StringVar(self,headerRow[i])
            entry = tk.Entry(self,textvariable=entryvar,width=self.cellWidth)
            entry.pack(side="left")
            self.entries.append(entry)
            self.entryvars.append(entryvar)

class EntryRow(tk.Frame):
    cellWidth = 10
    def __init__(self,parent,parentObj,comparisonsRow,index):
        super().__init__(parent)
        self.parent = parentObj
        self.comparisonsRow = comparisonsRow
        self.index = index
        for i in range(len(comparisonsRow)):
            self.columnconfigure(i,weight=1)

        self.namevar = tk.StringVar(self,f'{comparisonsRow[0]}')
        self.name = tk.Entry(self,textvariable=self.namevar,width=self.cellWidth)
        self.name.grid(row=0,column=0)

        self.pairs = []
        self.timevars = []
        for i in range(1,len(comparisonsRow),2):
            timevar = tk.StringVar(self,f'{timeh.trimTime(comparisonsRow[i])}')
            timevar.trace('w',lambda *args, timeIndex=self.comparisonIndex(i): self.validateTime(timeIndex))
            pair = [tk.Entry(self,textvariable=timevar,width=self.cellWidth,justify="right"),tk.Label(self,text=f'{timeh.trimTime(comparisonsRow[i+1])}',width=self.cellWidth,anchor="e")]
            pair[0].grid(row=0,column=i)
            pair[1].grid(row=0,column=i+1)
            self.pairs.append(pair)
            self.timevars.append(timevar)

    def updateLabel(self,index,time):
        self.pairs[index][1]["text"] = timeh.timeToString(time,{"precision":2})

    def validateTime(self,index):
        time = self.timevars[index].get()
        if timeh.validTime(time):
            self.pairs[index][0]["bg"] = "white"
            self.parent.updateComparison(self.index,index,time)
        else:
            self.pairs[index][0]["bg"] = "#ff6666"

    def columnIndex(self,index):
        return 2*index + 1

    def comparisonIndex(self,index):
        return int((index - 1)/2)
