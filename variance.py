global varianceList

def printLines(lines):
  for line in lines:
    print(line.__str__())

def getSplitNames():
    splitNames = cate.findAllSplits()
    names = cate.findNames(splitNames,0)
    game = cate.readThingInList(names)
    cate.restrictCategories(splitNames,game)
    categories = cate.findNames(splitNames,1)
    category = cate.readThingInList(categories)
    splitnames = cate.findGameSplits(splitNames,category)
    fileio.stripEmptyStrings(splitnames)
    return [game,category,splitnames]

def cutStart(csv):
  for i in range(len(csv)):
    csv[i] = csv[i][7:]

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
    timeList = Timelist.Timelist()
    for j in range(len(completeCsv[i])):
      timeList.insert(Time.Time(5,timestring=completeCsv[i][j]))
    rows.append(timeList)
  return rows

def sort(i):
  return varianceList[i]

def main():
  global varianceList
  [game,category,splitnames] = getSplitNames()
  completeCsv = fileio.csvReadStart(game,category,splitnames)
  completeCsv = completeCsv[1:]
  cutStart(completeCsv)
  completeCsv = filterEven(completeCsv)
  timeRows = getRows(completeCsv)
  varianceList = []
  for row in timeRows:
    avg = row.average().toSecs()
    secsList = [x.toSecs() for x in row.timelist]
    filtered = [x for x in secsList if not x == 0]
    varList = [(x-avg)**2 for x in filtered]
    variance = sum(varList)/len(varList)
    varianceList.append(100*variance/avg)
  print("In Order:\n\n")
  printLines(splitnames[i]+": "+'%.3f'%(varianceList[i])+"%" for i in range(len(varianceList)))

  print("\n\n\nSorted:\n\n")
  sortedRange = sorted(list(range(len(varianceList))),key=sort,reverse=True)
  printLines(splitnames[i]+": "+'%.3f'%(varianceList[i])+"%" for i in sortedRange) 

if __name__ == "__main__":
  import categorySelection as cate
  import fileio
  import Time, Timelist
  main()
