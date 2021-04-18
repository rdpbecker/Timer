import tkinter as tk
from Components import Component
import timeHelpers as timeh

class Timer(Component.Component):
    main = None

    def __init__(self,parent,state):
        Component.Component.__init__(self,parent,state)
        self.configure(bg=state.config["root"]["colours"]["bg"])
        self.state = state
        self.main = tk.Label(self, bg=state.config["root"]["colours"]["bg"], fg=state.config["mainTimer"]["colours"]["main"], font=state.config["mainTimer"]["font"])
        self.main.grid(row=0,column=0,columnspan=12)

    def frameUpdate(self):
        self.updateTimer(self.state.segmentTime)

    def onSplit(self):
        self.updateTimer(self.state.currentTime)

    def updateTimer(self,time):
        self.main.configure(\
            text=timeh.timeToString(time, {"blankToDash":False,"precision":2}))
        self.main.configure(fg=self.timerColour(time))

    def timerColour(self,time):
        goldSegment = self.state.bestTime

        # ahead of gold
        if goldSegment >= time:
            return self.state.config["mainTimer"]["colours"]["main"]
        # behind gold
        else:
            return self.state.config["mainTimer"]["colours"]["behindLosing"]
