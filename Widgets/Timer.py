import tkinter as tk
from Widgets import WidgetBase
from util import timeHelpers as timeh

class Timer(WidgetBase.WidgetBase):
    # main = None

    def __init__(self,parent,state,config):
        super().__init__(parent,state,config)
        self.configure(bg=config["colours"]["bg"],padx=state.config["padx"])
        self.main = tk.Label(self, bg=config["colours"]["bg"], fg=config["colours"]["main"], font=config["font"])
        m = config["position"]
        if m == "left":
            self.main.grid(row=0,column=0,columnspan=12,sticky="W")
        elif m == "center-left":
            self.main.grid(row=0,column=2,columnspan=10,sticky="W")
        elif m == "center":
            self.main.grid(row=0,column=0,columnspan=12)
        elif m == "center-right":
            self.main.grid(row=0,column=0,columnspan=10,sticky="E")
        elif m == "right":
            self.main.grid(row=0,column=0,columnspan=12,sticky="E")

        self.resetUI()

    def onRestart(self):
        self.resetUI()

    def resetUI(self):
        self.setMainTime(0)
        self.main.configure(fg=self.config["colours"]["main"])

    def frameUpdate(self):
        if not self.state.runEnded:
            self.setMainTime(self.state.totalTime)
            self.main.configure(fg=self.timerColour())
        else:
            self.setMainTime(self.state.currentRun.totals[-1])

    def setMainTime(self,time):
        self.main.configure(\
            text=timeh.timeToString(\
                time,\
                {\
                    "blankToDash": False,\
                    "precision": self.config["precision"],\
                }\
            )\
        )

    def timerColour(self):
        splitnum = self.state.splitnum
        comparisonTime = self.state.currentComparison.totals[splitnum]
        comparisonSegment = self.state.currentComparison.segments[splitnum]
        goldSegment = self.state.comparisons[0].segments[splitnum]

        # last split skipped
        if self.state.splitnum \
            and timeh.isBlank(self.state.currentRun.totals[-1]):
            # total blank or ahead of total
            if timeh.greater(comparisonTime,self.state.totalTime):
                return self.config["colours"]["main"]
            # behind total
            else:
                return self.config["colours"]["behindLosing"]
        # total blank
        if timeh.isBlank(comparisonTime):
            # gold blank or ahead of gold
            if timeh.greater(goldSegment,self.state.segmentTime):
                return self.config["colours"]["main"]
            # behind gold
            else:
                return self.config["colours"]["behindLosing"]
        # ahead of total
        elif timeh.greater(comparisonTime,self.state.totalTime):
            # segment blank
            if timeh.isBlank(comparisonSegment):
                # gold blank or ahead of gold
                if timeh.greater(goldSegment,self.state.segmentTime):
                    return self.config["colours"]["main"]
                # behind gold
                else:
                    return self.config["colours"]["aheadLosing"]
            # ahead of segment
            elif timeh.greater(comparisonSegment,self.state.segmentTime):
                # gold blank or ahead of gold
                if timeh.greater(goldSegment,self.state.segmentTime):
                    return self.config["colours"]["main"]
                # behind gold
                else:
                    return self.config["colours"]["notGoldAheadGaining"]
            # behind segment
            else:
                return self.config["colours"]["aheadLosing"]
        # behind total
        else:
            # segment blank
            if timeh.isBlank(comparisonSegment):
                # gold blank or behind gold
                if timeh.greater(self.state.segmentTime,goldSegment):
                    return self.config["colours"]["behindLosing"]
                # ahead of gold
                else:
                    return self.config["colours"]["behindGaining"]
            # ahead of segment
            elif timeh.greater(comparisonSegment,self.state.segmentTime):
                # gold blank or ahead of gold
                if timeh.greater(goldSegment,self.state.segmentTime):
                    return self.config["colours"]["behindGaining"]
                # behind gold
                else:
                    return self.config["colours"]["notGoldBehindGaining"]
            # behind segment
            else:
                return self.config["colours"]["behindLosing"]
