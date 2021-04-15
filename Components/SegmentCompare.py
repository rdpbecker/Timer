import tkinter as tk
from Components import Component

class SegmentCompare(Component.Component):
    segmentHeader = None
    segmentTime = None
    goldHeader = None
    goldTime = None

    def __init__(self,parent,state):
        Component.Component.__init__(self,parent,state)
        self.configure(bg=state.config["root"]["colours"]["bg"])
        self.segmentHeader = tk.Label(self, \
            text=state.currentComparison.segmentHeader + ":",\
            fg=state.config["root"]["colours"]["text"],\
            bg=state.config["root"]["colours"]["bg"]
        )
        self.segmentTime = tk.Label(self, \
            text=self.state.currentComparison.getString("segments",self.state.splitnum,{"precision":2}),\
            fg=state.config["root"]["colours"]["text"],\
            bg=state.config["root"]["colours"]["bg"]
        )
        self.goldHeader = tk.Label(self, \
            text="Best Split:",\
            fg=state.config["root"]["colours"]["text"],\
            bg=state.config["root"]["colours"]["bg"]
        )
        self.goldTime = tk.Label(self, \
            text=self.state.comparisons[0].getString("segments",self.state.splitnum,{"precision":2}),\
            fg=state.config["root"]["colours"]["text"],\
            bg=state.config["root"]["colours"]["bg"]
        )
        self.segmentHeader.grid(row=0,column=0,columnspan=1,sticky='W',ipadx=state.config["padx"])
        self.segmentTime.grid(row=0,column=1,columnspan=11,sticky='W')
        self.goldHeader.grid(row=1,column=0,columnspan=1,sticky='W',ipadx=state.config["padx"])
        self.goldTime.grid(row=1,column=1,columnspan=11,sticky='W')

    def onSplit(self):
        if not self.state.runEnded:
            self.updateSegmentTime()
            self.updateGoldTime()

    def onSplitSkipped(self):
        if not self.state.runEnded:
            self.updateSegmentTime()
            self.updateGoldTime()

    def onComparisonChanged(self):
        if not self.state.runEnded:
            self.updateSegmentHeader()
            self.updateSegmentTime()

    def updateSegmentHeader(self):
        self.segmentHeader.configure(text=self.state.currentComparison.segmentHeader+":")

    def updateSegmentTime(self):
        self.segmentTime.configure(text=self.state.currentComparison.getString("segments",self.state.splitnum,{"precision":2}))

    def updateGoldTime(self):
        self.goldTime.configure(text=self.state.comparisons[0].getString("segments",self.state.splitnum,{"precision":2}))
