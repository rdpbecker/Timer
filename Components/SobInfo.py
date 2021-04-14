import tkinter as tk
from Components import Info 
import timeHelpers as timeh

class SobInfo(Info.Info):
    def __init__(self,parent,state):
        Info.Info.__init__(self,parent,state)
        self.header.configure(text="Sum of Bests:")
        self.info.configure(text=timeh.timeToString(self.state.currentBests.total,{"precision":2}))
