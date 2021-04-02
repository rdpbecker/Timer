import timeHelpers as timeh

class SumList:
    total = 0
    bests = []
    totalBests = []

    def __init__(self,bests):
        self.bests = bests
        self.totalBests = [0 for i in range(len(bests))]
        self.setTotals()

    def update(self,time,index):
        self.bests[index] = time
        self.setTotals()

    def setTotals(self):
        total = self.bests[0]
        self.totalBests[0] = total
        for i in range(1,len(self.bests)):
            total = timeh.add(total,self.bests[i])
            self.totalBests[i] = total
        self.total = total
