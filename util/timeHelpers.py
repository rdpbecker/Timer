import re

def zeroPad(finalLength,string):
    while len(string) < finalLength:
        string = "0" + string
    return string

def adjustEnd(fracsecs):
    if fracsecs:
        string = str(fracsecs)
    else:
        string = "0.0"
    while (len(string) < 11):
        string = string + "0"
    return string

def trimTime(time):
    index = time.find(".")
    if index < 0:
        return time
    return time[:min([index+3,len(time)])]

def validTime(time):
    if not type(time) in [float,str]:
        return False
    if type(time) == float:
        return True
    if time == "-":
        return True
    secs = re.compile(r'^[1-5]?\d{1}\.\d{1,5}$')
    mins = re.compile(r'^[1-5]?\d{1}:[0-5]\d{1}\.\d{1,5}$')
    hours = re.compile(r'^\d{1,10}:[0-5]\d{1}:[0-5]\d{1}\.\d{1,5}$')
    return secs.match(time) or mins.match(time) or hours.match(time)

def parseOptions(options):
    newOptions = {\
        "showSign": False, \
        "blankToDash": True, \
        "precision": 0,\
        "noPrecisionOnMinute": False\
    }

    newOptions.update(options)
    return newOptions

def timeToString(totalSecs,options={}):
    options = parseOptions(options)
    if isBlank(totalSecs):
        if options["blankToDash"]:
            return '-'
        else:
            if not options["precision"]:
                return "0"
            else:
                return "0.0000000"[:options["precision"]+2]
    string = ""
    if options["showSign"]:
        if totalSecs > 0:
            string = "+"
        else: 
            string = '-'
    totalSecs = abs(totalSecs)
    if totalSecs > 60 and options["noPrecisionOnMinute"]:
        options["precision"] = 0
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
    if options["precision"]:
        string = string + adjustEnd(fracsecs)[1:options["precision"]+2]
    return string

def timesToStringList(arr,options={}):
    newarr = []
    for thing in arr:
        newarr.append(timeToString(thing,options))
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

def sumTimeList(arr):
    if not len(arr):
        return "BLANK"
    total = arr[0]
    for i in range(1,len(arr)):
        total = add(total,arr[i])
    return total

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
