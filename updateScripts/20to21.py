from util import fileio
from util import readConfig as rc
from util import categorySelection as cate
from util import timeHelpers as timeh
from DataClasses import DifferenceList

def insertCsvLines(lines,startIndex,csv_ref):
    for i in range(len(csv_ref)):
        for j in range(len(lines[i])):
            csv_ref[i].insert(startIndex+j,lines[i][j])

def findBestExit(splitnum,complete):
    minVal = 100000000
    for i in range(int((len(complete[0])-1)/2)):
        val = timeh.stringToTime(complete[splitnum+1][2*i+2])
        if(timeh.isBlank(val)):
            continue
        if val < minVal:
            minVal = val
    if minVal == 100000000:
        return 'BLANK'
    return minVal

def copy(arr):
    new = []
    for thing in arr:
        new.append(thing)
    return new

def main():
    config = rc.getUserConfig()
    splitNames = cate.findAllSplits(config["baseDir"])
    names = cate.findNames(splitNames,0)
    for game in names:
        splits_copy = copy(splitNames)
        cate.restrictCategories(splits_copy,game)
        categories = cate.findNames(splits_copy,1)
        for category in categories:
            print(game,category)
            splitArrs = fileio.csvReadStart(config["baseDir"],game,category,[])
            if len(splitArrs[0]) == 1:
                continue
            comparesCsv = splitArrs[1]

            newCompares = [['To Best Exit','Best Exit']]
            bestExits = DifferenceList.DifferenceList([findBestExit(i,splitArrs[0]) for i in range(len(comparesCsv)-1)])
            for i in range(len(comparesCsv)-1):
                newCompares.append([timeh.timeToString(bestExits.segments[i],{"precision":5}),timeh.timeToString(bestExits.totals[i],{"precision":5})])
            insertCsvLines(newCompares,7,comparesCsv)

            newCompares = [['Blank Split','Blank']]
            newCompares.extend(['-','-'] for _ in range(len(comparesCsv)-1))
            insertCsvLines(newCompares,9,comparesCsv)

            fileio.writeCSVs(config["baseDir"],game+"tmp",category,None,comparesCsv)

main()
