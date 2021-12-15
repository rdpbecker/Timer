class SplitList:
    def __init__(self,names):
        self.splits = self.parseSplits(names)
        self.visibleSplits = 0
        self.visuallyActive = 0
        self.numSplits = len(names)
        self.topSplitIndex = 0

    def parseSplits(self,names):
        splits = []
        for i in range(len(names)):
            splits.append(Split(i,names[i]))
        return splits

    def setVisualConfig(self,numSplits,visuallyActive):
        self.visibleSplits = numSplits
        self.visuallyActive = visuallyActive

    def getSplits(self,current):
        self.setTopSplitIndex(current)
        return self.splits[self.topSplitIndex:self.topSplitIndex+self.visibleSplits-1] + [self.splits[-1]]

    def setTopSplitIndex(self,current):
        if current <= self.visuallyActive - 1:
            self.topSplitIndex = 0
        elif current >= self.numSplits - (self.visibleSplits-self.visuallyActive):
            self.topSplitIndex = self.numSplits - self.visibleSplits
        else:
            self.topSplitIndex = current - (self.visuallyActive - 1)

class Split:
    def __init__(self,index,name):
        self.index = index
        self.name = name

    def __str__(self):
        return "Name: " + self.name + " | Index: " + str(self.index)
