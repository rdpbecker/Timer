def zeroPad(finalLength,string):
    while len(string) < finalLength:
        string = "0" + string
    return string

def toString(totalSecs,flag=0,flag2=1,precision=0):
    if not totalSecs:
        if flag2:
            return '-'
    string = ""
    if flag:
        if string > 0:
            string = "+"
        else: 
            string = '-'
    fracsecs = totalSecs - int(totalSecs)
    totalSecs = int(totalSecs)
    secs = totalSecs % 60
    totalSecs = (totalSecs - secs)/60
    mins = totalSecs % 60
    hours = (totalSecs - mins)/60
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
