import tkinter as tk
from Components import Component

class SegmentTimes(Component.Component):
    segmentHeader = None
    segmentTime = None
    goldHeader = None
    goldTime = None

    def __init__(self,parent,state,config):
        Component.Component.__init__(self,parent,state,config)
        fg = config["colours"]["text"]
        bg = config["colours"]["bg"]
        font = config["font"]

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
        if config["includeCurrentComparison"]:
            self.segmentHeader.pack(side="top",anchor="nw")
            self.segmentTime.pack(side="top",anchor="ne")
        self.goldHeader.pack(side="bottom",anchor="sw")
        self.goldTime.pack(side="bottom",anchor="se")

    def hide(self):
        self.segmentHeader.configure(text="")
        self.segmentTime.configure(text="")

    def onRestart(self):
        if self.shouldHide():
            self.hide()
            return
        self.updateSegmentHeader()
        self.updateSegmentTime()
        self.updateGoldTime()

    def onSplit(self):
        if self.shouldHide():
            self.hide()
            return
        if not self.state.runEnded:
            self.updateSegmentTime()
            self.updateGoldTime()

    def onSplitSkipped(self):
        if self.shouldHide():
            self.hide()
            return
        if not self.state.runEnded:
            self.updateSegmentTime()
            self.updateGoldTime()

    def onComparisonChanged(self):
        if self.shouldHide():
            self.hide()
            return
        if not self.state.runEnded:
            self.updateSegmentHeader()
            self.updateSegmentTime()

    def updateSegmentHeader(self):
        self.segmentHeader.configure(text=self.state.currentComparison.segmentHeader+":")

    def updateSegmentTime(self):
        self.segmentTime.configure(\
            text=\
                self.state.currentComparison.getString(\
                    "segments",\
                    self.state.splitnum,\
                    {\
                        "precision": self.config["precision"]\
                    }\
                )\
        )

    def updateGoldHeader(self):
        self.goldHeader.configure(text="Best Split:")

    def updateGoldTime(self):
        self.goldTime.configure(\
            text=\
                self.state.comparisons[0].getString(\
                    "segments",\
                    self.state.splitnum,\
                    {\
                        "precision": self.config["precision"]\
                    }\
                )\
        )
