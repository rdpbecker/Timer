import csv, sys
from util import readConfig as rc
from util import fileio

class Splits:
    indexDict = None
    splitNames = None
    splitsFile = ""

    def __init__(self):
        config = rc.getUserConfig()
        self.indexDict = {}
        self.splitNames = []
        self.splitsFile = config["baseDir"] + "/splitNames.csv"
        csvLines = fileio.readCsv(self.splitsFile)
        for i in range(len(csvLines)):
            if not i:
                game = csvLines[i][0]
                gameDict = {}
            elif csvLines[i][0] and i:
                self.indexDict[game] = gameDict
                game = csvLines[i][0]
                gameDict = {}
            gameDict[csvLines[i][1]] = i
            self.splitNames.append(csvLines[i])

    def getSplitNames(self,game,category):
        if not game or not category:
            return []
        return self.splitNames[self.indexDict[game][category]][2:]

    def getGames(self):
        return list(self.indexDict.keys())

    def getCategories(self,game):
        if not game:
            return []
        return list(self.indexDict[game].keys())

    def updateNames(self,game,category,names,write=True):
        if not game in self.getGames():
            addNewGame(game,category,names)
        elif category not in self.getCategories(game):
            addNewCategory(game,category,names)
        else:
            updateExistingCategory(game,category,names)

        if write:
            fileio.writeCSV(self.splitsFile,self.splitNames)
        else:
            for line in self.splitNames:
                print(line)

    def addNewGame(self,game,category,names):
        self.index[game] = {}
        self.index[category] = len(self.splitNames)
        newNames = [game,category]
        newNames.extend(names)
        self.splitNames.append(newNames)

    def addNewCategory(self,game,category,names):
        cateIndex = max([self.indexDict[game][cate] for cate in self.getCategories(game)])
        self.indexDict[game][category] = cateIndex
        newNames = ["",category]
        newNames.extend(names)
        self.splitNames.insert(cateIndex,newNames)

    def updateExistingCategory(self,game,category,names):
        newNames = self.splitNames[self.indexDict[game][category]][:2]
        newNames.extend(names)
        self.splitNames[self.indexDict[game][category]] = newNames
