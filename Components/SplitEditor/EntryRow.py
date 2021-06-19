import tkinter as tk
from Components import ValidationEntry as VE
from util import timeHelpers as timeh

class EntryRow(tk.Frame):
    cellWidth = 10
    def __init__(self,parent,parentObj,comparisonsRow):
        super().__init__(parent)
        self.parent = parentObj
        for i in range(len(comparisonsRow)):
            self.columnconfigure(i,weight=1)

        self.pairs = []
        for i in range(0,len(comparisonsRow),2):
            if not self.comparisonIndex(i) == 4:
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

    def shouldWarn(self):
        return not all([self.pairs[i][0].isValid() for i in filter(lambda x: not x == 4, range(len(self.pairs)))])

    def updateEntry(self,index,time):
        if not index == 4:
            self.pairs[index][0].setText(timeh.timeToString(time,{"precision":2}))

    def addComparison(self):
        pair = [\
            VE.Entry(\
                self,\
                '-',\
                {\
                    "validate": lambda time: timeh.validTime(time),\
                    "followup": lambda time, timeIndex=len(self.pairs): self.parent.updateComparisonValue(self,timeIndex,time)\
                },\
                width=self.cellWidth,justify="right"),\
            tk.Label(self,text='-',width=self.cellWidth,anchor="e")
        ]
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
