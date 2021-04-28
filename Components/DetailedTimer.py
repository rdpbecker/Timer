import tkinter as tk
from Components import Component
from util import timeHelpers as timeh

class Timer(Component.Component):
    main = None
    segment = None

    def __init__(self,parent,state,config):
        Component.Component.__init__(self,parent,state,config)
        self.configure(bg=config["colours"]["bg"], padx=state.config["padx"])
        self.main = tk.Label(self, bg=config["colours"]["bg"], fg=config["mainTimer"]["colours"]["main"], font=config["mainTimer"]["font"])

        self.segment = tk.Label(self, bg=config["colours"]["bg"], fg=config["segmentTimer"]["colour"], font=config["segmentTimer"]["font"])

        m = config["mainTimer"]["position"]
        if m == "left":
            self.main.grid(row=1,column=0,columnspan=12,sticky="W")
        elif m == "center-left":
            self.main.grid(row=1,column=2,columnspan=10,sticky="W")
        elif m == "center":
            self.main.grid(row=1,column=0,columnspan=12)
        elif m == "center-right":
            self.main.grid(row=1,column=0,columnspan=10,sticky="E")
        elif m == "right":
            self.main.grid(row=1,column=0,columnspan=12,sticky="E")

        s = config["segmentTimer"]["position"]
        if s == "left":
            self.segment.grid(row=0,column=0,columnspan=12,sticky="W")
        elif s == "center-left":
            self.segment.grid(row=0,column=2,columnspan=10,sticky="W")
        elif s == "center":
            self.segment.grid(row=0,column=0,columnspan=12)
        elif s == "center-right":
            self.segment.grid(row=0,column=0,columnspan=10,sticky="E")
        elif s == "right":
            self.segment.grid(row=0,column=0,columnspan=12,sticky="E")
        self.resetUI()

    def onRestart(self):
        self.resetUI()

    def resetUI(self):
        self.main.configure(fg=self.config["mainTimer"]["colours"]["main"])
        self.setMainTime(0)
        self.setSegmentTime(0)

    def frameUpdate(self):
        if not self.state.runEnded:
            self.setMainTime(self.state.totalTime)
            self.main.configure(fg=self.timerColour())
            self.setSegmentTime(self.state.segmentTime)
        else:
            self.setMainTime(self.state.currentRun.totals[-1])
            self.setSegmentTime(self.state.currentRun.segments[-1])

    def setMainTime(self,time):
        self.main.configure(text=self.formatTime(time,"main"))

    def setSegmentTime(self,time):
        self.segment.configure(text=self.formatTime(time,"segment"))

    def formatTime(self,time,ttype):
        if ttype == "main":
            precision = self.config["mainTimer"]["precision"]
        else:
            precision = self.config["segmentTimer"]["precision"]
        return timeh.timeToString(\
                time,\
                {\
                    "blankToDash": False,\
                    "precision": precision
                }\
            )\

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
                return self.config["mainTimer"]["colours"]["main"]
            # behind total
            else:
                return self.config["mainTimer"]["colours"]["behindLosing"]
        # total blank
        if timeh.isBlank(comparisonTime):
            # gold blank or ahead of gold
            if timeh.greater(goldSegment,self.state.segmentTime):
                return self.config["mainTimer"]["colours"]["main"]
            # behind gold
            else:
                return self.config["mainTimer"]["colours"]["behindLosing"]
        # ahead of total
        elif timeh.greater(comparisonTime,self.state.totalTime):
            # segment blank
            if timeh.isBlank(comparisonSegment):
                # gold blank or ahead of gold
                if timeh.greater(goldSegment,self.state.segmentTime):
                    return self.config["mainTimer"]["colours"]["main"]
                # behind gold
                else:
                    return self.config["mainTimer"]["colours"]["aheadLosing"]
            # ahead of segment
            elif timeh.greater(comparisonSegment,self.state.segmentTime):
                # gold blank or ahead of gold
                if timeh.greater(goldSegment,self.state.segmentTime):
                    return self.config["mainTimer"]["colours"]["main"]
                # behind gold
                else:
                    return self.config["mainTimer"]["colours"]["notGoldAheadGaining"]
            # behind segment
            else:
                return self.config["mainTimer"]["colours"]["aheadLosing"]
        # behind total
        else:
            # segment blank
            if timeh.isBlank(comparisonSegment):
                # gold blank or behind gold
                if timeh.greater(self.state.segmentTime,goldSegment):
                    return self.config["mainTimer"]["colours"]["behindLosing"]
                # ahead of gold
                else:
                    return self.config["mainTimer"]["colours"]["behindGaining"]
            # ahead of segment
            elif timeh.greater(comparisonSegment,self.state.segmentTime):
                # gold blank or ahead of gold
                if timeh.greater(goldSegment,self.state.segmentTime):
                    return self.config["mainTimer"]["colours"]["behindGaining"]
                # behind gold
                else:
                    return self.config["mainTimer"]["colours"]["notGoldBehindGaining"]
            # behind segment
            else:
                return self.config["mainTimer"]["colours"]["behindLosing"]
