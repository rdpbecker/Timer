import Time, Timelist, gui, categorySelection as cate, fileio 
import timeHelpers as timeh
import Comparison
import BptList, SobList, SumList
import CurrentRun
import os

class State:
    started = False
    paused = False
    reset = False

    pauseTime = 0
    starttime = 0
    splitstarttime = 0

    splitnum = 0
    splitnames = []

    game = ""
    category = ""

    completeCsv = None
    comparesCsv = None

    bptList = None
    currentBests = None

    currentRun = None

    comparisons = []
    currentCompare = 2
    numComparisons = 0

    generalInfo = None
    generalInfoKeys = []

    config = None

    def __init__(self):
        self.config = self.getConfigAndSplits()

        splitArrs = fileio.csvReadStart(self.config["baseDir"],self.game,self.category,self.splitnames)
        self.completeCsv = splitArrs[0]
        self.comparesCsv = splitArrs[1]

        self.bptList = BptList.BptList(self.getTimes(1,self.comparesCsv))
        self.currentBests = SobList.SobList(self.getTimes(1,self.comparesCsv))
        
        for i in range(int((len(self.comparesCsv[0])-1)/2)):
            self.comparisons.append(Comparison.Comparison( \
                self.comparesCsv[0][2*i+1], \
                self.comparesCsv[0][2*i+2], \
                self.getTimes(2*i+1,self.comparesCsv), \
                self.getTimes(2*i+2,self.comparesCsv) \
             ))

        ## There's no way to take out a comparison at the moment, and we
        ## set all the comparisons for the first run of a category when
        ## we read the CSV file, so if there isn't a run already we just
        ## set the last run to be the PB splits. It doesn't matter 
        ## because the PB splits are all '-' anyway
        if len(self.completeCsv[0]) > 1:
            self.comparisons.append(Comparison.Comparison( \
                "Last Run Splits", \
                "Last Run", \
                self.getTimes(1,self.completeCsv), \
                self.getTimes(2,self.completeCsv) \
            ))
        else: 
            self.comparisons.append(Comparison.Comparison( \
                "Last Run Splits", \
                "Last Run", \
                self.getTimes(1,self.comparesCsv), \
                self.getTimes(2,self.comparesCsv) \
            ))

        self.numComparisons = len(self.comparisons)
        
        self.currentRun = CurrentRun.CurrentRun()

        if self.config["numSplits"] > len(self.splitnames):
            self.config["numSplits"] = len(self.splitnames)
            self.config["activeSplit"] = len(self.splitnames) - 2

    def getConfigAndSplits(self):
        defaultConfig = fileio.readJson("defaultConfig.json")
        config = defaultConfig
        if os.path.exists("config.json"):
            userConfig = fileio.readJson("config.json")
            config.update(userConfig)
        self.getSplitNames(config["baseDir"])
        cateFile = config["baseDir"] + "/" + self.game + "/" + self.category + "_config.json"
        if os.path.exists(cateFile):
            cateConfig = fileio.readJson(cateFile)
            config.update(cateConfig)
        return config

    def getSplitNames(self,baseDir):
        splitNames = cate.findAllSplits(baseDir)
        names = cate.findNames(splitNames,0)
        self.game = cate.readThingInList(names)
        cate.restrictCategories(splitNames,self.game)
        categories = cate.findNames(splitNames,1)
        self.category = cate.readThingInList(categories)
        self.splitnames = cate.findGameSplits(splitNames,self.category)
        fileio.stripEmptyStrings(self.splitnames)

    def getTimes(self,col,toCheck):
        times = []
        for i in range(1,len(toCheck)):
            times.append(timeh.stringToTime(toCheck[i][col]))
        return times

    def getWindowStart(self):
        if self.splitnum <= self.config["activeSplit"] - 1:
            return 0
        if self.splitnum >= len(self.splitnames) - (self.config["numSplits"]-self.config["activeSplit"]):
            return len(self.splitnames) - self.config["numSplits"]
        return self.splitnum - (self.config["activeSplit"] - 1)

    def completeSegment(self,endTime):
        totalTime = endTime - self.starttime
        splitTime = endTime - self.splitstarttime
        self.currentRun.addSegment(splitTime,totalTime)

        self.bptList.update(totalTime)
        for i in range(self.numComparisons):
            self.comparisons[i].updateDiffs(splitTime,totalTime)
        if timeh.greater(self.currentBests.bests[self.splitnum],splitTime):
            self.currentBests.update(splitTime,self.splitnum)
        self.splitnum = self.splitnum + 1

    def skipSegment(self,splitEnd):
        self.currentRun.addSegment("BLANK","BLANK")
        self.bptList.update(splitEnd-self.starttime)
        for i in range(self.numComparisons):
            self.comparisons[i].updateDiffs("BLANK","BLANK")
        self.splitnum = self.splitnum + 1

    def endPause(self,time):
            self.paused = False
            elapsed = time - self.pauseTime
            self.starttime = self.starttime + elapsed
            self.splitstarttime = self.splitstarttime + elapsed
            self.pauseTime = 0

    def startPause(self,time):
            self.paused = True
            self.pauseTime = time

    def getBests(self):
        return [self.currentBests.bests,self.currentBests.totalBests]

    def getAverages(self):
        averages = []
        for i in range(len(self.currentRun.segments)):
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

    def isPB(self):
        if len(self.currentRun.totals) > len(self.comparisons[2].totals):
            return 1
        if len(self.currentRun.totals) < len(self.comparisons[2].totals):
            return 0
        if timeh.greater(0,self.comparisons[2].totalDiffs[-1]):
            return 1
        return 0

    def fillTimes(self,times):
        n = times.length
        for i in range(n+1,len(self.completeCsv)):
            times.insert(Time.Time(5,timestring='-'))

    def replaceCsvLines(self,lines,start,csv_ref):
        for i in range(1,len(csv_ref)):
            for j in range(len(lines)):
                csv_ref[i][start+j]=lines[j][i-1]

    def insertCsvLines(self,lines,startIndex):
        for i in range(1,len(self.completeCsv)):
            for j in range(len(lines)):
                self.completeCsv[i].insert(startIndex+j,lines[j][i-1])

    ##########################################################
    ## Calculate all the comparisons and export them along 
    ## with the splits from the current run
    ##########################################################
    def doEnd(self):
        self.currentRun.fillTimes(len(self.splitnames))
        bests = self.getBests()
        averages = self.getAverages()
        if self.isPB():
            pbSplits = [timeh.timesToStringList(self.currentRun.segments,precision=5),timeh.timesToStringList(self.currentRun.totals,precision=5)]
        else:
            pbSplits = [timeh.timesToStringList(self.comparisons[2].segments,precision=5),timeh.timesToStringList(self.comparisons[2].totals,precision=5)]
        bestSplits = [timeh.timesToStringList(bests[0],precision=5), timeh.timesToStringList(bests[1],precision=5)]
        averageSplits = [timeh.timesToStringList(averages.bests,precision=5), timeh.timesToStringList(averages.totalBests,precision=5)]
        lastRun = [timeh.timesToStringList(self.currentRun.segments,precision=5),timeh.timesToStringList(self.currentRun.totals,precision=5)]
        self.completeCsv[0].insert(1,"Run #"+str(int((len(self.completeCsv[1])+1)/2)))
        self.completeCsv[0].insert(2,"Totals")
        self.replaceCsvLines([self.splitnames],0,self.completeCsv)
        self.replaceCsvLines(bestSplits,1,self.comparesCsv)
        self.replaceCsvLines(averageSplits,3,self.comparesCsv)
        self.replaceCsvLines(pbSplits,5,self.comparesCsv)
        self.insertCsvLines(lastRun,1)
        fileio.writeCSV(self.config["baseDir"],self.game,self.category,self.completeCsv,self.comparesCsv)
        print("Close the window to end the program")
