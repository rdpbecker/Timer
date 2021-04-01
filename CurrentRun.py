class CurrentRun:
    segments = []
    totals = []

    def __init__(self):
        self.segments = []
        self.totals = []

    def addSegment(self,segment,total):
        if (not(len(self.segments)) or not self.totals[-1] == "BLANK"):
            self.segments.append(segment)
        else:
            self.segments.append("BLANK")
        self.totals.append(total)

    def fillTimes(self,requiredLength):
        n = len(self.segments)
        for i in range(n+1,requiredLength):
            self.segments.append("BLANK")
            self.totals.append("BLANK")
