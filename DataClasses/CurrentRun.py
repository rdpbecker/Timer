from util import timeHelpers as timeh

class CurrentRun:
    segments = []
    totals = []
    empty = False

    def __init__(self):
        self.segments = []
        self.totals = []

    def addSegment(self,segment,total):
        if (not(len(self.segments)) or not timeh.isBlank(self.totals[-1])):
            self.segments.append(segment)
        else:
            self.segments.append(timeh.blank())
        self.totals.append(total)

    def fillTimes(self,requiredLength):
        n = len(self.segments)
        if not n:
            self.empty = True
        for _ in range(requiredLength-n):
            self.segments.append(timeh.blank())
            self.totals.append(timeh.blank())

    def lastNonBlank(self):
        for i in range(len(self.totals)-1,-1,-1):
            if not timeh.isBlank(self.totals[i]):
                return i
        return -1
