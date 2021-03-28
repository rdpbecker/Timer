class CurrentRun:
    segments = []
    totals = []

    def __init__(self):
        pass

    def addSegment(self,segment,total):
        if (not segment == "BLANK"):
            self.segments.append(segment)
        self.totals.append(total)
