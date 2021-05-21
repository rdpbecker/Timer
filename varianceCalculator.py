from util import fileio
from util import timeHelpers as timeh
from util import readConfig as rc
global varianceList

def cutStart(csv):
    for i in range(len(csv)):
        csv[i] = csv[i][1:]

def filterEven(csv):
    new = []
    for i in range(len(csv)):
        line = []
        for j in range(len(csv[i])):
            if not j%2:
                line.append(csv[i][j])
        new.append(line)
    return new

def getRows(completeCsv):
    rows = []
    for i in range(len(completeCsv)):
        timeList = []
        for j in range(len(completeCsv[i])):
            time = timeh.stringToTime(completeCsv[i][j])
            if not timeh.isBlank(time):
                timeList.append(time)
        rows.append(timeList)
    return rows

def sort(i):
    return varianceList[i]

def createTable(names,variances,sort):
    table = []
    for i in sort:
        table.append([names[i],variances[i]])
    return table

def computeVariances(game,category,splits):
    global varianceList
    config = rc.getUserConfig()
    splitNames = splits.getSplitNames(game,category)
    completeCsv = fileio.csvReadStart(config["baseDir"],game,category,splitNames)[0]
    completeCsv = completeCsv[1:]
    cutStart(completeCsv)
    completeCsv = filterEven(completeCsv)
    timeRows = getRows(completeCsv)
    varianceList = []
    for row in timeRows:
        avg = sum(row)/len(row)
        varList = [(x-avg)**2 for x in row]
        variance = sum(varList)/len(varList)
        varianceList.append(100*variance/avg)
    sortedRange = sorted(list(range(len(varianceList))),key=sort,reverse=True)

    return {\
        "order": createTable(splitNames,varianceList,range(len(varianceList))),\
        "sorted": createTable(splitNames,varianceList,sortedRange)\
    }
