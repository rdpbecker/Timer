from util import fileio
from util import timeHelpers as timeh
from DataClasses import SumList
from States import BaseState

class State(BaseState.State):
    bestTime = 0
    currentTime = 0
    splitName = ""
    splitnum = 0

    def __init__(self,session):
        super().__init__(session)
        self.splitName = session.split
        self.splitnum = self.splitnames.index(session.split)
        bestTimes = self.getTimes(1,self.comparesCsv)
        self.bestTime = bestTimes[self.splitnum]

    def frameUpdate(self,time):
        if not (self.started and not self.runEnded):
            return 1
        self.segmentTime = time - self.starttime

    ##########################################################
    ## Do the state update when the run starts
    ##
    ## Parameters: time - the time the run started
    ##########################################################
    def onStarted(self,time):
        self.starttime = time
        self.started = True
        self.runEnded = False

    ##########################################################
    ## Do the state update when the split is ended
    ##
    ## Parameters: time - the time the split was ended
    ##########################################################
    def onSplit(self,time):
        self.runEnded = True
        splitTime = time - self.starttime
        self.currentTime = splitTime
        self.unSaved = True
        if timeh.greater(self.bestTime,splitTime):
            self.bestTime = splitTime

    ##########################################################
    ## Restart the run
    ##########################################################
    def onRestart(self):
        self.started = False

    ##########################################################
    ## Save the times when we close the window.
    ##########################################################
    def saveTimes(self):
        bests = SumList.SumList(self.getTimes(1,self.comparesCsv))
        bests.update(self.bestTime,self.splitnum)
        bestSplits = [timeh.timesToStringList(bests.bests,{"precision":5}), timeh.timesToStringList(bests.totalBests,{"precision":5})]
        self.replaceCsvLines(bestSplits,1,self.comparesCsv)
        fileio.writeCSVs(self.config["baseDir"],self.game,self.category,self.completeCsv,self.comparesCsv)
        print("Save successful.")
