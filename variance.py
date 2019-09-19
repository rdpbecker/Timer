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

def main():
  [game,category,splitnames] = getSplitNames()
  completeCsv = fileio.csvReadStart(game,category,splitnames)
  completeCsv = completeCsv[1:]
  cutStart(completeCsv)
  completeCsv = filterEven(completeCsv)

if __name__ == "__main__":
  import categorySelection as cate
  import fileio
  main()
