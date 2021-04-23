from util import timeHelpers as timeh

class DifferenceList:
    total = 0
    segments = []
    totals = []

    def __init__(self,totals):
        self.totals = totals
        self.segments = [0 for i in range(len(totals))]
        self.setSegments()

    def update(self,time,index):
        self.totals[index] = time
        self.setSegments()

    def setSegments(self):
        self.segments[0] = self.totals[0]
        for i in range(1,len(self.totals)):
            self.segments[i] = timeh.difference(self.totals[i],self.totals[i-1])
