import os, csv
import json

def resolveFilename(arr):
    return "/".join(arr)

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
            'Personal Best' \
        ]]
        for thing in splitList:
            splitWrite[1].append([thing,'-','-','-','-','-','-'])
        with open(compareCsvName,'w') as writer:
            csvWriter = csv.writer(writer, delimiter = ',')
            for thing in splitWrite[1]:
                csvWriter.writerow(thing)

    else:
        with open(compareCsvName, 'r') as reader:
            csvReader = csv.reader(reader, delimiter = ',')
            for row in csvReader:
                splitWrite[1].append(row)

    return splitWrite

def writeCSV(baseDir,name,category,splitWrite,comparesWrite):
    csvName = resolveFilename([baseDir,name,category + ".csv"])
    compareCsvName = resolveFilename([baseDir,name,category + "_comparisons.csv"])
    with open(csvName,'w') as writer:
        csvWriter = csv.writer(writer, delimiter = ',')
        for thing in splitWrite:
            csvWriter.writerow(thing)

    with open(compareCsvName,'w') as writer:
        csvWriter = csv.writer(writer, delimiter = ',')
        for thing in comparesWrite:
            csvWriter.writerow(thing)

def stripEmptyStrings(stringList):
    while not stringList[-1]:
        stringList.pop(-1)

def readJson(filepath):
    with open(filepath,'r') as reader:
        data = json.load(reader)
    return data
