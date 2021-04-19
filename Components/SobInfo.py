import tkinter as tk
from Components import Info 
from util import timeHelpers as timeh

class SobInfo(Info.Info):
    def __init__(self,parent,state,config):
        Info.Info.__init__(self,parent,state,config)
        self.header.configure(text="Sum of Bests:")
        self.info.configure(text=timeh.timeToString(self.state.currentBests.total,{"precision":2}))

    def onSplit(self):
        self.info.configure(text=timeh.timeToString(self.state.currentBests.total,{"precision":2}))
