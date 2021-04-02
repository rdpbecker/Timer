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

    def getSegmentHeader(self):
        return self.segmentHeader

    def getTotalHeader(self):
        return self.totalHeader

    def getSegments(self):
        return self.segments

    def getTotals(self):
        return self.totals

    def getSegmentDiffs(self):
        return self.segmentDiffs

    def getTotalDiffs(self):
        return self.totalDiffs

    def getSegment(self,index):
        return self.segments[index]

    def getTotal(self,index):
        return self.totals[index]

    def updateDiffs(self,splittime,totaltime):
        if (not(len(self.segmentDiffs)) or not self.totalDiffs[-1] == "BLANK"):
            self.segmentDiffs.append(timeh.difference(splittime,self.segments[len(self.segmentDiffs)]))
        else:
            self.segmentDiffs.append("BLANK")
        self.totalDiffs.append(timeh.difference(totaltime,self.totals[len(self.totalDiffs)]))
