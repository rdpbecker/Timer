import categorySelection as cate, fileio
import SumList
import timeHelpers as timeh
import BaseState

class State(BaseState.State):
    bestTime = 0

    def __init__(self):
        BaseState.State.__init__(self)
        self.getPracticeSplits()

    ##########################################################
    ## Get the split number and the best time for that split,
    ## and set the appropriate values in the state.
    ##########################################################
    def getPracticeSplits(self):
        startSplitName = cate.readThingInList(self.splitnames)
        self.splitnum = self.splitnames.index(startSplitName)
        bestTimes = self.getTimes(1,self.comparesCsv)
        self.bestTime = bestTimes[self.splitnum]

    ##########################################################
    ## Do the state update when the run starts
    ##
    ## Parameters: time - the time the run started
    ##########################################################
    def onStarted(self,time):
        self.starttime = time
        self.started = True
        self.finished = False

    ##########################################################
    ## Do the state update when the split is ended
    ##
    ## Parameters: time - the time the split was ended
    ##########################################################
    def onSplit(self,time):
        self.finished = True
        splitTime = time - self.starttime
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
        fileio.writeCSV(self.config["baseDir"],self.game,self.category,self.completeCsv,self.comparesCsv)
