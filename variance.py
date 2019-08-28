def getSplitNames(self):
    splitNames = cate.findAllSplits()
    names = cate.findNames(splitNames,0)
    self.game = cate.readThingInList(names)
    cate.restrictCategories(splitNames,self.game)
    categories = cate.findNames(splitNames,1)
    self.category = cate.readThingInList(categories)
    self.splitnames = cate.findGameSplits(splitNames,self.category)
    fileio.stripEmptyStrings(self.splitnames)

