import tkinter as tk
from Widgets import WidgetBase
from util import timeHelpers as timeh
from util import fileio

class Timer(WidgetBase.WidgetBase):
    # main = None

    def __init__(self,parent,state):
        config = fileio.readJson("defaults/timer.json")
        super().__init__(parent,state,config)
        self.configure(bg=config["colours"]["bg"])
        self.main = tk.Label(self, bg=config["colours"]["bg"], fg=config["colours"]["main"], font=config["font"])
        self.main.grid(row=0,column=0,columnspan=12)

    def frameUpdate(self):
        self.updateTimer(self.state.segmentTime)

    def onSplit(self):
        self.updateTimer(self.state.currentTime)

    def onRestart(self):
        self.updateTimer(0)

    def updateTimer(self,time):
        self.main.configure(\
            text=timeh.timeToString(time, {"blankToDash":False,"precision":self.config["precision"]}))
        self.main.configure(fg=self.timerColour(time))

    def timerColour(self,time):
        goldSegment = self.state.bestTime

        # ahead of gold
        if timeh.isBlank(goldSegment) or goldSegment >= time:
            return self.config["colours"]["main"]
        # behind gold
        else:
            return self.config["colours"]["behindLosing"]
