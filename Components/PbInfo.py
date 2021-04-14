import tkinter as tk
from Components import Info 

class PbInfo(Info.Info):
    def __init__(self,parent,state):
        Info.Info.__init__(self,parent,state)
        self.header.configure(text="Personal Best:")
        self.info.configure(text=self.state.comparisons[2].getString("totals",-1,{"precision":2}))
