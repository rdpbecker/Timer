import Time, Timelist, categorySelection as cate, fileio

class State:
    started = False
    finished = False
    starttime = 0
    splitstarttime = 0
    splitnum = 0
    splitnames = []
    game = ""
    category = ""
    completeCsv = None
    bptList = None
    diffs = None
    diffSplits = None
    currentSplits = None
    currentTotals = None
    windowStart = 0

    def __init__(self):
        self.getSplitNames()

        self.completeCsv = fileio.csvReadStart(self.game,self.category,self.splitnames)

        self.bptList = self.getTimes(1)
        
        self.getPracticeSplits()

        self.diffs = Timelist.Timelist()
        self.diffSplits = Timelist.Timelist()
        
        self.currentSplits = Timelist.Timelist()
        self.currentTotals = Timelist.Timelist()

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

    def getPracticeSplits(self):
        startSplitName = cate.readThingInList(self.splitnames)
        self.startSplitIndex = self.splitnames.index(startSplitName)
        self.splitnames = self.splitnames[self.startSplitIndex]
        newBptList = Timelist.Timelist()
        newBptList.insert(self.bptList.get(self.startSplitIndex))
        self.bptList = newBptList

    def replaceCsvLines(self,lines,start):
        for i in range(1,len(self.completeCsv)):
            for j in range(len(lines)):
                self.completeCsv[i][start+j]=lines[j][i-1]
