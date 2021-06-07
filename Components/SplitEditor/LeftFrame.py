import tkinter as tk
from Components import ValidationEntry as VE

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
                self.labels.append(label)
            else:
                label = tk.Label(self)
            label.grid(row=i,column=0,sticky="NSWE")

            name = VE.Entry(self,comparisons[i][0],{"validate":lambda val: val.find(",") < 0},width=self.cellWidth)
            name.grid(row=i,column=1,sticky="NSEW")
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

    def addSplit(self,index):
        label = tk.Label(self,text=len(self.labels)+1)
        label.bind("<Button-1>",self.onClicked)
        label.grid(row=len(self.labels)+1,column=0,sticky="NSWE")
        self.labels.append(label)

        name = VE.Entry(self,"",{"validate":lambda val: val.find(",") < 0},width=self.cellWidth)
        name.grid(row=len(self.names),column=1,sticky="NSEW")
        self.names.append(name)

        if index < 0:
            self.updateCurrentSplit(len(self.names))
            return

        names = self.splitNames()
        self.names[index+1].setText("")
        for i in range(index+2,len(self.names)):
            self.names[i].setText(names[i-2])
        self.updateCurrentSplit(index)

    def removeSplit(self):
        if self.currentSplit < 0:
            return
        names = self.splitNames()
        self.names[-1].grid_forget()
        self.labels[-1].grid_forget()
        del names[self.currentSplit]
        del self.names[-1]
        del self.labels[-1]
        for i in range(len(names)):
            self.names[i+1].setText(names[i])
        self.updateCurrentSplit(-1)
