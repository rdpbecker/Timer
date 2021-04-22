from util import fileio
from util import readConfig as rc
from util import categorySelection as cate

def insertCsvLines(lines,startIndex,csv_ref):
    for i in range(len(csv_ref)):
        for j in range(len(lines[i])):
            csv_ref[i].insert(startIndex+j,lines[i][j])

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

            newCompares = [['To Best Exit','Best Exit','Blank Split','Blank']]
            for i in range(1,len(comparesCsv)):
                newCompares.append(['-','-','-','-'])
            insertCsvLines(newCompares,7,comparesCsv)

            fileio.writeCSVs(config["baseDir"],game+"tmp",category,splitArrs[0],comparesCsv)

main()
