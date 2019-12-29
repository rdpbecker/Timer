import Time

class Timelist:
    timelist = []
    maxPrecision = 0
    length = 0
    nzeroLength = 0

    def __init__(self):
        self.timelist = []
        self.maxPrecision = 0

    def __str__(self):
        string = ""
        for time in self.timelist:
            string = string + time.__str__() + "\n"
        return string

    def toStringList(self,precision=-1):
        strings = []
        for i in range(self.length):
            strings.append(self.timelist[i].__str__(precision=precision))
        return strings

    def insert(self,time):
        self.timelist.append(time)
        if time.precision > self.maxPrecision:
            self.maxPrecision = time.precision
        self.length = self.length + 1
        if not time.equal(Time.Time(time.precision,timestring='-')):
            self.nzeroLength = self.nzeroLength + 1

    def sum(self):
        total = 0
        precision = 0
        for time in self.timelist:
            total = total + time.toSecs()
        return Time.Time(self.maxPrecision,floattime=total)

    def getSums(self):
        new = Timelist()
        splice = Timelist()
        for i in range(self.length):
            splice.insert(self.timelist[i])
            if self.timelist[i].equal(Time.Time(self.timelist[i].precision,timestring='-')):
                new.insert(Time.Time(self.maxPrecision,timestring='-'))
            else:
                new.insert(splice.sum())
        return new

    def average(self):
        newtime = self.sum()
        return newtime.divide(self.nzeroLength)

    def max(self):
        index = -1
        theMax = 0
        for i in range(self.length):
            if self.timelist[i].toSecs() > theMax:
                index = i
                theMax = self.timelist[i].toSecs()
        return self.timelist[index]

    def replace(self,time,index):
        self.timelist[index] = time
        if time.precision > self.maxPrecision:
            self.maxPrecision = time.precision

    def get(self,index):
        return self.timelist[index]

    def lastNonZero(self):
        for i in range(self.length-1,-1,-1):
            if not self.timelist[i].equal(Time.Time(self.timelist[i].precision,timestring='-')):
                return i+1
        return -1 # Should never get here
