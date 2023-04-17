import tkinter as tk
from Widgets import WidgetBase

class SegmentTimes(WidgetBase.WidgetBase):
    # segmentHeader = None
    # segmentTime = None
    # goldHeader = None
    # goldTime = None

    def __init__(self,parent,state,config):
        super().__init__(parent,state,config)
        fg = config["colours"]["text"]
        bg = config["colours"]["bg"]

        self.configure(bg=bg)
        self.leftFrame = tk.Frame(self,bg=bg)
        self.rightFrame = tk.Frame(self,bg=bg)
        self.segmentHeader = tk.Label(self.leftFrame, fg=fg, bg=bg)
        self.segmentTime = tk.Label(self.rightFrame, fg=fg, bg=bg)
        self.goldHeader = tk.Label(self.leftFrame, fg=fg, bg=bg)
        self.goldTime = tk.Label(self.rightFrame, fg=fg, bg=bg)

        self.leftFrame.pack(side="left", padx=state.config["padx"])
        self.rightFrame.pack(side="left", padx=state.config["padx"])
        row = 0
        if config["includeCurrentComparison"]:
            self.segmentHeader.grid(row=row,column=0,sticky="W")
            self.segmentTime.grid(row=row,column=0,sticky="E")
            row = 1
            self.leftFrame.rowconfigure(1,weight=1)
            self.rightFrame.rowconfigure(1,weight=1)
        self.goldHeader.grid(row=row,column=0,sticky="W")
        self.goldTime.grid(row=row,column=0,sticky="E")
        self.leftFrame.rowconfigure(0,weight=1)
        self.rightFrame.rowconfigure(0,weight=1)

        self.resetUI()

    def hide(self):
        self.segmentHeader.configure(text="")
        self.segmentTime.configure(text="")

    def onRestart(self):
        self.resetUI()

    def resetUI(self):
        if self.shouldHide():
            self.hide()
        else:
            self.updateSegmentHeader()
            self.updateSegmentTime()
        self.updateGoldHeader()
        self.updateGoldTime()

    def onSplit(self):
        if not self.state.runEnded:
            if self.shouldHide():
                self.hide()
            else:
                self.updateSegmentTime()
            self.updateGoldTime()

    def onSplitSkipped(self):
        if not self.state.runEnded:
            if self.shouldHide():
                self.hide()
            else:
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
