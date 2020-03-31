import Time, Timelist, gui, categorySelection as cate, fileio 

guiComplete=0

class State:
    started = False
    starttime = 0
    splitstarttime = 0
    splitnum = 0
    splitnames = []
    game = ""
    category = ""
    completeCsv = None
    bptList = None
    compares = []
    compareSplits = []
    diffs = []
    diffSplits = []
    currentSplits = None
    currentTotals = None
    reset = False
    currentCompare = 2
    compareHeaders = ["Sum of Bests", "Average", "Personal Best", "Last Run"]
    splitCompareHeaders = ["Best Split", "Average Split", "PB Split", "Last Run Split"]
    windowStart = 0
    config = None

    def __init__(self,pbstart,splitstart,config):
        self.config = config
        self.getSplitNames()

        self.completeCsv = fileio.csvReadStart(self.game,self.category,self.splitnames)

        self.bptList = self.getTimes(1)
        
        for i in range(3):
            self.compares.append(self.getTimes(2*i+2))
            self.compareSplits.append(self.getTimes(2*i+1))

        ## There's no way to take out a comparison at the moment, and we
        ## set all the comparisons for the first run of a category when
        ## we read the CSV file, so if there isn't a run already we just
        ## set the last run to be the PB splits. It doesn't matter 
        ## because the PB splits are all '-' anyway
        if len(self.completeCsv[0]) > 7:
          self.compares.append(self.getTimes(8))
          self.compareSplits.append(self.getTimes(7))
        else: 
          self.compares.append(self.getTimes(6))
          self.compareSplits.append(self.getTimes(5))
        
        for i in range(4):
            self.diffs.append(Timelist.Timelist())
            self.diffSplits.append(Timelist.Timelist())
        
        self.currentSplits = Timelist.Timelist()
        self.currentTotals = Timelist.Timelist()
        self.windowStart = config["numSplits"]-min(pbstart-splitstart-1, self.compares[0].length)

    def getSplitNames(self):
        splitNames = cate.findAllSplits()
        names = cate.findNames(splitNames,0)
        self.game = cate.readThingInList(names)
        cate.restrictCategories(splitNames,self.game)
        categories = cate.findNames(splitNames,1)
        self.category = cate.readThingInList(categories)
        self.splitnames = cate.findGameSplits(splitNames,self.category)
        fileio.stripEmptyStrings(self.splitnames)

    def getTimes(self,col):
        times = Timelist.Timelist()
        for i in range(1,len(self.completeCsv)):
            times.insert(Time.Time(5,timestring=self.completeCsv[i][col]))
        return times

    def getWindowStart(self):
        if self.splitnum <= self.config["activeSplit"]-1:
            return 0
        if self.splitnum >= len(self.splitnames) - (self.config["numSplits"]-self.config["activeSplit"]):
            return len(self.splitnames) - self.config["numSplits"]
        return self.splitnum - 2

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
            for j in range((len(self.completeCsv[0])-7)/2):
                average.insert(Time.Time(5,timestring=self.completeCsv[i+1][2*j+7]))
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

    def replaceCsvLines(self,lines,start):
        for i in range(1,len(self.completeCsv)):
            for j in range(len(lines)):
                self.completeCsv[i][start+j]=lines[j][i-1]

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
        self.completeCsv[0].insert(7,"Run #"+str((len(self.completeCsv[1])-5)/2))
        self.completeCsv[0].insert(8,"Totals")
        self.replaceCsvLines([self.splitnames],0)
        self.replaceCsvLines(bestSplits,1)
        self.replaceCsvLines(averageSplits,3)
        self.replaceCsvLines(pbSplits,5)
        self.insertCsvLines(lastRun,7)
        fileio.writeCSV(self.game,self.category,self.completeCsv)
        print "Close the window to end the program"
