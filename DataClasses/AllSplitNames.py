import csv, sys
from util import readConfig as rc
from util import fileio

class Splits:
    indexDict = None
    splitNames = None

    def __init__(self):
        config = rc.getUserConfig()
        self.indexDict = {}
        self.splitNames = []
        csvLines = fileio.readCsv(config["baseDir"] + "/splitNames.csv")
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
