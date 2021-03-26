import Time, Timelist, gui, categorySelection as cate, fileio 
import os

guiComplete=0

class State:
    started = False
    paused = False
    pauseTime = 0
    starttime = 0
    splitstarttime = 0
    lastUpdateTime = 0
    splitnum = 0
    splitnames = []
    game = ""
    category = ""
    completeCsv = None
    bptList = None
    currentBests = None
    compares = []
    compareSplits = []
    diffs = []
    diffSplits = []
    currentSplits = None
    currentTotals = None
    reset = False
    currentCompare = 2
    compareHeaders = []
    splitCompareHeaders = []
    windowStart = 0
    config = None
    numComparisons = 0

    def __init__(self):
        self.config = self.getConfigAndSplits()

        splitArrs = fileio.csvReadStart(self.config["baseDir"],self.game,self.category,self.splitnames)
        self.completeCsv = splitArrs[0]
        self.comparesCsv = splitArrs[1]

        self.bptList = self.getTimes(1,self.comparesCsv)
        self.currentBests = self.getTimes(1,self.comparesCsv)
        
        for i in range(int((len(self.comparesCsv[0])-1)/2)):
            self.compares.append(self.getTimes(2*i+2,self.comparesCsv))
            self.compareSplits.append(self.getTimes(2*i+1,self.comparesCsv))
            self.splitCompareHeaders.append(self.comparesCsv[0][2*i+1])
            self.compareHeaders.append(self.comparesCsv[0][2*i+2])

        ## There's no way to take out a comparison at the moment, and we
        ## set all the comparisons for the first run of a category when
        ## we read the CSV file, so if there isn't a run already we just
        ## set the last run to be the PB splits. It doesn't matter 
        ## because the PB splits are all '-' anyway
        if len(self.completeCsv[0]) > 1:
          self.compares.append(self.getTimes(2,self.completeCsv))
          self.compareSplits.append(self.getTimes(1,self.completeCsv))
        else: 
          self.compares.append(self.getTimes(2,self.comparesCsv))
          self.compareSplits.append(self.getTimes(1,self.comparesCsv))
        self.splitCompareHeaders.append("Last Run Splits")
        self.compareHeaders.append("Last Run")

        self.numComparisons = len(self.compareHeaders)
        
        for i in range(self.numComparisons):
            self.diffs.append(Timelist.Timelist())
            self.diffSplits.append(Timelist.Timelist())
        
        self.currentSplits = Timelist.Timelist()
        self.currentTotals = Timelist.Timelist()

        if self.config["numSplits"] > len(self.splitnames):
            self.config["numSplits"] = len(self.splitnames)
            self.config["activeSplit"] = len(self.splitnames) - 2

        self.windowStart = max(0,self.config["numSplits"]-len(self.splitnames))

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
        times = Timelist.Timelist()
        for i in range(1,len(toCheck)):
            times.insert(Time.Time(5,timestring=toCheck[i][col]))
        return times

    def getWindowStart(self):
        if self.splitnum <= self.config["activeSplit"] - 1:
            return 0
        if self.splitnum >= len(self.splitnames) - (self.config["numSplits"]-self.config["activeSplit"]):
            return len(self.splitnames) - self.config["numSplits"]
        return self.splitnum - (self.config["activeSplit"] - 1)

    def getBests(self):
        bests = Timelist.Timelist()
        for i in range(self.currentSplits.length):
            if (self.currentSplits.get(i).greater(self.compareSplits[0].get(i)) > 0 and not self.compareSplits[0].get(i).equal(Time.Time(5,timestring='-'))) or self.currentSplits.get(i).equal(Time.Time(5,timestring='-')):
                bests.insert(self.compareSplits[0].get(i))
            else:
                bests.insert(self.currentSplits.get(i))
        return bests

    def getAverages(self):
        averages = Timelist.Timelist()
        for i in range(self.currentSplits.length):
            average = Timelist.Timelist()
            for j in range(int((len(self.completeCsv[0])-1)/2)):
                average.insert(Time.Time(5,timestring=self.completeCsv[i+1][2*j+1]))
            average.insert(self.currentSplits.get(i))
            averages.insert(average.average())
        return averages

    def isPB(self):
        if self.currentSplits.lastNonZero()> self.compares[2].lastNonZero():
            return 1
        if self.currentSplits.lastNonZero() < self.compares[2].lastNonZero():
            return 0
        if self.compares[2].get(-1).greater(self.currentTotals.get(-1)) == 1:
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
        self.fillTimes(self.currentSplits)
        self.fillTimes(self.currentTotals)
        bests = self.getBests()
        averages = self.getAverages()
        if self.isPB():
            pbSplits = [self.currentSplits.toStringList(),self.currentTotals.toStringList()]
        else:
            pbSplits = [self.compareSplits[2].toStringList(),self.compares[2].toStringList()]
        bestSplits = [bests.toStringList(), bests.getSums().toStringList()]
        averageSplits = [averages.toStringList(), averages.getSums().toStringList()]
        lastRun = [self.currentSplits.toStringList(),self.currentTotals.toStringList()]
        self.completeCsv[0].insert(1,"Run #"+str(int((len(self.completeCsv[1])+1)/2)))
        self.completeCsv[0].insert(2,"Totals")
        self.replaceCsvLines([self.splitnames],0,self.completeCsv)
        self.replaceCsvLines(bestSplits,1,self.comparesCsv)
        self.replaceCsvLines(averageSplits,3,self.comparesCsv)
        self.replaceCsvLines(pbSplits,5,self.comparesCsv)
        self.insertCsvLines(lastRun,1)
        fileio.writeCSV(self.config["baseDir"],self.game,self.category,self.completeCsv,self.comparesCsv)
        print("Close the window to end the program")
