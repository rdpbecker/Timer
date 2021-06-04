import os
from util import dataManip
from util import fileio
from util import timeHelpers as timeh
from DataClasses import BptList
from DataClasses import Comparison
from DataClasses import CurrentRun
from DataClasses import SumList
from DataClasses import DifferenceList
from States import BaseState

class State(BaseState.State):
    pauseTime = 0
    splitstarttime = 0

    bptList = None
    currentBests = None
    bestExits = None

    currentRun = None

    comparisons = []
    currentComparison = None
    compareNum = 2
    numComparisons = 0

    def __init__(self,session):
        super().__init__(session)
        self.currentBests = SumList.SumList(dataManip.getTimesByCol(1,self.comparesCsv))
        self.bestExits = DifferenceList.DifferenceList(dataManip.getTimesByCol(8,self.comparesCsv))
        self.comparisons = []
        self.setComparisons()

    ##########################################################
    ## Initialize the comparisons, BPT list, and current run.
    ##########################################################
    def setComparisons(self):
        self.bptList = BptList.BptList(dataManip.getTimesByCol(1,self.comparesCsv))
        
        for i in range(int((len(self.comparesCsv[0])-1)/2)):
            self.comparisons.append(Comparison.Comparison( \
                self.comparesCsv[0][2*i+1], \
                self.comparesCsv[0][2*i+2], \
                dataManip.getTimesByCol(2*i+1,self.comparesCsv), \
                dataManip.getTimesByCol(2*i+2,self.comparesCsv) \
             ))

        if len(self.completeCsv[0]) > 1:
            self.comparisons.append(Comparison.Comparison( \
                "Last Run Splits", \
                "Last Run", \
                dataManip.getTimesByCol(1,self.completeCsv), \
                dataManip.getTimesByCol(2,self.completeCsv) \
            ))

        self.numComparisons = len(self.comparisons)
        if self.compareNum >= self.numComparisons:
            self.compareNum = self.numComparisons - 1
        self.currentComparison = self.comparisons[self.compareNum]
        
        self.currentRun = CurrentRun.CurrentRun()

    ##########################################################
    ## Sets the segment and total times. Should be used only
    ## for frame updates.
    ## Parameter: time - the current time according to the
    ##                   system clock
    ##########################################################
    def setTimes(self, time):
        self.segmentTime = time - self.splitstarttime
        self.totalTime = time - self.starttime

    ##########################################################
    ## Does all the state updates necessary to end a split. Uses
    ## the system clock at the exact time that the button/key was
    ## pressed for higher accuracy than the frame timer.
    ## 
    ## Parameters: time - the current system time
    ##########################################################
    def completeSegment(self,time):
        totalTime = time - self.starttime
        splitTime = time - self.splitstarttime
        self.currentRun.addSegment(splitTime,totalTime)
        self.bptList.update(totalTime)

        for i in range(self.numComparisons):
            self.comparisons[i].updateDiffs(splitTime,totalTime)
        if timeh.greater(self.currentBests.bests[self.splitnum],splitTime):
            self.currentBests.update(splitTime,self.splitnum)
        if timeh.greater(self.bestExits.totals[self.splitnum],totalTime):
            self.bestExits.update(totalTime,self.splitnum)
        self.splitnum = self.splitnum + 1
        self.splitstarttime = time
        if self.splitnum >= len(self.splitnames):
            self.runEnded = True
            self.localSave()

    ##########################################################
    ## Does all the state updates necessary to skip a split.
    ## 
    ## Parameters: time - the current system time
    ##########################################################
    def skipSegment(self,time):
        self.currentRun.addSegment("BLANK","BLANK")
        self.bptList.update(time-self.starttime)
        for i in range(self.numComparisons):
            self.comparisons[i].updateDiffs("BLANK","BLANK")
        self.splitnum = self.splitnum + 1
        self.splitstarttime = time
        if self.splitnum >= len(self.splitnames):
            self.runEnded = True
            self.localSave()

    ##########################################################
    ## Unpause
    ##
    ## Parameters: time - the current system time
    ##########################################################
    def endPause(self,time):
        self.paused = False
        elapsed = time - self.pauseTime
        self.starttime = self.starttime + elapsed
        self.splitstarttime = self.splitstarttime + elapsed
        self.pauseTime = 0

    ##########################################################
    ## Pause
    ## 
    ## Parameters: time - the current system time
    ##########################################################
    def startPause(self,time):
        self.paused = True
        self.pauseTime = time

    ##########################################################
    ## Compute the average for each split
    ##########################################################
    def getAverages(self):
        averages = []
        for i in range(len(self.splitnames)):
            average = []
            for j in range(int((len(self.completeCsv[0])-1)/2)):
                time = timeh.stringToTime(self.completeCsv[i+1][2*j+1])
                if not timeh.isBlank(time):
                    average.append(timeh.stringToTime(self.completeCsv[i+1][2*j+1]))
            if not timeh.isBlank(self.currentRun.segments[i]):
                average.append(self.currentRun.segments[i])
            averageTime = timeh.sumTimeList(average)
            if timeh.isBlank(averageTime):
                averages.append("BLANK")
            else:
                averages.append(averageTime/len(average))
        return SumList.SumList(averages)

    ##########################################################
    ## Determines whether the current run is a PB or not
    ##
    ## Returns: True if the current run is a PB, False if not
    ##########################################################
    def isPB(self):
        if self.currentRun.lastNonBlank() > self.comparisons[2].lastNonBlank():
            return True
        if self.currentRun.lastNonBlank() < self.comparisons[2].lastNonBlank():
            return False
        if timeh.greater(0,self.comparisons[2].totalDiffs[-1]):
            return True
        return False

    ##########################################################
    ## Cleans the state when the user wants to restart the run.
    ##########################################################
    def cleanState(self):
        self._cleanState()
        self.pauseTime = 0
        self.splitstarttime = 0
        self.comparisons = []

    def frameUpdate(self,time):
        if not self.started:
            return 1
        if self.runEnded:
            return 2
        if self.paused:
            time = self.pauseTime
        self.setTimes(time)

    def onStarted(self,time):
        if self.started:
            return 1
        self.starttime = time
        self.splitstarttime = time
        self.started = True

    def onSplit(self,time):
        if not self.started or self.paused or self.runEnded:
            return 1

        if self.splitnames[self.splitnum][-3:] == "[P]" and not self.splitnum == len(self.splitnames) and not self.paused:
            self.completeSegment(time)
            return 2

        self.completeSegment(time)

    def onComparisonChanged(self,rotation):
        self.compareNum = (self.compareNum+rotation)%self.numComparisons
        self.currentComparison = self.comparisons[self.compareNum]

    def setComparison(self,num):
        if num >= self.numComparisons:
            num = 2
        self.compareNum = num
        self.currentComparison = self.comparisons[self.compareNum]

    def onPaused(self,time):
        if not self.started or self.runEnded:
            return 1
        if self.paused:
            self.endPause(time)
        else:
            self.startPause(time)

    def onSplitSkipped(self,time):
        if not self.started or self.runEnded or self.paused:
            return 1
        self.skipSegment(time)

    def onReset(self):
        if not self.started or self.runEnded:
            return 1
        self.runEnded = True
        self.localSave()

    def onRestart(self):
        if not self.runEnded:
            return 1
        self.cleanState()
        self.setComparisons()

    def shouldFinish(self):
        return not self.started or self.runEnded

    ##########################################################
    ## Updates the local versions of the data files.
    ##########################################################
    def localSave(self):
        self.currentRun.fillTimes(len(self.splitnames))
        dataManip.replaceCols([self.splitnames],0,self.completeCsv)
        dataManip.replaceSumList(self.currentBests,1,1,self.comparesCsv,{"precision":5})
        dataManip.replaceSumList(self.getAverages(),1,3,self.comparesCsv,{"precision":5})
        if self.isPB():
            dataManip.replaceComparison(self.currentRun,1,5,self.comparesCsv,{"precision":5})
        dataManip.replaceComparison(self.bestExits,1,7,self.comparesCsv,{"precision":5})

        lastRun = [timeh.timesToStringList(self.currentRun.segments,{"precision":5}),timeh.timesToStringList(self.currentRun.totals,{"precision":5})]
        if not self.currentRun.empty:
            self.completeCsv[0].insert(1,"Run #"+str(int((len(self.completeCsv[1])+1)/2)))
            self.completeCsv[0].insert(2,"Totals")
            dataManip.insertSumList(SumList.SumList(self.currentRun.segments),1,1,self.completeCsv)
        for line in self.completeCsv:
            print(line)
        for line in self.comparesCsv:
            print(line)
        self.unSaved = True

    ##########################################################
    ## Export the locally saved data. Only do this after a local
    ## save.
    ##########################################################
    def saveTimes(self):
        fileio.writeCSVs(self.config["baseDir"],self.game,self.category,self.completeCsv,self.comparesCsv)
        self.unSaved = False
        print("Saved data successfully.")
