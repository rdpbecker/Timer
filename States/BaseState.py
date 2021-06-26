from util import fileio
from util import readConfig as rc

class State:
    started = False
    paused = False
    runEnded = False

    starttime = 0
    segmentTime = 0
    totalTime = 0

    splitnum = 0
    splitnames = []
    numSplits = 0

    game = ""
    category = ""

    completeCsv = None
    comparesCsv = None

    config = None

    unSaved = False

    def __init__(self,session):
        self.config = rc.getUserConfig()
        self.game = session.game
        self.category = session.category
        self.splitnames = session.splitNames
        self.numSplits = len(self.splitnames)

        splitArrs = fileio.csvReadStart(self.config["baseDir"],self.game,self.category,self.splitnames)
        self.completeCsv = splitArrs[0]
        self.comparesCsv = splitArrs[1]

    def _cleanState(self):
        self.started = False
        self.paused = False
        self.runEnded = False

        self.starttime = 0
        self.segmentTime = 0
        self.totalTime = 0

        self.splitnum = 0

    def frameUpdate(self):
        pass

    def onStarted(self,time):
        pass

    def onSplit(self,time):
        pass

    def onComparisonChanged(self,rotation):
        pass

    def onPaused(self,time):
        pass

    def onSplitSkipped(self,time):
        pass

    def onReset(self):
        pass
        
    def onRestart(self):
        pass

    def saveTimes(self):
        pass

    def shouldFinish(self):
        return True
