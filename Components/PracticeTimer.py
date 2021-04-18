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
        if not self.state.runEnded:
            self.main.configure(\
                text=timeh.timeToString(\
                    self.state.segmentTime,\
                    {"blankToDash":False,"precision":2}\
                )\
            )
            self.main.configure(fg=self.timerColour())
        else:
            self.main.configure(\
                text=timeh.timeToString(\
                    self.state.currentTime,\
                    {"blankToDash":False,"precision":2}\
                )\
            )

    def timerColour(self):
        goldSegment = self.state.bestTime

        # ahead of gold
        if timeh.greater(goldSegment,self.state.segmentTime):
            return self.state.config["mainTimer"]["colours"]["main"]
        # behind gold
        else:
            return self.state.config["mainTimer"]["colours"]["behindLosing"]
