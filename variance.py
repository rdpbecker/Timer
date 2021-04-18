global varianceList

def printLines(lines):
    for line in lines:
        print(line)

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

def main():
    global varianceList
    config = fileio.getUserConfig()
    splits = cate.getSplitNames(config["baseDir"])
    completeCsv = fileio.csvReadStart(config["baseDir"],splits["game"],splits["category"],splits["splits"])[0]
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
    print("In Order:\n\n")
    printLines(splits["splits"][i]+": "+'%.3f'%(varianceList[i])+"%" for i in range(len(varianceList)))

    print("\n\n\nSorted:\n\n")
    sortedRange = sorted(list(range(len(varianceList))),key=sort,reverse=True)
    printLines(splits["splits"][i]+": "+'%.3f'%(varianceList[i])+"%" for i in sortedRange)

if __name__ == "__main__":
    from util import categorySelection as cate
    from util import fileio
    from util import timeHelpers as timeh
    main()
