import tkinter as tk
from Components import Info
from util import timeHelpers as timeh

class BptInfo(Info.Info):
    def __init__(self,parent,state,config):
        Info.Info.__init__(self,parent,state,config)
        self.header.configure(text="Best Possible Time:")
        self.updateTime()

    def hide(self):
        self.info.configure(text="-")

    def frameUpdate(self):
        if self.state.runEnded:
            return
        if self.shouldHide():
            self.hide()
            return
        if not timeh.greater(self.state.comparisons[0].segments[self.state.splitnum],self.state.segmentTime):
            self.info.configure(
                text=\
                    timeh.timeToString(\
                        timeh.add(\
                            timeh.difference(self.state.segmentTime,self.state.comparisons[0].segments[self.state.splitnum]),\
                            self.state.bptList.total
                        ), \
                        {\
                            "precision": self.config["precision"]\
                        }\
                    )\
            )

    def onSplit(self):
        self.updateTime()

    def onRestart(self):
        self.updateTime()

    def updateTime(self):
        if self.shouldHide():
            self.hide()
            return
        self.info.configure(\
            text=\
                timeh.timeToString(\
                    self.state.bptList.total,\
                    {\
                        "precision": self.config["precision"]\
                    }\
                )\
        )
