from Widgets import InfoBase
from util import timeHelpers as timeh

class SobInfo(InfoBase.InfoBase):
    def __init__(self,parent,state,config):
        super().__init__(parent,state,config)
        self.resetUI()

    def resetUI(self):
        self.header.configure(text="Sum of Bests:")
        self.updateTime()

    def onSplit(self):
        self.updateTime()

    def updateTime(self):
        self.info.configure(text=timeh.timeToString(self.state.currentBests.total,{"precision":self.config["precision"]}))
