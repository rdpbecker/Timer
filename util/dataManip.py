from util import timeHelpers as timeh
import copy

##########################################################
## Reads a column of times in from a specified data table
##
## Parameters: col - the column to read
##             data_ref - the array to read from
##########################################################
def getTimesByCol(col,data_ref):
    times = []
    for i in range(1,len(data_ref)):
        times.append(timeh.stringToTime(data_ref[i][col]))
    return times

##########################################################
## Replaces the elements of a data table, starting with a 
## specified column.
## 
## Parameters: lines - the new data to put in
##             startIndex - the column to start replacing at
##             data_ref - the CSV to replace data in
##########################################################
def replaceCols(lines,startIndex,data_ref):
    for i in range(1,len(data_ref)):
        for j in range(len(lines)):
            data_ref[i][startIndex+j]=lines[j][i-1]

##########################################################
## Inserts new lines into a data table, starting with a
## specified column.
##
## Parameters: lines - the new data to put in
##             startIndex - the column to start inserting at
##########################################################
def insertCols(lines,startIndex,data_ref):
    for i in range(1,len(data_ref)):
        for j in range(len(lines)):
            data_ref[i].insert(startIndex+j,lines[j][i-1])

##############################################################
## Inserts a SumList object into the data_ref table as two 
## columns, starting with startIndex.
##
## Parameters: sumList: the SumList object to insert into the 
##                      table
##             startIndex - the column to start inserting at
##             data_ref - the table to insert the SumList into
##             options - the options for converting the times
##                       into strings
##
## Returns: None
##############################################################
def insertSumList(sumList,startRow,startCol,data_ref,options={}):
    for i in range(len(sumList.bests)):
        data_ref[startRow+i].insert(startCol,timeh.timeToString(sumList.totalBests[i],options))
        data_ref[startRow+i].insert(startCol,timeh.timeToString(sumList.bests[i],options))

##############################################################
## Inserts a SumList object into the data_ref table as two
## columns, starting with startIndex.
##
## Parameters: sumList: the SumList object to insert into the
##                      table
##             startIndex - the column to start inserting at
##             data_ref - the table to insert the SumList into
##             options - the options for converting the times
##                       into strings
##
## Returns: None
##############################################################
def replaceSumList(sumList,startRow,startCol,data_ref,options={}):
    for i in range(len(sumList.bests)):
        data_ref[i+startRow][startCol] = timeh.timeToString(sumList.bests[i],options)
        data_ref[i+startRow][startCol+1] = timeh.timeToString(sumList.totalBests[i],options)

##############################################################
## Inserts a SumList object into the data_ref table as two
## columns, starting with startIndex.
##
## Parameters: sumList: the SumList object to insert into the
##                      table
##             startIndex - the column to start inserting at
##             data_ref - the table to insert the SumList into
##             options - the options for converting the times
##                       into strings
##
## Returns: None
##############################################################
def replaceComparison(comparison,startRow,startCol,data_ref,options={}):
    for i in range(len(comparison.segments)):
        data_ref[i+startRow][startCol] = timeh.timeToString(comparison.segments[i],options)
        data_ref[i+startRow][startCol+1] = timeh.timeToString(comparison.totals[i],options)

##############################################################
## Changes the names in the first column of the table in
## data_ref, adding and removing rows from the table if the
## lists of names do not have the same length.
##
## Parameters: names - a list of the new names
##             data_ref - the data table to update
##
## Returns: A deep copy of the original data, with the names
##          updated.
##############################################################
def adjustNames(names,data_ref):
    new_data = copy.deepcopy(data_ref)
    for i in range(1,len(names)+1):
        if i >= len(new_data):
            row = [names[i-1]]
            row.extend(['-' for j in range(len(new_data[0])-1)])
            new_data.append(row)
        else:
            new_data[i][0] = names[i-1]
    return new_data[:len(names)+1]

##############################################################
## Changes the names in the first column of the table in
## data_ref, adding and removing rows from the table if the
## lists of names do not have the same length.
##
## Parameters: names - a list of the new names
##             data_ref - the data table to update
##
## Returns: A deep copy of the original data, with the names
##          updated.
##############################################################
def adjustNamesMismatch(names,data_ref,originals):
    new_data = [copy.deepcopy(data_ref[0])]
    for i in range(len(names)):
        if i in originals:
            new_data.append(copy.deepcopy(data_ref[originals.index(i)+1]))
        else:
            new_data.append([names[i]]+['-' for j in range(len(new_data[0])-1)])
    return new_data
