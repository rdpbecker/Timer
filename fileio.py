import os, csv
import json

def csvReadStart(name,category,splitList):
    csvName = "../" + name + "/" + category + ".csv"
    if not os.path.exists(csvName):
        if not os.path.isdir("../" + name):
            os.mkdir("../" + name)
        splitWrite = [['Split Names',"Best Split","Best Split Totals","Average Split","Average Split Total","Best Run Split","Best Run Totals"]]
        for thing in splitList:
            splitWrite.append([thing,"-","-","-","-","-","-"])
        with open(csvName,'w') as writer:
            csvWriter = csv.writer(writer, delimiter = ',')
            for thing in splitWrite:
                csvWriter.writerow(thing)

    else:
        with open(csvName,'r') as reader:
            csvReader = csv.reader(reader, delimiter = ',')
            splitWrite = []
            for row in csvReader:
                splitWrite.append(row)
    return splitWrite

def writeCSV(name,category,splitWrite):
    csvName = "../" + name + "/" + category + ".csv"
    with open(csvName,'w') as writer:
        csvWriter = csv.writer(writer, delimiter = ',')
        for thing in splitWrite:
            csvWriter.writerow(thing)


def stripEmptyStrings(stringList):
    while not stringList[-1]:
        stringList.pop(-1)

def readJson(filepath):
    with open(filepath,'r') as reader:
        data = json.load(reader)
    return data
