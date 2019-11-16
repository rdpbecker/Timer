import Time, Timelist, gui, categorySelection as cate, fileio, config

guiComplete=0

class State:
    started = False
    starttime = 0
    splitstarttime = 0
    splitnum = 0
    splitnames = []
    game = ""
    category = ""
    completeCsv = ""
    bptList = 0 
    compares = []
    compareSplits = []
    diffs = []
    diffSplits = []
    currentSplits = 0
    currentTotals = 0
    reset = 0
    skip = 0
    currentCompare = 2
    compareHeaders = ["Sum of Bests", "Average", "Personal Best", "Last Run"]
    app = 0
    windowStart = 0

    def __init__(self,pbstart,splitstart):
        self.getSplitNames()

        self.completeCsv = fileio.csvReadStart(self.game,self.category,self.splitnames)

        self.bptList = self.getTimes(1)
        
        for i in range(3):
            self.compares.append(self.getTimes(2*i+2))
            self.compareSplits.append(self.getTimes(2*i+1))
        self.compares.append(self.getTimes(-1))
        self.compareSplits.append(self.getTimes(-2))
        
        for i in range(4):
            self.diffs.append(Timelist.Timelist())
            self.diffSplits.append(Timelist.Timelist())
        
        self.currentSplits = Timelist.Timelist()
        self.currentTotals = Timelist.Timelist()
        self.windowStart = 7-min(pbstart-splitstart-1, self.compares[0].length)

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

    def InitGui(self):
        self.InitHeader()
        self.InitTimes()
        self.InitInfo()
        self.updateCurrentColour()

    def InitHeader(self):
        self.app.labels[0][0].configure(text=self.game)
        self.app.labels[0][1].configure(text=self.category)
        self.app.labels[0][2].configure(text="Comparing Against")
        self.app.labels[0][3].configure(text="Personal Best")

    def InitTimes(self):
        for i in range(self.windowStart,self.app.pbstart-self.app.splitstart-2):
            self.app.labels[self.app.splitstart+i][0].configure(text=self.splitnames[i-self.windowStart])
            self.app.labels[self.app.splitstart+i][2].configure(text=self.compares[self.currentCompare].get(i-self.windowStart).__str__(precision=2))
        self.app.labels[self.app.pbstart-2][0].configure(text=self.splitnames[-1])
        self.app.labels[self.app.pbstart-2][2].configure(text=self.compares[self.currentCompare].get(-1).__str__(precision=2))

    def InitInfo(self):
        self.app.labels[self.app.pbstart][0].configure(text="PB Split:")
        self.app.labels[self.app.pbstart+1][0].configure(text="Best Split:")

        self.app.labels[self.app.bptstart][0].configure(text="Possible Time Save:")
        self.app.labels[self.app.bptstart+1][0].configure(text="Last Split (vs Best):")
        self.app.labels[self.app.bptstart+2][0].configure(text="Best Possible Time:")
        self.app.labels[self.app.bptstart+3][0].configure(text="Personal Best:")
        self.app.labels[self.app.bptstart+3][1].configure(text=self.compares[2].get(-1).__str__(precision=2))
        self.updateInfo()

    def startRun(self,start):
        self.start = start

    def onSplitEnd(self,splitEnd,splitTime):
        if self.reset:
            return
        totalTime = Time.Time(5,floattime=splitEnd-self.start)
        if self.skip:
            self.currentSplits.insert(Time.Time(5,timestring='-'))
            self.currentTotals.insert(Time.Time(5,timestring='-'))
        else:
            self.currentSplits.insert(Time.Time(5,floattime=splitTime))
            self.bptList.replace(Time.Time(5,floattime=splitTime),self.splitnum)
            self.currentTotals.insert(Time.Time(5,floattime=splitEnd-self.start))
        for i in range(4):
            if self.skip:
                self.diffs[i].insert(Time.Time(5,timestring='-'))
                self.diffSplits[i].insert(Time.Time(5,timestring='-'))
            else:
                self.diffs[i].insert(totalTime.subtract(self.compares[i].get(self.splitnum)))
                self.diffSplits[i].insert(self.currentSplits.get(self.splitnum).subtract(self.compareSplits[i].get(self.splitnum)))
        self.splitnum = self.splitnum + 1
        lowIndex = self.getWindowStart()
        self.updateTimes(lowIndex)
        self.updateCurrentColour()
        if self.splitnum < len(self.splitnames):
            self.updateInfo()
        self.skip = 0
        config.skip = 0

    def getWindowStart(self):
        if self.splitnum <= 2:
            return 0
        if self.splitnum >= len(self.splitnames) - 4:
            return len(self.splitnames) - 7
        return self.splitnum - 2

    def updateTimes(self,lowIndex):
        for i in range(self.windowStart,self.app.pbstart-self.app.splitstart-2):
            self.app.labels[self.app.splitstart+i][0].configure(text=self.splitnames[i+lowIndex-self.windowStart])
            if self.currentSplits.length > i + lowIndex - self.windowStart:
                if not self.compareSplits[self.currentCompare].get(i+lowIndex-self.windowStart).equal(Time.Time(5,timestring='-')):
                    self.app.labels[self.app.splitstart+i][1].configure(text=self.diffs[self.currentCompare].get(i+lowIndex-self.windowStart).__str__(1,precision=2))
                else:
                    self.app.labels[self.app.splitstart+i][1].configure(text='-')
                self.app.labels[self.app.splitstart+i][2].configure(text=self.currentTotals.get(i+lowIndex-self.windowStart).__str__(precision=2))
                if self.diffSplits[0].get(i+lowIndex-self.windowStart).greater(Time.Time(5,timestring='-')) == -1:
                    self.app.labels[self.app.splitstart+i][1].configure(fg='gold')
                elif (self.diffs[self.currentCompare].get(i+lowIndex-self.windowStart).greater(Time.Time(5,timestring='-')) == -1) or (self.compareSplits[self.currentCompare].get(i+lowIndex-self.windowStart).equal(Time.Time(2,timestring='-'))):
                    self.app.labels[self.app.splitstart+i][1].configure(fg='green')
                else:
                    self.app.labels[self.app.splitstart+i][1].configure(fg='red')
            else:
                self.app.labels[self.app.splitstart+i][1].configure(text="")
                self.app.labels[self.app.splitstart+i][2].configure(text=self.compares[self.currentCompare].get(i+lowIndex-self.windowStart).__str__(precision=2))
        if self.splitnum >= len(self.splitnames):
            self.app.labels[self.app.pbstart-2][1].configure(text=self.diffs[self.currentCompare].get(-1).__str__(1,precision=2))
            self.app.labels[self.app.pbstart-2][2].configure(text=self.currentTotals.get(-1).__str__(precision=2))
            if self.diffs[0].get(-1).greater(Time.Time(5,timestring='-')) == -1:
                self.app.labels[self.app.pbstart-2][1].configure(fg='gold')
            elif self.diffs[self.currentCompare].get(-1).greater(Time.Time(5,timestring='-')) == -1:
                self.app.labels[self.app.pbstart-2][1].configure(fg='green')
            else:
                self.app.labels[self.app.pbstart-2][1].configure(fg='red')

    def updateInfo(self):
        self.app.labels[self.app.pbstart][1].configure(text=self.compareSplits[self.currentCompare].get(self.splitnum).__str__(precision=2))
        self.app.labels[self.app.pbstart+1][1].configure(text=self.compareSplits[0].get(self.splitnum).__str__(precision=2))
        self.app.labels[self.app.bptstart][1].configure(text=self.compareSplits[self.currentCompare].get(self.splitnum).subtract(self.compareSplits[0].get(self.splitnum)).__str__(precision=2))
        if self.splitnum:
            self.app.labels[self.app.bptstart+1][1].configure(text=self.currentSplits.get(-1).subtract(self.compareSplits[0].get(self.splitnum-1)).__str__(1,precision=2))
        if not self.skip:
            self.app.labels[self.app.bptstart+2][1].configure(text=self.bptList.sum().__str__(precision=2))

    def updateCompare(self):
        self.currentCompare = config.choice
        self.app.labels[0][3].configure(text=self.compareHeaders[self.currentCompare])
        self.updateTimes(self.getWindowStart())
        self.app.labels[self.app.pbstart-2][2].configure(text=self.compares[self.currentCompare].get(-1).__str__(precision=2))

    def updateCurrentColour(self):
        for i in range(0,self.app.pbstart-self.app.splitstart-1):
            if i == self.splitnum-self.getWindowStart()+self.windowStart:
                self.app.labels[self.app.splitstart+i][0].configure(fg="DarkOrchid2")
                self.app.labels[self.app.splitstart+i][2].configure(fg="DarkOrchid2")
            else:
                self.app.labels[self.app.splitstart+i][0].configure(fg="white")
                self.app.labels[self.app.splitstart+i][2].configure(fg="white")
        self.app.labels[self.app.pbstart-2][0].configure(fg="maroon1")
        self.app.labels[self.app.pbstart-2][2].configure(fg="maroon1")

    def getBests(self):
        bests = Timelist.Timelist()
        for i in range(self.currentSplits.length):
            if (self.currentSplits.get(i).greater(self.compareSplits[0].get(i)) > 0 and not self.compareSplits[0].get(i).equal(Time.Time(2,timestring='-'))) or self.currentSplits.get(i).equal(Time.Time(5,timestring='-')):
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

    def appendCsvLines(self,lines):
        for i in range(1,len(self.completeCsv)):
            for j in range(len(lines)):
                self.completeCsv[i].append(lines[j][i-1])

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

    def setFlags(self,skip,reset):
        self.skip = skip
        self.reset = reset
