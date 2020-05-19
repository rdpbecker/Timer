import re

def zeroPad(finalLength,string):
    while len(string) < finalLength:
        string = "0" + string
    return string

def setPrecision(finalLength,string):
    if len(string) >= finalLength:
        return string[:finalLength]
    while len(string) < finalLength:
        string = string + "0"
    return string

class Time:
    hours = 0
    mins = 0
    secs = 0
    fracsecs = 0
    precision = 0
    sign = ""

    def __init__(self,precision,fracsecs=0,secs=0,mins=0,hours=0,floattime=0,timestring=""):
        self.precision = precision
        if not floattime and not timestring:
            self.fracsecs = fracsecs
            self.secs = secs
            self.mins = mins
            self.hours = hours
        elif floattime:
            if floattime < 0:
                self.sign = "-"
                floattime = -1*floattime
            fracs = floattime - int(floattime)
            self.fracsecs = int(fracs*(10**precision))
            real = int(floattime)
            self.secs = real%60
            real = int((real-self.secs)/60)
            self.mins = real%60
            real = int((real-self.mins)/60)
            self.hours = real
        else:
            if timestring == "-":
                return
            parts1 = re.split("\.",timestring)
            parts2 = re.split(":",parts1[0])
            if precision and len(parts1) > 1:
                stringPrecision = len(parts1[1])
                self.fracsecs = int(parts1[1])*(10**(precision-stringPrecision))
            if len(parts2) == 3:
                self.hours = int(parts2[0])
                self.mins = int(parts2[1])
                self.secs = int(parts2[2])
            elif len(parts2) == 2:
                self.mins = int(parts2[0])
                self.secs = int(parts2[1])
            else:
                self.secs = int(parts2[0])

    def __str__(self,flag=0,flag2=1,precision=-1):
        if precision == -1:
            if self.precision:
                precision = self.precision
            else:
                precision = 0
        if self.equal(Time(self.precision,timestring='-')):
            if flag2:
                return '-'
        string = self.sign
        if flag and not self.sign:
            string = "+"
        if self.hours:
            string = string + str(self.hours) + ":"
            string = string + zeroPad(2,str(self.mins)) + ":"
            string = string + zeroPad(2,str(self.secs))
        elif self.mins:
            string = string + str(self.mins) + ":"
            string = string + zeroPad(2,str(self.secs))
        elif self.secs:
            string = string + str(self.secs)
        else:
            string = string + "0" 
        if self.precision:
            string = string + "." + setPrecision(precision,zeroPad(self.precision,str(self.fracsecs)))
        return string

    def toSecs(self):
        num = 3600*self.hours + 60*self.mins + self.secs + self.fracsecs*float(10)**(-1*self.precision) 
        if self.sign:
            return -1*num
        else:
            return num

    def add(self,time):
        if self.precision != time.precision:
            return -1
        newtime = Time(self.precision,floattime=self.toSecs()+time.toSecs())
        return newtime

    def subtract(self,time):
        if self.precision != time.precision:
            return -1
        newtime = Time(self.precision,floattime=(self.toSecs()-time.toSecs()))
        return newtime

    def greater(self,time):
        if self.precision != time.precision:
            return -1
        if self.subtract(time).toSecs() > 0:
            return 1
        elif self.subtract(time).toSecs():
            return -1
        return 0

    def divide(self,num):
        if not num:
            return Time(self.precision,timestring='-')
        return Time(self.precision,floattime=self.toSecs()/num)

    def equal(self,time):
        if self.precision != time.precision:
            return 0
        if self.fracsecs != time.fracsecs:
            return 0
        if self.secs != time.secs:
            return 0
        if self.mins != time.mins:
            return 0
        if self.hours != time.hours:
            return 0
        if self.sign != time.sign:
            return 0
        return 1

    def isNeg(self):
        if self.sign:
            return 1
        return 0
