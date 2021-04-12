# Run tkinter code in another thread

import timeHelpers as timeh
import tkinter as tk
import threading
from timeit import default_timer as timer
import State, GeneralInfo, fileio 

class Gui(threading.Thread):
    labels = []
    buttons = []
    backgrounds = []
    splitstart = 2
    pbstart = 10
    timer = 12
    bptstart = 14
    buttonstart = 18
    state = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.run()

    def callback(self):
        self.root.quit()

    def run(self):
        ## Initialize the state. This picks the game and category
        self.state = State.State()
        config = self.state.config
        generalInfo = {\
            "timeSave": GeneralInfo.GeneralInfo(config["timeSaveShow"],self.timeSaveSet,self.timeSaveInfo),\
            "diff": GeneralInfo.GeneralInfo(config["diffShow"],self.diffSet,self.diffInfo),\
            "bpt": GeneralInfo.GeneralInfo(config["bptShow"],self.bptSet,self.bptInfo),\
            "sob": GeneralInfo.GeneralInfo(config["sobShow"],self.sobSet,self.sobInfo),\
            "pb": GeneralInfo.GeneralInfo(config["pbShow"],self.pbSet,self.pbInfo)\
        }
        generalInfoKeys = ["timeSave","diff","bpt","sob","pb"]
        self.setSectionStarts(config,generalInfo,generalInfoKeys)
        self.state.generalInfo = generalInfo
        self.state.generalInfoKeys = generalInfoKeys

        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.configure(background='black')

        for i in range(12):
            self.root.columnconfigure(i,minsize=40,weight=1)

        ## Initialize the format of the gui and store references to all
        ## the labels so we can change them. References are stored in
        ## a grid

        ## The Title rows
        for i in range(self.splitstart):
            label = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"])
            label.grid(row=i,column=0,columnspan=2,sticky='W',ipadx=10)
            label2 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"])
            label2.grid(row=i,column=2,columnspan=3,sticky='W')
            label3 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"])
            label3.grid(row=i,column=5,columnspan=4,sticky='E')
            label4 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"])
            label4.grid(row=i,column=9,columnspan=3,sticky='E',ipadx=10)
            self.labels.append([label,label2,label3,label4])

        ## Splits and comparisons
        for i in range(self.splitstart,self.pbstart):
            background = tk.Frame(self.root, bg='black')
            background.grid(row=i,column=0,columnspan=12,sticky='NSWE')
            self.backgrounds.append(background)
            label = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"])
            label.grid(row=i,column=0,columnspan=8,sticky='W',padx=10)
            label2 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"])
            label2.grid(row=i,column=8,columnspan=2,sticky='E')
            label3 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"])
            label3.grid(row=i,column=10,columnspan=2,sticky='E',padx=10)
            self.labels.append([label,label2,label3])

        ## Current segment comparisons
        for i in range(self.pbstart,self.timer):
            label = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"])
            label.grid(row=i,column=0,columnspan=3,sticky='W',padx=10)
            label2 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"])
            label2.grid(row=i,column=3,columnspan=3,sticky='W')
            label3 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"])
            label3.grid(row=i,column=6,columnspan=3,sticky='W')
            label4 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"])
            label4.grid(row=i,column=9,columnspan=3,sticky='E',padx=10)
            self.labels.append([label,label2,label3,label4])

        ## Timers (segment and overall)
        anchorlist = ['E','']
        span = [10,12]
        fontlist = [config['segmentFont'],config['timerFont']]
        colourlist = [config["segmentColour"],config["timerMainColour"]]
        for i in range(self.timer,self.bptstart):
            label = tk.Label(self.root, bg='black', text="", fg=colourlist[i-self.timer], font=fontlist[i-self.timer])
            label.grid(row=i,column=0,columnspan=12,sticky=anchorlist[i-self.timer],padx=100)
            self.labels.append([label])

        ## Information
        for i in range(self.bptstart,self.buttonstart):
            label = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"])
            label.grid(row=i,column=0,columnspan=6,sticky='W',padx=10)
            label4 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"])
            label4.grid(row=i,column=9,columnspan=3,sticky='E',padx=10)
            self.labels.append([label,label4])

        button1 = tk.Button(self.root, bg=config["buttonBgColour"], font=config["buttonFont"], text="Change Compare", fg=config["buttonTextColour"],command=self.guiSwitchCompare)
        button2 = tk.Button(self.root, bg=config["buttonBgColour"], font=config["buttonFont"], text="Split", fg=config["buttonTextColour"],  command=self.onSplitEnd)
        self.root.bind('<Return>', self.onSplitEnd)
        button3 = tk.Button(self.root, bg=config["buttonBgColour"], font=config["buttonFont"], text="Reset", fg=config["buttonTextColour"],  command=self.reset)
        self.root.bind('r', self.reset)
        button4 = tk.Button(self.root, bg=config["buttonBgColour"], font=config["buttonFont"], text="Skip Split", fg=config["buttonTextColour"], command=self.skip)
        self.root.bind('s', self.skip)
        button5 = tk.Button(self.root, bg=config["buttonBgColour"], font=config["buttonFont"], text="Start Run", fg=config["buttonTextColour"], command=self.start)
        self.root.bind('<space>', self.start)
        button6 = tk.Button(self.root, bg=config["buttonBgColour"], font=config["buttonFont"], text="Pause", fg=config["buttonTextColour"], command=self.togglePause)
        self.root.bind('p', self.togglePause)
        button3.grid(row=self.buttonstart,column=0,columnspan=6,sticky='WE')
        button4.grid(row=self.buttonstart,column=6,columnspan=6,sticky='WE')
        button1.grid(row=self.buttonstart+1,column=0,columnspan=6,sticky='WE')
        button6.grid(row=self.buttonstart+1,column=6,columnspan=6,sticky='WE')
        button2.grid(row=self.buttonstart+2,column=0,columnspan=6,sticky='WE')
        button5.grid(row=self.buttonstart+2,column=6,columnspan=6,sticky='WE')
        self.buttons.append([button1,button2,button3,button4,button5,button6])

        ## Initialize the text in the gui and set the timer to update 
        ## at 125ish FPS
        self.initialize()
        self.root.after(8,self.update)

        self.root.mainloop()

    def setSectionStarts(self,config,generalInfo,generalInfoKeys):
        self.pbstart = self.splitstart + config["numSplits"] + 1
        self.timer = self.pbstart + 2
        self.bptstart = self.timer + 2
        count = 0
        for key in generalInfoKeys:
            if generalInfo[key].show:
                count = count + 1
        self.buttonstart = self.bptstart + count

    ##########################################################
    ## Set the timer to update every time this is called
    ##########################################################
    def update(self):
        if self.state.started:
            currentTime = timer()
            if self.state.paused:
                currentTime = self.state.pauseTime
            self.state.setTimes(currentTime)
            self.labels[self.timer+1][0].configure(text=timeh.timeToString(self.state.totalTime,{"blankToDash":False,"precision":2}))
            self.labels[self.timer+1][0].configure(fg=self.setTimerColour())
            self.labels[self.timer][0].configure(text=timeh.timeToString(self.state.segmentTime,{"blankToDash":False}))
            # if behind gold or behind current comparison total,
            # show the diff column for the current split in the
            # split area. If either is blank, ignore the comparison
            if self.state.splitnum < len(self.state.splitnames) \
                and (not timeh.greater(self.state.currentComparison.totals[self.state.splitnum],self.state.totalTime)\
                or not timeh.greater(self.state.comparisons[0].segments[self.state.splitnum],self.state.segmentTime)):
                self.showCurrentSplitDiff()
        if self.state.splitnum < len(self.state.splitnames) and not self.state.reset:
            self.root.after(17,self.update)
        else:
            self.root.after(1,self.state.doEnd)

    def setTimerColour(self):
        splitnum = self.state.splitnum
        if self.state.splitnum >= len(self.state.splitnames):
            splitnum = len(self.state.splitnames) - 1
        comparisonTime = self.state.currentComparison.totals[splitnum]
        comparisonSegment = self.state.currentComparison.segments[splitnum]
        goldSegment = self.state.comparisons[0].segments[splitnum]

        # last split skipped
        if self.state.splitnum \
            and timeh.isBlank(self.state.currentRun.totals[-1]):
            # total blank or ahead of total
            if timeh.greater(comparisonTime,self.state.totalTime):
                return self.state.config["timerMainColour"]
            # behind total
            else:
                return self.state.config["timerBehindLosingColour"]
        # total blank
        if timeh.isBlank(comparisonTime):
            # gold blank or ahead of gold
            if timeh.greater(goldSegment,self.state.segmentTime):
                return self.state.config["timerMainColour"]
            # behind gold
            else:
                return self.state.config["timerBehindLosingColour"]
        # ahead of total
        elif timeh.greater(comparisonTime,self.state.totalTime):
            # segment blank
            if timeh.isBlank(comparisonSegment):
                # gold blank or ahead of gold
                if timeh.greater(goldSegment,self.state.segmentTime):
                    return self.state.config["timerMainColour"]
                # behind gold
                else:
                    return self.state.config["timerAheadLosingColour"]
            # ahead of segment
            elif timeh.greater(comparisonSegment,self.state.segmentTime):
                # gold blank or ahead of gold
                if timeh.greater(goldSegment,self.state.segmentTime):
                    return self.state.config["timerMainColour"]
                # behind gold
                else:
                    return self.state.config["timerNotGoldAheadGainingColour"]
            # behind segment
            else:
                return self.state.config["timerAheadLosingColour"]
        # behind total
        else:
            # segment blank
            if timeh.isBlank(comparisonSegment):
                # gold blank or behind gold
                if timeh.greater(self.state.segmentTime,goldSegment):
                    return self.state.config["timerBehindLosingColour"]
                # ahead of gold
                else:
                    return self.state.config["timerBehindGainingColour"]
            # ahead of segment
            elif timeh.greater(comparisonSegment,self.state.segmentTime):
                # gold blank or ahead of gold
                if timeh.greater(goldSegment,self.state.segmentTime):
                    return self.state.config["timerBehindGainingColour"]
                # behind gold
                else:
                    return self.state.config["timerNotGoldBehindGainingColour"]
            # behind segment
            else:
                return self.state.config["timerBehindLosingColour"]

    def showCurrentSplitDiff(self):
        activeSplit = self.state.splitnum - self.state.getTopSplitIndex()
        self.labels[self.splitstart+activeSplit][1].configure(\
            text=timeh.timeToString(\
                timeh.difference(self.state.totalTime,self.state.currentComparison.totals[self.state.splitnum]),\
                {"showSign":True,"precision": 2}\
            ),\
            fg=self.getCurrentDiffColour(\
                timeh.difference(self.state.segmentTime,self.state.currentComparison.segments[self.state.splitnum]), \
                timeh.difference(self.state.totalTime,self.state.currentComparison.totals[self.state.splitnum])\
            )\
        )

    ##########################################################
    ## Caller to all the functions that initialize text before
    ## the run is started
    ##########################################################
    def initialize(self):
        self.initHeader()
        self.initTimes()
        self.initInfo()
        self.updateCurrentColour()

    ##########################################################
    ## Initialize the header with game, category, and
    ## comparison name
    ##########################################################
    def initHeader(self):
        self.labels[0][0].configure(text=self.state.game)
        self.labels[0][1].configure(text=self.state.category)
        self.labels[0][2].configure(text="Comparing Against")
        self.labels[0][3].configure(text=self.state.currentComparison.totalHeader)

    ##########################################################
    ## Initialize the split names and times for the first few
    ## splits and the last one. This is based on the PB time
    ##########################################################
    def initTimes(self):
        for i in range(0,self.pbstart-self.splitstart-2):
            self.labels[self.splitstart+i][0].configure(text=self.state.splitnames[i])
            self.labels[self.splitstart+i][2].configure(text=self.state.currentComparison.getString("totals",i,{"precision":2}))
        self.labels[self.pbstart-2][0].configure(text=self.state.splitnames[-1])
        self.labels[self.pbstart-2][2].configure(text=self.state.currentComparison.getString("totals",-1,{"precision":2}))

    ##########################################################
    ## Initialize all the info on the bottom, including split
    ## comparisons, time save, BPT, and PB
    ##########################################################
    def initInfo(self):
        self.labels[self.pbstart][0].configure(text=self.state.currentComparison.segmentHeader)
        self.labels[self.pbstart+1][0].configure(text="Best Split:")

        count = 0
        for key in self.state.generalInfoKeys:
            if self.state.generalInfo[key].show:
                self.state.generalInfo[key].startCallback(count)
                count = count + 1

        self.updateInfo()

    ##########################################################
    ## Set the colours for the current and last splits based
    ## on the current split number
    ##########################################################
    def updateCurrentColour(self):
        lowIndex = self.state.getTopSplitIndex()
        for i in range(0,self.pbstart-self.splitstart-1):
            if i == self.state.splitnum-lowIndex:
                self.labels[self.splitstart+i][0].configure(fg=self.state.config["activeColour"],bg=self.state.config["activeBgColour"])
                self.labels[self.splitstart+i][1].configure(bg=self.state.config["activeBgColour"])
                self.labels[self.splitstart+i][2].configure(fg=self.state.config["activeColour"],bg=self.state.config["activeBgColour"])
                self.backgrounds[i].configure(bg=self.state.config["activeBgColour"])
            else:
                self.labels[self.splitstart+i][0].configure(fg=self.state.config["mainColour"],bg='black')
                self.labels[self.splitstart+i][1].configure(bg='black')
                self.labels[self.splitstart+i][2].configure(fg=self.state.config["mainColour"],bg='black')
                self.backgrounds[i].configure(bg='black')
        self.labels[self.pbstart-2][0].configure(fg=self.state.config["endColour"])
        self.labels[self.pbstart-2][2].configure(fg=self.state.config["endColour"])

    ##########################################################
    ## Update current split and BPT information based on the
    ## current split
    ##########################################################
    def updateInfo(self):
        self.labels[self.pbstart][1].configure(text=self.state.currentComparison.getString("segments",self.state.splitnum,{"precision":2}))
        self.labels[self.pbstart+1][1].configure(text=self.state.comparisons[0].getString("segments",self.state.splitnum,{"precision":2}))
        count = 0
        for key in self.state.generalInfoKeys:
            if self.state.generalInfo[key].show:
                self.state.generalInfo[key].generalCallback(count)
                count = count + 1

    ##########################################################
    ## Initialize the start and first split times when the run
    ## starts
    ##########################################################
    def start(self, event=None):
        currentTime = timer()
        if self.state.started:
            self.onSplitEnd()
            return
        self.state.starttime = currentTime
        self.state.splitstarttime = currentTime
        self.state.started = True

    ##########################################################
    ## At the end of each split, record and store the times, 
    ## calculate all the diffs, and call the helper functions 
    ## to update the GUI
    ##########################################################
    def onSplitEnd(self,event=None):
        splitEnd = timer()
        if not self.state.started:
            self.start()
            return

        if self.state.paused:
            self.togglePause()
            return
        
        if self.state.splitnames[self.state.splitnum][-3:] == "[P]" and not self.state.splitnum == len(self.state.splitnames) and not self.state.paused:
            self.togglePause()

        self.state.completeSegment(splitEnd)
        self.updateTimes()
        self.updateCurrentColour()
        if self.state.splitnum < len(self.state.splitnames):
            self.updateInfo()
        self.state.splitstarttime = splitEnd

    def getCurrentDiffColour(self,segmentDiff,totalDiff):
        if timeh.greater(0,totalDiff):
            # if comparison segment is blank or current segment is
            # ahead
            if timeh.greater(0,segmentDiff):
                return self.state.config["aheadGainingColour"]
            else:
                return self.state.config["aheadLosingColour"]
        else:
            # if comparison segment is blank or current segment is
            # behind
            if timeh.greater(segmentDiff,0):
                return self.state.config["behindLosingColour"]
            else:
                return self.state.config["behindGainingColour"]

    def findDiffColour(self,splitIndex):
        # Either the split in this run is blank, or we're comparing
        # to something that's blank
        if \
            timeh.isBlank(self.state.currentRun.totals[splitIndex]) \
            or timeh.isBlank(self.state.currentComparison.totals[splitIndex]):
            return self.state.config["skippedColour"]
        # This split is the best ever. Mark it with the gold colour
        elif not timeh.isBlank(self.state.comparisons[0].segmentDiffs[splitIndex]) \
            and timeh.greater(0,self.state.comparisons[0].segmentDiffs[splitIndex]):
            return self.state.config["goldColour"]
        else:
            return self.getCurrentDiffColour(\
                self.state.currentComparison.segmentDiffs[splitIndex],\
                self.state.currentComparison.totalDiffs[splitIndex]\
            )

    ##########################################################
    ## Update the times and split names in the split portion 
    ## of the GUI. This includes shifting entries as needed so
    ## the current split is the third entry in the list, and 
    ## colouring the diff numbers properly
    ##########################################################
    def updateTimes(self):
        ## i is the number from the top of the list of splits. For the 
        ## top entry i=0, the next one down has i=1, and so on
        ##
        ## lowIndex is the index in the list of splits of the top split
        ## in the gui - if split #5 is at the top of the view area in
        ## the gui, then lowIndex=5
        lowIndex = self.state.getTopSplitIndex()
        for i in range(0,self.pbstart-self.splitstart-2):
            ## The index of the split we're looking at currently
            subjectSplitIndex = i+lowIndex
            self.labels[self.splitstart+i][0].configure(text=self.state.splitnames[subjectSplitIndex])
            if self.state.splitnum > subjectSplitIndex:
                self.labels[self.splitstart+i][1].configure(text=self.state.currentComparison.getString("totalDiffs",subjectSplitIndex,{"showSign":True,"precision":2}))
                self.labels[self.splitstart+i][2].configure(text=timeh.timeToString(self.state.currentRun.totals[subjectSplitIndex],{"precision":2}))
                self.labels[self.splitstart+i][1].configure(fg=self.findDiffColour(subjectSplitIndex))
            else:
                self.labels[self.splitstart+i][1].configure(text="")
                self.labels[self.splitstart+i][2].configure(text=self.state.currentComparison.getString("totals",subjectSplitIndex,{"precision":2}))

        if self.state.splitnum >= len(self.state.splitnames):
            self.labels[self.pbstart-2][1].configure(text=self.state.currentComparison.getString("totalDiffs",-1,{"showSign":True,"precision":2}))
            self.labels[self.pbstart-2][2].configure(text=timeh.timeToString(self.state.currentRun.totals[-1],{"precision":2}))
            self.labels[self.pbstart-2][1].configure(fg=self.findDiffColour(len(self.state.splitnames)-1))

    ##########################################################
    ## Update information about the comparison splits when the 
    ## comparison is changed
    ##########################################################
    def updateCompare(self):
        self.labels[0][3].configure(text=self.state.currentComparison.totalHeader)
        self.labels[self.pbstart][0].configure(text=self.state.currentComparison.segmentHeader+":")
        self.labels[self.pbstart-2][2].configure(text=self.state.currentComparison.getString("totals",-1,{"precision":2}))

    ##########################################################
    ## The function called when the 'Switch Compare' button is
    ## clicked
    ##########################################################
    def guiSwitchCompare(self,event=None):
        self.state.compareNum = (self.state.compareNum+1)%self.state.numComparisons
        self.state.currentComparison = self.state.comparisons[self.state.compareNum]
        self.updateTimes()
        self.updateInfo()
        self.updateCompare()

    ##########################################################
    ## Stop the run here
    ##########################################################
    def reset(self, event=None):
        self.state.reset = True

    ##########################################################
    ## Skip a split
    ##########################################################
    def skip(self,event=None):
        splitEnd = timer()
        self.state.skipSegment(splitEnd)
        self.updateTimes()
        self.updateCurrentColour()
        if self.state.splitnum < len(self.state.splitnames):
            self.updateInfo()
        self.state.splitstarttime = splitEnd

    def togglePause(self,event=None):
        currentTime = timer()
        if self.state.paused:
            self.state.endPause(currentTime)
        else:
            self.state.startPause(currentTime)

    def timeSaveSet(self,i):
        self.labels[self.bptstart+i][0].configure(text="Possible Time Save:")

    def diffSet(self,i):
        self.labels[self.bptstart+i][0].configure(text="Last Split (vs Best):")

    def bptSet(self,i):
        self.labels[self.bptstart+i][0].configure(text="Best Possible Time:")

    def sobSet(self,i):
        self.labels[self.bptstart+i][0].configure(text="Sum of Bests:")

    def pbSet(self,i):
        self.labels[self.bptstart+i][0].configure(text="Personal Best:")
        self.labels[self.bptstart+i][1].configure(text=self.state.comparisons[2].getString("totals",-1,{"precision":2}))

    def timeSaveInfo(self,i):
        self.labels[self.bptstart+i][1].configure(text=timeh.timeToString(timeh.difference(self.state.currentComparison.segments[self.state.splitnum],self.state.comparisons[0].segments[self.state.splitnum]),{"precision":2}))

    def diffInfo(self,i):
        if self.state.splitnum > 0:
            self.labels[self.bptstart+i][1].configure(text=self.state.comparisons[0].getString("segmentDiffs",self.state.splitnum-1,{"showSign":True,"precision":2}))

    def bptInfo(self,i):
        self.labels[self.bptstart+i][1].configure(text=timeh.timeToString(self.state.bptList.total,{"precision":2}))

    def sobInfo(self,i):
        self.labels[self.bptstart+i][1].configure(text=timeh.timeToString(self.state.currentBests.total,{"precision":2}))

    def pbInfo(self,i):
        pass
