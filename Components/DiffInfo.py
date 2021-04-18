import tkinter as tk
from Components import Info
from util import timeHelpers as timeh

class DiffInfo(Info.Info):
    def __init__(self,parent,state,config):
        Info.Info.__init__(self,parent,state,config)
        self.header.configure(text="Last Split (vs Best):")

    def frameUpdate(self):
        if self.state.runEnded:
            return
        if not timeh.greater(self.state.comparisons[0].segments[self.state.splitnum],self.state.segmentTime):
            self.header.configure(text="Current Segment:")
            self.info.configure(text=timeh.timeToString(\
                timeh.difference(self.state.segmentTime,self.state.comparisons[0].segments[self.state.splitnum]),\
                {"showSign": True, "precision":2})\
            )

    def onSplit(self):
        if not self.state.splitnum:
            return
        self.header.configure(text="Last Split (vs Best):")
        self.info.configure(text=self.state.comparisons[0].getString("segmentDiffs",self.state.splitnum-1,{"showSign":True,"precision":2}))
