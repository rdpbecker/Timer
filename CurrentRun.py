class CurrentRun:
    segments = []
    totals = []

    def __init__(self):
        pass

    def addSegment(self,segment,total):
        if (not self.totals[-1] == "BLANK"):
            self.segments.append(segment)
        else:
            self.segments.append("BLANK")
        self.totals.append(total)
