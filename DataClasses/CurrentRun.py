from util import timeHelpers as timeh

class CurrentRun:
    segments = []
    totals = []

    def __init__(self):
        self.segments = []
        self.totals = []

    def addSegment(self,segment,total):
        if (not(len(self.segments)) or not timeh.isBlank(self.totals[-1])):
            self.segments.append(segment)
        else:
            self.segments.append("BLANK")
        self.totals.append(total)

    def fillTimes(self,requiredLength):
        n = len(self.segments)
        for i in range(requiredLength-n):
            self.segments.append("BLANK")
            self.totals.append("BLANK")

    def lastNonBlank(self):
        for i in range(len(self.totals)-1,-1,-1):
            if not timeh.isBlank(self.totals[i]):
                return i
        return -1
