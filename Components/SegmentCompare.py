import tkinter as tk
from Components import Component

class SegmentCompare(Component.Component):
    segmentHeader = None
    segmentTime = None
    goldHeader = None
    goldTime = None

    def __init__(self,parent,state):
        Component.Component.__init__(self,parent,state)
        fg = state.config["root"]["colours"]["text"]
        bg = state.config["root"]["colours"]["bg"]

        self.configure(bg=bg)
        self.leftFrame = tk.Frame(self,bg=bg)
        self.rightFrame = tk.Frame(self,bg=bg)
        self.segmentHeader = tk.Label(self.leftFrame, fg=fg, bg=bg)
        self.segmentTime = tk.Label(self.rightFrame, fg=fg, bg=bg)
        self.goldHeader = tk.Label(self.leftFrame, fg=fg, bg=bg)
        self.goldTime = tk.Label(self.rightFrame, fg=fg, bg=bg)

        self.updateSegmentHeader()
        self.updateSegmentTime()
        self.updateGoldHeader()
        self.updateGoldTime()

        self.leftFrame.pack(side="left", padx=state.config["padx"])
        self.rightFrame.pack(side="left", padx=state.config["padx"])
        self.segmentHeader.pack(side="top",anchor="nw")
        self.goldHeader.pack(side="bottom",anchor="sw")
        self.segmentTime.pack(side="top",anchor="ne")
        self.goldTime.pack(side="bottom",anchor="se")

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

    def updateGoldHeader(self):
        self.goldHeader.configure(text="Best Split:")

    def updateGoldTime(self):
        self.goldTime.configure(text=self.state.comparisons[0].getString("segments",self.state.splitnum,{"precision":2}))
