class BptList:
    total = 0
    bests = []

    def __init__(self,bests):
        self.bests = bests
        self.total = sum(bests)

    def update(self,time,index):
        self.bests[index] = time
        self.total = sum(self.bests)
