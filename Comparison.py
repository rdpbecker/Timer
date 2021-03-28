class Comparison:
    segmentHeader = ""
    totalHeader = ""
    segments = []
    totals = []

    def __init__(self,shead,thead,segments,totals):
        self.segmentHeader = shead
        self.totalHeader = thead
        self.segments = segments
        self.totals = totals

    def getSegmentHeader(self):
        return self.segmentHeader

    def getTotalHeader(self):
        return self.totalHeader

    def getSegments(self):
        return self.segments

    def getTotals(self):
        return self.totals

    def getSegment(self,index):
        return self.segments[index]

    def getTotal(self,index):
        return self.totals[index]
