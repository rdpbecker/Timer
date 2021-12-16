import copy

class SplitList:
    def __init__(self,names):
        self.splits, self.groups = self.parseSplits(names)
        self.visibleSplits = 0
        self.visuallyActive = 0
        self.numSplits = len(names)
        self.topSplitIndex = 0
        self.typeChecker = TypeChecker()
        self.currentSplits = []
        self.activeIndex = 0

    def parseSplits(self,names):
        splits = []
        groups = []
        groupStart = -1
        for i in range(len(names)):
            if names[i][0:2] == "- ":
                truename = names[i][2:]
                if groupStart < 0:
                    groupStart = i
                if "{" in names[i] and "}" in names[i]:
                    groups.append(SplitGroup(groupStart,i,names[i].split("{")[1].split("}")[0]))
                    truename = truename.split("{")[0]
                    groupStart = -1
                splits.append(Split(i,truename,True))
            else:
                splits.append(Split(i,names[i]))
                groupStart = -1
        return splits, groups

    def setVisualConfig(self,numSplits,visuallyActive):
        self.visibleSplits = numSplits
        self.visuallyActive = visuallyActive

    def updateCurrent(self,currentSplit):
        self.setTopSplitIndex(currentSplit)
        if currentSplit == self.numSplits:
            group = copy.deepcopy(self.groups[-1])
        else:
            group = self.findGroup(currentSplit)
        subs = []
        if group:
            subs = self.splits[group.start:group.end+1]
        available = self.synthesizeSplits(subs)
        availableIndex = self.findSplit(available,currentSplit)
        topSplitIndex = self.trueTopSplitIndex(availableIndex,len(available))
        self.activeIndex = availableIndex - topSplitIndex
        self.currentSplits = available[topSplitIndex:topSplitIndex+self.visibleSplits-1] + [available[-1]]

    def findGroup(self,index):
        for group in self.groups:
            if group.start <= index and group.end >= index:
                return copy.deepcopy(group)
        return None

    def findSplit(self,available,index):
        for i in range(len(available)):
            split = available[i]
            if not self.typeChecker.isNormal(split):
                continue
            if split.index == index:
                return i
        return -1

    def synthesizeSplits(self,openSubsplits):
        topLevel = self.getTopLevelSplits()
        if not len(openSubsplits):
            while len(topLevel) < self.visibleSplits:
                topLevel.insert(len(topLevel)-1,EmptySplit())
            return topLevel

        i = 0
        while i < len(topLevel) and len(openSubsplits):
            split = topLevel[i]
            if self.typeChecker.isNormal(split):
                if openSubsplits[0].index < split.index:
                    topLevel.insert(i,copy.deepcopy(openSubsplits.pop(0)))
            elif self.typeChecker.isGroup(split):
                if openSubsplits[0].index < split.start:
                    topLevel.insert(i,copy.deepcopy(openSubsplits.pop(0)))
            i = i + 1
        topLevel = topLevel + copy.deepcopy(openSubsplits)
        while len(topLevel) < self.visibleSplits:
            topLevel.insert(len(topLevel)-1,EmptySplit())
        return topLevel

    def getTopLevelSplits(self):
        topLevel = []
        i = 0
        while i < len(self.splits):
            group = self.findGroup(i)
            if group:
                topLevel.append(group)
                i = group.end
            else:
                topLevel.append(copy.deepcopy(self.splits[i]))
            i = i + 1
        return topLevel

    def setTopSplitIndex(self,current):
        if current <= self.visuallyActive - 1:
            self.topSplitIndex = 0
        elif current >= self.numSplits - (self.visibleSplits-self.visuallyActive):
            self.topSplitIndex = self.numSplits - self.visibleSplits
        else:
            self.topSplitIndex = current - (self.visuallyActive - 1)

    def trueTopSplitIndex(self,current,available):
        if current <= self.visuallyActive - 1:
            return 0
        elif current >= available - (self.visibleSplits-self.visuallyActive):
            return available - self.visibleSplits
        else:
            return current - (self.visuallyActive - 1)

    def __str__(self):
        string = ""
        for split in self.splits:
            string = string + str(split) + "\n"
        for group in self.groups:
            string = string + str(group) + "\n"
        return string

class Split:
    def __init__(self,index,name,isSub=False):
        self.index = index
        self.name = name
        self.subsplit = isSub

    def __str__(self):
        return "Name: " + self.name + " | Index: " + str(self.index)

class SplitGroup:
    def __init__(self,start,end,name):
        self.start = start
        self.end = end
        self.name = name
        self.count = end - start + 1

    def __str__(self):
        return "Name: " + self.name + " | Indexes: " + str(self.start) + "-" + str(self.end)

class EmptySplit:
    def __init__(self):
        pass

    def __str__(self):
        return "Empty split"

class TypeChecker():
    def __init__(self):
        pass

    def isNormal(self,obj):
        return type(obj) == Split

    def isGroup(self,obj):
        return type(obj) == SplitGroup

    def isEmpty(self,obj):
        return type(obj) == EmptySplit
