from util import timeHelpers as timeh

class Comparison:
    segmentHeader = ""
    totalHeader = ""
    segments = []
    totals = []
    segmentDiffs = []
    totalDiffs = []

    def __init__(self,shead,thead,segments,totals):
        self.segmentHeader = shead
        self.totalHeader = thead
        self.segments = segments
        self.totals = totals
        self.segmentDiffs = []
        self.totalDiffs = []

    def getString(self,name,index,options={}):
        if (name == "segments"):
            return timeh.timeToString(self.segments[index],options)
        if (name == "totals"):
            return timeh.timeToString(self.totals[index],options)
        if (name == "segmentDiffs"):
            return timeh.timeToString(self.segmentDiffs[index],options)
        if (name == "totalDiffs"):
            return timeh.timeToString(self.totalDiffs[index],options)
        return "BLANK"

    def updateDiffs(self,splittime,totaltime):
        if (not(len(self.segmentDiffs)) or not timeh.isBlank(self.totalDiffs[-1])):
            self.segmentDiffs.append(timeh.difference(splittime,self.segments[len(self.segmentDiffs)]))
        else:
            self.segmentDiffs.append("BLANK")
        self.totalDiffs.append(timeh.difference(totaltime,self.totals[len(self.totalDiffs)]))

    def lastNonBlank(self):
        for i in range(len(self.totals)-1,-1,-1):
            if not timeh.isBlank(self.totals[i]):
                return i
        return -1
