import csv, sys
from util import fileio

generalHeader = "Please enter a value from the following list:"

allSplits = []

def setGlobalSplits(baseDir):
    csvlines = findAllSplits(baseDir)
    global allSplits
    for i in len(csvlines):
        singleLine = []
        for j in len(csvlines[i]):
            singleLine.append(csvlines[i][j])
        allSplits.append(singleLine)

def findAllSplits(baseDir):
    csvname = baseDir + "/splitNames.csv"
    with open(csvname,'r') as csvfile:
        thereader = csv.reader(csvfile, delimiter=",",quotechar="|")
        csvlines = []
        for row in thereader:
            csvlines.append(row)
    return csvlines

def findNames(csvlines,index):
    names = []
    for row in csvlines:
        if row[index]:
            names.append(row[index])
    return names

def findGames():
    games = []
    for row in csvlines:
        if row[0]:
            names.append(row[0])
    return games

def findCategories(game):
    games = []
    for row in csvlines:
        if row[0]:
            names.append(row[0])
    return games

def getGameBounds(csvLines,game):
    start = 0
    while not csvLines[start][0] == game:
        start = start + 1
    end = start + 1
    while not csvLines[end][0] and not end >= len(csvLines):
        end = end + 1
    return {"start": start, "end": end}

def restrictCategories(csvlines,game):
    while csvlines[0][0] != game:
        csvlines.pop(0)
    categories = [csvlines[0][1]]
    count = 1
    while count < len(csvlines) and not csvlines[count][0]:
        categories.append(csvlines[count])
        count = count + 1
    count = count - 1
    while csvlines[count] != csvlines[-1]:
        csvlines.pop(-1)

def findGameSplits(csvlines,category):
    for splits in csvlines:
        if splits[1] == category:
            return splits[2:]

def readThingInList(aList,header=generalHeader):
    print(header)
    print(aList)
    thing = sys.stdin.readline()[:-1]
    while not thing in aList:
        print("Not an option. Your options are: ")
        print(aList)
        thing = sys.stdin.readline()[:-1]
    return thing

def getSplitNames(baseDir):
    splitNames = findAllSplits(baseDir)
    names = findNames(splitNames,0)
    game = readThingInList(names, "Pick a game:")
    restrictCategories(splitNames,game)
    categories = findNames(splitNames,1)
    category = readThingInList(categories, "Pick a category:")
    splitnames = findGameSplits(splitNames,category)
    fileio.stripEmptyStrings(splitnames)
    return { \
        "game": game,\
        "category": category,\
        "splits": splitnames\
    }
