import tkinter as tk
import copy
from Dialogs import Popup
from Components import ScrollableFrame
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
            row = EntryRow(self.scrollable_frame,comparisons[i])
            row.grid(row=i,column=0,sticky="NSEW")
            self.rows.append(row)

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
    def __init__(self,parent,comparisonsRow):
        super().__init__(parent)
        self.comparisonsRow = comparisonsRow
        for i in range(len(comparisonsRow)):
            self.columnconfigure(i,weight=1)

        self.namevar = tk.StringVar(self,f'{comparisonsRow[0]}')
        self.name = tk.Entry(self,textvariable=self.namevar,width=self.cellWidth)
        self.name.grid(row=0,column=0)

        self.pairs = []
        self.timevars = []
        for i in range(1,len(comparisonsRow),2):
            timevar = tk.StringVar(self,f'{timeh.trimTime(comparisonsRow[i])}')
            pair = [tk.Entry(self,textvariable=timevar,width=self.cellWidth,justify="right"),tk.Label(self,text=f'{timeh.trimTime(comparisonsRow[i+1])}',width=self.cellWidth,anchor="e")]
            pair[0].grid(row=0,column=i)
            pair[1].grid(row=0,column=i+1)
            self.pairs.append(pair)
            self.timevars.append(timevar)
