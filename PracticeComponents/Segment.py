import tkinter as tk
from Components import Component
from util import timeHelpers as timeh

class SegmentCompare(Component.Component):
    goldHeader = None
    goldTime = None

    def __init__(self,parent,state):
        Component.Component.__init__(self,parent,state)
        fg = state.config["root"]["colours"]["text"]
        bg = state.config["root"]["colours"]["bg"]

        self.configure(bg=bg)
        self.leftFrame = tk.Frame(self,bg=bg)
        self.rightFrame = tk.Frame(self,bg=bg)
        self.goldHeader = tk.Label(self.leftFrame, fg=fg, bg=bg)
        self.goldTime = tk.Label(self.rightFrame, fg=fg, bg=bg)

        self.updateGoldHeader()
        self.updateGoldTime()

        self.leftFrame.pack(side="left", padx=state.config["padx"])
        self.rightFrame.pack(side="left", padx=state.config["padx"])
        self.goldHeader.pack(side="bottom",anchor="sw")
        self.goldTime.pack(side="bottom",anchor="se")

    def onSplit(self):
        if not self.state.runEnded:
            self.updateGoldTime()

    def updateGoldHeader(self):
        self.goldHeader.configure(text="Best Split:")

    def updateGoldTime(self):
        self.goldTime.configure(text=timeh.timeToString(self.state.bestTime,{"precision":2}))
