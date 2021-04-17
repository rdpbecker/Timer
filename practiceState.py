import categorySelection as cate, fileio
import readConfig as rc
import SumList
import timeHelpers as timeh

class State:
    started = False
    finished = False

    starttime = 0

    splitnum = 0
    splitnames = []

    game = ""
    category = ""

    completeCsv = None
    comparesCsv = None

    bestTime = 0

    config = None

    def __init__(self):
        self.config = self.getConfigAndSplits()

        splitArrs = fileio.csvReadStart(self.config["baseDir"],self.game,self.category,self.splitnames)
        self.completeCsv = splitArrs[0]
        self.comparesCsv = splitArrs[1]

        self.getPracticeSplits()

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
    ## Get the split number and the best time for that split,
    ## and set the appropriate values in the state.
    ##########################################################
    def getPracticeSplits(self):
        startSplitName = cate.readThingInList(self.splitnames)
        self.splitnum = self.splitnames.index(startSplitName)
        bestTimes = self.getTimes(1,self.comparesCsv)
        self.bestTime = bestTimes[self.splitnum]

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
    ## Do the state update when the run starts
    ##
    ## Parameters: time - the time the run started
    ##########################################################
    def startRun(self,time):
        self.starttime = time
        self.started = True
        self.finished = False

    ##########################################################
    ## Do the state update when the split is ended
    ##
    ## Parameters: time - the time the split was ended
    ##########################################################
    def onSplitEnd(self,time):
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
