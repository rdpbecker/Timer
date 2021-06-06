import tkinter as tk
import copy
from DataClasses import AllSplitNames
from Dialogs import Popup
from Components import ScrollableFrame
from Components import SaveButton
from Components import ValidationEntry as VE
from DataClasses import SumList
from util import timeHelpers as timeh
from util import fileio
from util import dataManip

class SplitEditor(Popup.Popup):
    def __init__(self,master,callback,state):
        super().__init__(master,callback)
        self.localComparisons = copy.deepcopy(state.comparesCsv)
        self.state = state
        self.splits = AllSplitNames.Splits()

        self.entries = EntryGrid(self.window,self.localComparisons)
        self.entries.pack(side="left")

        self.deleteSplitButton = tk.Button(self.window, text="Delete Split", command=self.deleteSplit)
        self.deleteSplitButton.pack()

        self.saveButton = SaveButton.SaveButton(self.window, {"callback": self.save})
        self.saveButton.pack(side="bottom")

    def deleteSplit(self,event=None):
        self.entries.removeSplit()

    def save(self,retVal):
        csvs = self.entries.generateCsvs()
        csvs["complete"] = dataManip.adjustNames(csvs["names"],self.state.completeCsv)
        fileio.writeCSVs(self.state.config["baseDir"],self.state.game,self.state.category,csvs["complete"],csvs["comparisons"])
        self.splits.updateNames(self.state.game,self.state.category,csvs["names"])

class EntryGrid(ScrollableFrame.ScrollableFrame):
    def __init__(self,parent,comparisons):
        super().__init__(parent,width=600,height=300)
        self.leftFrame = LeftFrame(self.scrollable_frame,comparisons)
        self.leftFrame.pack(side="left",fill="both")

        self.rightFrame = tk.Frame(self.scrollable_frame)
        self.rightFrame.pack(side="left",fill="y")

        self.headerRow = HeaderRow(self.rightFrame,comparisons[0][1:])
        self.headerRow.pack(side="top",fill="both")

        self.rows = []
        for i in range(1,len(comparisons)):
            row = EntryRow(self.rightFrame,self,comparisons[i][1:],i-1)
            row.pack(side="top",fill="both")
            self.rows.append(row)

        self.comparisons = []
        for i in range(1,len(comparisons[0]),2):
            self.comparisons.append(SumList.SumList([timeh.stringToTime(comparisons[j][i]) for j in range(1,len(comparisons))]))

    def removeSplit(self):
        currentSplit = self.leftFrame.currentSplit
        self.leftFrame.removeSplit()
        self.rows[currentSplit-1].pack_forget()
        del self.rows[currentSplit-1]
        for comparison in range(len(self.comparisons)):
            self.comparisons[comparison].removeSegment(currentSplit-1)
            self.updateComparison(comparison,["entry"])

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
        current.insert(0,[self.leftFrame.cornerName()] + self.headerRow.headers())
        retVal = {"comparisons": current}
        retVal["names"] = self.leftFrame.splitNames()
        return retVal

class LeftFrame(tk.Frame):
    cellWidth = 10
    def __init__(self,parent,comparisons):
        super().__init__(parent)
        self.currentSplit = -1
        self.frames = []
        self.labels = []
        self.names = []
        for i in range(len(comparisons)):
            if i:
                label = tk.Label(self,text=str(i))
                label.bind("<Button-1>",self.onClicked)
            else:
                label = tk.Label(self)
            label.grid(row=i,column=0,sticky="NSWE")

            name = VE.Entry(self,comparisons[i][0],{"validate":lambda val: val.find(",") < 0},width=self.cellWidth)
            name.grid(row=i,column=1,sticky="NSEW")

            self.labels.append(label)
            self.names.append(name)

    def cornerName(self):
        return self.names[0].val

    def splitNames(self):
        return [self.names[i].val for i in range(1,len(self.names))]

    def onClicked(self,event):
        self.updateCurrentSplit(self.labels.index(event.widget))

    def updateCurrentSplit(self,new):
        if new == self.currentSplit:
            return
        for i in range(len(self.labels)):
            if i == new:
                self.labels[i]["bg"] = "blue"
                self.labels[i]["fg"] = "white"
            elif i == self.currentSplit:
                self.labels[i]["bg"] = "#d0d0d0"
                self.labels[i]["fg"] = "black"
        self.currentSplit = new

    def removeSplit(self):
        if self.currentSplit <= 0:
            return
        names = self.splitNames()
        self.names[-1].grid_forget()
        self.labels[-1].grid_forget()
        del names[self.currentSplit-1]
        del self.names[-1]
        del self.labels[-1]
        for i in range(len(names)):
            self.names[i+1].setText(names[i])
        self.updateCurrentSplit(-1)

class HeaderRow(tk.Frame):
    cellWidth = 10
    def __init__(self,parent,headerRow):
        super().__init__(parent)
        self.entries = []
        for i in range(len(headerRow)):
            if not i in [8,9]:
                entry = VE.Entry(self,headerRow[i],{"validate": lambda name: name.find(",") < 0},width=self.cellWidth)
            else:
                entry = tk.Label(self,text=headerRow[i],width=self.cellWidth)
            entry.pack(side="left")
            self.entries.append(entry)

    def headers(self):
        return\
            [self.entries[i].val for i in range(8)]\
            + [self.entries[8],self.entries[9]]\
            + [self.entries[i].val for i in range(10,len(self.entries))]

class EntryRow(tk.Frame):
    cellWidth = 10
    def __init__(self,parent,parentObj,comparisonsRow,index):
        super().__init__(parent)
        self.parent = parentObj
        self.comparisonsRow = comparisonsRow
        for i in range(len(comparisonsRow)):
            self.columnconfigure(i,weight=1)

        self.pairs = []
        for i in range(0,len(comparisonsRow),2):
            if not self.comparisonIndex(i) == 4:
                timevar = tk.StringVar(self,f'{timeh.trimTime(comparisonsRow[i])}')
                pair = [\
                    VE.Entry(\
                        self,\
                        timeh.trimTime(comparisonsRow[i]),\
                        {\
                            "validate": lambda time: timeh.validTime(time),\
                            "followup": lambda time, timeIndex=i: self.parent.updateComparisonValue(self,timeIndex,time)\
                        },\
                        width=self.cellWidth,justify="right"),\
                    tk.Label(self,text=f'{timeh.trimTime(comparisonsRow[i+1])}',width=self.cellWidth,anchor="e")
                ]
            else:
                pair = [\
                    tk.Label(self,text=f'{timeh.trimTime(comparisonsRow[i])}',width=self.cellWidth,anchor="e"),\
                    tk.Label(self,text=f'{timeh.trimTime(comparisonsRow[i+1])}',width=self.cellWidth,anchor="e")\
                ]
            pair[0].grid(row=0,column=i)
            pair[1].grid(row=0,column=i+1)
            self.pairs.append(pair)

    def updateEntry(self,index,time):
        if not index == 4:
            self.pairs[index][0].setText(timeh.timeToString(time,{"precision":2}))

    def updateLabel(self,index,time):
        self.pairs[index][1]["text"] = timeh.timeToString(time,{"precision":2})

    def columnIndex(self,index):
        return 2*index

    def comparisonIndex(self,index):
        return int(index/2)
