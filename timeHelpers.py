import re

def zeroPad(finalLength,string):
    while len(string) < finalLength:
        string = "0" + string
    return string

def timeToString(totalSecs,showSign=False,blankToDash=True,precision=0):
    if isBlank(totalSecs):
        if blankToDash:
            return '-'
        else:
            if not precision:
                return "0"
            else:
                return "0.0000000"[:precision+2]
    string = ""
    if showSign:
        if totalSecs > 0:
            string = "+"
        else: 
            string = '-'
    totalSecs = abs(totalSecs)
    fracsecs = totalSecs - int(totalSecs)
    totalSecs = int(totalSecs)
    secs = totalSecs % 60
    totalSecs = (totalSecs - secs)/60
    mins = int(totalSecs % 60)
    hours = int((totalSecs - mins)/60)
    if hours:
        string = string + str(hours) + ":"
        string = string + zeroPad(2,str(mins)) + ":"
        string = string + zeroPad(2,str(secs))
    elif mins:
        string = string + str(mins) + ":"
        string = string + zeroPad(2,str(secs))
    elif secs:
        string = string + str(secs)
    else:
        string = string + "0" 
    if precision:
        string = string + str(fracsecs)[1:precision+2]
    return string

def timesToStringList(arr,showSign=False,blankToDash=True,precision=0):
    newarr = []
    for thing in arr:
        newarr.append(timeToString(thing,showSign,blankToDash,precision))
    return newarr

def stringToTime(timestring):
    if timestring == "-":
        return "BLANK"
    parts1 = re.split("\.",timestring)
    parts2 = re.split(":",parts1[0])
    hours = 0
    mins = 0
    secs = 0
    fracsecs = 0
    if len(parts1) > 1:
        fracsecs = float("0."+parts1[1])
    if len(parts2) == 3:
        hours = int(parts2[0])
        mins = int(parts2[1])
        secs = int(parts2[2])
    elif len(parts2) == 2:
        mins = int(parts2[0])
        secs = int(parts2[1])
    else:
        secs = int(parts2[0])
    return 3600*hours + 60*mins + secs + fracsecs

def isBlank(time):
    return time == "BLANK"

def difference(time1,time2):
    if isBlank(time1) or isBlank(time2):
        return "BLANK"
    return time1 - time2

def add(time1,time2):
    if isBlank(time1) or isBlank(time2):
        return "BLANK"
    return time1 + time2

def greater(time1,time2):
    if isBlank(time1) or isBlank(time2):
        return "BLANK"
    return time1 > time2

def equal(time1,time2):
    if isBlank(time1) or isBlank(time2):
        return "BLANK"
    return time1 == time2
