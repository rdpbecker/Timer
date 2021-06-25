import tkinter as tk
from Components import ValidationEntry as VE

class LeftFrame(tk.Frame):
    cellWidth = 10
    def __init__(self,parent,comparisons,parentObj):
        super().__init__(parent)
        self.grid = parentObj
        self.currentSplit = -1
        self.frames = []
        self.labels = []
        self.names = []
        for i in range(len(comparisons)):
            self.addRow(comparisons[i][0])

    def splitNames(self):
        return [self.names[i].val for i in range(len(self.names))]

    def onClicked(self,event):
        self.updateCurrentSplit(self.labels.index(event.widget))
        self.grid.splitUpdated()

    def addRow(self,newName):
        label = tk.Label(self,text=len(self.labels)+1)
        label.bind("<Button-1>",self.onClicked)
        label.grid(row=len(self.labels),column=0,sticky="NSWE")
        self.labels.append(label)

        name = VE.Entry(self,newName,{"validate": self.validate},width=self.cellWidth)
        name.grid(row=len(self.names),column=1,sticky="NSEW")
        self.names.append(name)

    def validate(self,val):
        return len(val) > 0 and val.find(",") < 0

    def removeRow(self,index):
        self.names[-1].grid_forget()
        self.labels[-1].grid_forget()
        del self.names[-1]
        del self.labels[-1]

    def updateCurrentSplit(self,new,allowRemoval=True):
        if new == self.currentSplit and allowRemoval:
            new = -1
        for i in range(len(self.labels)):
            if i == new:
                self.labels[i]["bg"] = "blue"
                self.labels[i]["fg"] = "white"
            elif i == self.currentSplit:
                self.labels[i]["bg"] = "#d0d0d0"
                self.labels[i]["fg"] = "black"
        self.currentSplit = new

    def addSplit(self,index):
        self.addRow("")
        self.updateCurrentSplit(index,False)
        if index < 0:
            return

        names = self.splitNames()
        self.names[index].setText("",True)
        for i in range(index+1,len(self.names)):
            self.names[i].setText(names[i-1],True)

    def removeSplit(self):
        if self.currentSplit < 0:
            return
        names = self.splitNames()
        self.removeRow(-1)
        del names[self.currentSplit]
        for i in range(len(names)):
            self.names[i].setText(names[i])
        self.updateCurrentSplit(-1)

    def shouldWarn(self):
        return not all([self.validate(name) for name in self.splitNames()])

    def isValid(self):
        return all([name.isValid() for name in self.names])
