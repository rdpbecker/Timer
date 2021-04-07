import csv, sys, fileio

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

def readThingInList(aList):
    print("Please enter a value from the following list:")
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
    game = readThingInList(names)
    restrictCategories(splitNames,game)
    categories = findNames(splitNames,1)
    category = readThingInList(categories)
    splitnames = findGameSplits(splitNames,category)
    fileio.stripEmptyStrings(splitnames)
    return { \
        "game": game,\
        "category": category,\
        "splits": splitnames\
    }
