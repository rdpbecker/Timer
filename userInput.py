import sys, select, Time, config
from timeit import default_timer as timer

switch = 0

def guiSplit():
    pass

def waitForInput():
    while 1:
        stdin = sys.stdin.readline()
        if "\n" in stdin:
            break

def waitWithInterrupt(time,starttime,state):
    global switch
    start = timer()
    end = timer()
    splitTimeFloat = timer()
    splitTime = Time.Time(0,floattime=end-start)
    splitFlag = 0
    globalStart = timer()
    globalEnd = timer()
    count = 0
    currentFloat = timer()
    current = Time.Time(2,floattime=(starttime+globalEnd-globalStart))
    currentFlag = 0
    flag = 0
    string1 = "0"
    string2 = str(int(starttime))
    while 1:
        end = timer()
        globalEnd = timer()
        if end - splitTimeFloat < 0.95 and globalEnd - currentFloat < 0.0095:
            continue
        nextSplitTime = Time.Time(0,floattime=end-start)
        if nextSplitTime != splitTime:
            splitTime = nextSplitTime
            string1 = nextSplitTime.__str__(flag2=0)
            if splitFlag:
                splitTimeFloat = end 
                splitFlag = 0
            else:
                splitTimeFloat = timer()
                splitFlag = 1
            flag = 1
        nexttime = Time.Time(2,floattime=(starttime+globalEnd-globalStart))
        if nexttime != current:
            current = nexttime
            string2 = nexttime.__str__()
            if currentFlag:
                currentFloat = globalEnd 
                currentFlag = 0
            else:
                currentFloat = timer()
                currentFlag = 1
            flag = 1
        if flag:
            flag = 0
            CURSOR_UP_ONE = '\x1b[1A'
            ERASE_LINE = '\x1b[2K'
            state.app.labels[state.app.timer][0].configure(text=string1)
            state.app.labels[state.app.timer+1][0].configure(text=string2) 
        if sys.stdin in select.select([sys.stdin],[],[],0)[0]:
            if sys.stdin.readline() == "\n":
                switch = 1
        if switch == 1:
            switch = 0
            return
        if config.choiceChanged:
            config.choiceChanged=0
            state.updateCompare()
