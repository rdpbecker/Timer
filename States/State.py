import os
from util import fileio
from util import categorySelection as cate
from util import readConfig as rc
from util import timeHelpers as timeh
from DataClasses import BptList
from DataClasses import Comparison
from DataClasses import CurrentRun
from DataClasses import SumList
from States import BaseState

class State(BaseState.State):
    pauseTime = 0
    splitstarttime = 0

    bptList = None
    currentBests = None

    currentRun = None

    comparisons = []
    currentComparison = None
    compareNum = 2
    numComparisons = 0

    def __init__(self):
        BaseState.State.__init__(self)
        self.bptList = BptList.BptList(self.getTimes(1,self.comparesCsv))
        self.currentBests = SumList.SumList(self.getTimes(1,self.comparesCsv))
        
        for i in range(int((len(self.comparesCsv[0])-1)/2)):
            self.comparisons.append(Comparison.Comparison( \
                self.comparesCsv[0][2*i+1], \
                self.comparesCsv[0][2*i+2], \
                self.getTimes(2*i+1,self.comparesCsv), \
                self.getTimes(2*i+2,self.comparesCsv) \
             ))

        if len(self.completeCsv[0]) > 1:
            self.comparisons.append(Comparison.Comparison( \
                "Last Run Splits", \
                "Last Run", \
                self.getTimes(1,self.completeCsv), \
                self.getTimes(2,self.completeCsv) \
            ))

        self.numComparisons = len(self.comparisons)
        self.currentComparison = self.comparisons[2]
        
        self.currentRun = CurrentRun.CurrentRun()

        if self.config["numSplits"] > len(self.splitnames):
            self.config["numSplits"] = len(self.splitnames)
            self.config["activeSplit"] = len(self.splitnames) - 2

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
        self.splitnum = self.splitnum + 1
        if self.splitnum >= len(self.splitnames):
            self.runEnded = True
        self.splitstarttime = time

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
        if self.splitnum >= len(self.splitnames):
            self.runEnded = True
        self.splitstarttime = time

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

    def frameUpdate(self,time):
        if not self.started or self.finished or self.reset or self.runEnded:
            return 1
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
        if not self.started or self.paused:
            return 1

        if self.splitnames[self.splitnum][-3:] == "[P]" and not self.splitnum == len(self.splitnames) and not self.paused:
            self.completeSegment(time)
            return 2

        self.completeSegment(time)

    def onComparisonChanged(self,rotation):
        self.compareNum = (self.compareNum+rotation)%self.numComparisons
        self.currentComparison = self.comparisons[self.compareNum]

    def onPaused(self,time):
        if self.paused:
            self.endPause(time)
        else:
            self.startPause(time)

    def onSplitSkipped(self,time):
        self.skipSegment(time)

    def onReset(self):
        self.reset = True
        self.saveTimes()

    ##########################################################
    ## Calculate all the comparisons and export them along 
    ## with the splits from the current run
    ##########################################################
    def saveTimes(self):
        self.currentRun.fillTimes(len(self.splitnames))
        bests = self.currentBests
        averages = self.getAverages()
        if self.isPB():
            pbSplits = [timeh.timesToStringList(self.currentRun.segments,{"precision":5}),timeh.timesToStringList(self.currentRun.totals,{"precision":5})]
        else:
            pbSplits = [timeh.timesToStringList(self.comparisons[2].segments,{"precision":5}),timeh.timesToStringList(self.comparisons[2].totals,{"precision":5})]
        bestSplits = [timeh.timesToStringList(bests.bests,{"precision":5}), timeh.timesToStringList(bests.totalBests,{"precision":5})]
        averageSplits = [timeh.timesToStringList(averages.bests,{"precision":5}), timeh.timesToStringList(averages.totalBests,{"precision":5})]
        lastRun = [timeh.timesToStringList(self.currentRun.segments,{"precision":5}),timeh.timesToStringList(self.currentRun.totals,{"precision":5})]
        self.completeCsv[0].insert(1,"Run #"+str(int((len(self.completeCsv[1])+1)/2)))
        self.completeCsv[0].insert(2,"Totals")
        self.replaceCsvLines([self.splitnames],0,self.completeCsv)
        self.replaceCsvLines(bestSplits,1,self.comparesCsv)
        self.replaceCsvLines(averageSplits,3,self.comparesCsv)
        self.replaceCsvLines(pbSplits,5,self.comparesCsv)
        self.insertCsvLines(lastRun,1)
        fileio.writeCSV(self.config["baseDir"],self.game,self.category,self.completeCsv,self.comparesCsv)
        print("Saved data successfully.")
        print("Close the window to end the program")
