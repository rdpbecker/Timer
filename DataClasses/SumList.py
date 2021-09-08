from util import timeHelpers as timeh

class SumList:
    total = 0
    bests = []
    totalBests = []

    def __init__(self,bests):
        self.bests = bests
        self.totalBests = [0 for _ in range(len(bests))]
        self.setTotals()

    def update(self,time,index):
        self.bests[index] = time
        self.setTotals()

    def insertNewSegment(self,segment):
        self.bests.insert(segment,timeh.blank())
        if segment < len(self.totalBests):
            self.totalBests.insert(segment,self.totalBests[segment])
        else:
            self.totalBests.insert(segment,timeh.blank())

    def removeSegment(self,segment):
        del self.bests[segment]
        del self.totalBests[segment]
        if segment < len(self.bests):
            self.bests[segment] = timeh.difference(self.totalBests[segment],self.totalBests[segment-1])

    def setTotals(self):
        if not len(self.bests):
            self.total = timeh.blank()
            self.totalBests = []
            return
        total = self.bests[0]
        self.totalBests[0] = total
        for i in range(1,len(self.bests)):
            total = timeh.add(total,self.bests[i])
            self.totalBests[i] = total
        self.total = total
