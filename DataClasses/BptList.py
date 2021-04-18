from util import timeHelpers as timeh

class BptList:
    total = 0
    bests = []
    currentTime = 0

    def __init__(self,bests):
        self.bests = bests
        self.setTotal()

    def update(self,currentTime):
        self.currentTime = currentTime
        self.bests.pop(0)
        self.setTotal()

    def setTotal(self):
        total = self.currentTime
        for i in range(len(self.bests)):
            total = timeh.add(total,self.bests[i])
        self.total = total
