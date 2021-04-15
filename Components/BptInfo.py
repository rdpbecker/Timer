import tkinter as tk
from Components import Info
import timeHelpers as timeh

class BptInfo(Info.Info):
    def __init__(self,parent,state):
        Info.Info.__init__(self,parent,state)
        self.header.configure(text="Best Possible Time:")
        self.info.configure(text=timeh.timeToString(self.state.bptList.total,{"precision":2}))

    def frameUpdate(self):
        if self.state.runEnded:
            return
        if not timeh.greater(self.state.comparisons[0].segments[self.state.splitnum],self.state.segmentTime):
            self.info.configure(text=timeh.timeToString(\
                timeh.add(\
                    timeh.difference(self.state.segmentTime,self.state.comparisons[0].segments[self.state.splitnum]),\
                    self.state.bptList.total
                ), {"precision":2})\
            )

    def onSplit(self):
        self.info.configure(text=timeh.timeToString(self.state.bptList.total,{"precision":2}))
