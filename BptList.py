class BptList:
    totalSecs = 0
    bests = []

    def __init__(self,bests):
        self.bests = bests
        self.totalSecs = sum(bests)

    def update(self,index,time):
        if time > self.bests[index]
            return
        self.bests[index] = time
        self.totalSecs = sum(bests)
