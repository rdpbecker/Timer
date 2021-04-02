import timeHelpers as timeh

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

    def getString(self,index,name,options={}):
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
        if (not(len(self.segmentDiffs)) or not self.totalDiffs[-1] == "BLANK"):
            self.segmentDiffs.append(timeh.difference(splittime,self.segments[len(self.segmentDiffs)]))
        else:
            self.segmentDiffs.append("BLANK")
        self.totalDiffs.append(timeh.difference(totaltime,self.totals[len(self.totalDiffs)]))
