import os, csv, json
from util import dataManip

def resolveFilename(arr):
    return "/".join(arr)

def getDir(string):
    return resolveFilename(string.split("/")[:-1])

def csvReadStart(baseDir,name,category,splitList):
    csvName = resolveFilename([baseDir,name,category + ".csv"])
    compareCsvName = resolveFilename([baseDir,name,category + "_comparisons.csv"])
    splitWrite = [[],[]]
    if not os.path.exists(csvName):
        if not os.path.isdir(resolveFilename([baseDir,name])):
            os.mkdir(resolveFilename([baseDir,name]))
        splitWrite[0] = [['Split Names']]
        for thing in splitList:
            splitWrite[0].append([thing])
        with open(csvName,'w') as writer:
            csvWriter = csv.writer(writer, delimiter = ',')
            for thing in splitWrite[0]:
                csvWriter.writerow(thing)

    else:
        with open(csvName,'r') as reader:
            csvReader = csv.reader(reader, delimiter = ',')
            for row in csvReader:
                splitWrite[0].append(row)
        splitWrite[0] = dataManip.adjustNames(splitList,splitWrite[0])

    if not os.path.exists(compareCsvName):
        if not os.path.isdir(resolveFilename([baseDir,name])):
            os.mkdir(resolveFilename([baseDir,name]))
        splitWrite[1] = [[ \
            'Split Names', \
            'Best Split', \
            'Sum of Bests', \
            'Average Split', \
            'Average', \
            'PB Split', \
            'Personal Best',\
            'To Best Exit',\
            'Best Exit',\
            'Blank Split',\
            'Blank'\
        ]]
        for thing in splitList:
            splitWrite[1].append([thing,'-','-','-','-','-','-','-','-','-','-'])
        with open(compareCsvName,'w') as writer:
            csvWriter = csv.writer(writer, delimiter = ',')
            for thing in splitWrite[1]:
                csvWriter.writerow(thing)

    else:
        with open(compareCsvName, 'r') as reader:
            csvReader = csv.reader(reader, delimiter = ',')
            for row in csvReader:
                splitWrite[1].append(row)
        splitWrite[1] = dataManip.adjustNames(splitList,splitWrite[1])

    return splitWrite

def writeCSVs(baseDir,name,category,splitWrite,comparesWrite):
    if splitWrite:
        writeCSV(resolveFilename([baseDir,name,category + ".csv"]),splitWrite)
    if comparesWrite:
        writeCSV(resolveFilename([baseDir,name,category + "_comparisons.csv"]),comparesWrite)

def writeCSV(filename,rows):
    if not os.path.exists(getDir(filename)):
        os.mkdir(getDir(filename))
    with open(filename,'w') as writer:
        csvWriter = csv.writer(writer, delimiter = ',')
        for thing in rows:
            csvWriter.writerow(thing)

def stripEmptyStrings(stringList):
    while not stringList[-1]:
        stringList.pop(-1)

def stripEmptyStringsReturn(stringList):
    if not len(stringList):
        return []
    new = [stringList[i] for i in range(len(stringList))]
    while not new[-1]:
        new.pop(-1)
    return new

def readJson(filepath):
    with open(filepath,'r') as reader:
        data = json.load(reader)
    return data

def writeJson(filepath,data):
    jsonData = json.dumps(data)
    with open(filepath,'w') as writer:
        writer.write(jsonData)

def readCsv(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath,'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=",",quotechar="|")
        csvlines = []
        for row in reader:
            csvlines.append(stripEmptyStringsReturn(row))
    return csvlines

def getLayouts():
    if os.path.exists("layouts"):
        layoutFiles = [f[:-5] for f in os.listdir("layouts")]
        layoutFiles.insert(0,"System Default")
    else:
        layoutFiles = ["System Default"]
    return layoutFiles
