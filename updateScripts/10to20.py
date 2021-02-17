import categorySelection as cate
import fileio
import os, csv

def csvReadStart(name,category):
    csvName = "../" + name + "/" + category + ".csv"
    compareCsvName = "../" + name + "/" + category + "_comparisons.csv"
    splitWrite = []

    with open(csvName,'r') as reader:
        csvReader = csv.reader(reader, delimiter = ',')
        for row in csvReader:
            splitWrite.append(row)
    return splitWrite

def getColumnsWithNames(csvLines,start,end):
    new  = []
    for row in csvLines:
        new_row = [row[0]]
        new_row.extend(row[start:end+1])
        new.append(new_row)
    return new

def removeColumns(csvLines,start,end):
    new = []
    for row in csvLines:
        new_row = row[:start]
        new_row.extend(row[end+1:])
        new.append(new_row)
    return new

def copy(arr):
    new = []
    for thing in arr:
        new.append(thing)
    return new

def main():
    splitNames = cate.findAllSplits()
    names = cate.findNames(splitNames,0)
    flag = False
    for game in names:
        splits_copy = copy(splitNames)
        cate.restrictCategories(splits_copy,game)
        categories = cate.findNames(splits_copy,1)
        for category in categories: 
            if os.path.exists("../"+game+"/"+category+".csv") and not os.path.exists("../"+game+"/"+category+"_comparisons.csv"):
                print(game, category)
                csvLines = csvReadStart(game,category)
                comparisons = getColumnsWithNames(csvLines,1,6)
                base = removeColumns(csvLines,1,6)
                fileio.writeCSV(game,category,removeColumns(csvLines,1,6),getColumnsWithNames(csvLines,1,6))

main()
