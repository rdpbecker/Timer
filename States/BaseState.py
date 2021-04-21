from util import fileio
from util import categorySelection as cate
from util import timeHelpers as timeh
from util import readConfig as rc

class State:
    started = False
    paused = False
    reset = False
    runEnded = False
    finished = False

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

    def __init__(self):
        self.config = self.getConfigAndSplits()

        splitArrs = fileio.csvReadStart(self.config["baseDir"],self.game,self.category,self.splitnames)
        self.completeCsv = splitArrs[0]
        self.comparesCsv = splitArrs[1]

    def _cleanState(self):
        self.started = False
        self.paused = False
        self.reset = False
        self.runEnded = False
        self.finished = False

        self.starttime = 0
        self.segmentTime = 0
        self.totalTime = 0

        self.splitnum = 0

    ##########################################################
    ## Gets the global configuration, game, category, and splits.
    ## Sets the game, category, and splitnames.
    ##
    ## Returns: The final version of the configuration
    ##########################################################
    def getConfigAndSplits(self):
        config = rc.getUserConfig()
        splitnames = cate.getSplitNames(config["baseDir"])
        self.game = splitnames["game"]
        self.category = splitnames["category"]
        self.splitnames = splitnames["splits"]
        self.numSplits = len(self.splitnames)
        config = rc.mergeConfigs(config,rc.getGameConfig(config["baseDir"],self.game,self.category))
        return config

    ##########################################################
    ## Reads a column of times in from a specified array
    ##
    ## Parameters: col - the column to read
    ##             csv_ref - the array to read from
    ##########################################################
    def getTimes(self,col,csv_ref):
        times = []
        for i in range(1,len(csv_ref)):
            times.append(timeh.stringToTime(csv_ref[i][col]))
        return times

    ##########################################################
    ## Replaces the elements of a CSV, starting with a specified
    ## column.
    ## 
    ## Parameters: lines - the new data to put in
    ##             startIndex - the column to start replacing at
    ##             csv_ref - the CSV to replace data in
    ##########################################################
    def replaceCsvLines(self,lines,startIndex,csv_ref):
        for i in range(1,len(csv_ref)):
            for j in range(len(lines)):
                csv_ref[i][startIndex+j]=lines[j][i-1]

    ##########################################################
    ## Inserts new lines into the completeCsv starting with a
    ## specified column.
    ##
    ## Parameters: lines - the new data to put in
    ##             startIndex - the column to start inserting at
    ##########################################################
    def insertCsvLines(self,lines,startIndex):
        for i in range(1,len(self.completeCsv)):
            for j in range(len(lines)):
                self.completeCsv[i].insert(startIndex+j,lines[j][i-1])

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
