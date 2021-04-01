# Run tkinter code in another thread

import Time
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
        colourlist = [config["segmentColour"],config["timerColour"]]
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
            self.labels[self.timer+1][0].configure(text=timeh.timeToString(currentTime-self.state.starttime,blankToDash=False,precision=2))
            self.labels[self.timer][0].configure(text=timeh.timeToString(currentTime-self.state.splitstarttime,blankToDash=False))
        if self.state.splitnum < len(self.state.splitnames) and not self.state.reset:
            self.root.after(17,self.update)
        else:
            self.root.after(1,self.state.doEnd)

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
        self.labels[0][3].configure(text=self.state.comparisons[self.state.currentCompare].totalHeader)

    ##########################################################
    ## Initialize the split names and times for the first few
    ## splits and the last one. This is based on the PB time
    ##########################################################
    def initTimes(self):
        for i in range(0,self.pbstart-self.splitstart-2):
            self.labels[self.splitstart+i][0].configure(text=self.state.splitnames[i])
            self.labels[self.splitstart+i][2].configure(text=timeh.timeToString(self.state.comparisons[self.state.currentCompare].totals[i],precision=2))
        self.labels[self.pbstart-2][0].configure(text=self.state.splitnames[-1])
        self.labels[self.pbstart-2][2].configure(text=timeh.timeToString(self.state.comparisons[self.state.currentCompare].totals[-1],precision=2))

    ##########################################################
    ## Initialize all the info on the bottom, including split
    ## comparisons, time save, BPT, and PB
    ##########################################################
    def initInfo(self):
        self.labels[self.pbstart][0].configure(text=self.state.comparisons[self.state.currentCompare].segmentHeader)
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
        lowIndex = self.state.getWindowStart()
        for i in range(0,self.pbstart-self.splitstart-1):
            if i == self.state.splitnum-lowIndex:
                self.labels[self.splitstart+i][0].configure(fg=self.state.config["activeColour"],bg=self.state.config["activeBgColour"])
                self.labels[self.splitstart+i][2].configure(fg=self.state.config["activeColour"],bg=self.state.config["activeBgColour"])
                self.backgrounds[i].configure(bg=self.state.config["activeBgColour"])
            else:
                self.labels[self.splitstart+i][0].configure(fg=self.state.config["mainColour"],bg='black')
                self.labels[self.splitstart+i][2].configure(fg=self.state.config["mainColour"],bg='black')
                self.backgrounds[i].configure(bg='black')
        self.labels[self.pbstart-2][0].configure(fg=self.state.config["endColour"])
        self.labels[self.pbstart-2][2].configure(fg=self.state.config["endColour"])

    ##########################################################
    ## Update current split and BPT information based on the
    ## current split
    ##########################################################
    def updateInfo(self):
        self.labels[self.pbstart][1].configure(text=timeh.timeToString(self.state.comparisons[self.state.currentCompare].segments[self.state.splitnum],precision=2))
        self.labels[self.pbstart+1][1].configure(text=timeh.timeToString(self.state.comparisons[0].segments[self.state.splitnum],precision=2))
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
        lowIndex = self.state.getWindowStart()
        self.updateTimes(lowIndex)
        self.updateCurrentColour()
        if self.state.splitnum < len(self.state.splitnames):
            self.updateInfo()
        self.state.splitstarttime = splitEnd

    ##########################################################
    ## Update the times and split names in the split portion 
    ## of the GUI. This includes shifting entries as needed so
    ## the current split is the third entry in the list, and 
    ## colouring the diff numbers properly
    ##
    ## Parameters: lowIndex - the index in state.splitNames of
    ##                        the split at the top of the 
    ##                        section
    ##########################################################
    def updateTimes(self,lowIndex):
        ## i is the number from the top of the list of splits. For the 
        ## top entry i=0, the next one down has i=1, and so on
        ##
        ## lowIndex is the index in the list of splits of the top split
        ## in the gui - if split #5 is at the top of the view area in
        ## the gui, then lowIndex=5
        for i in range(0,self.pbstart-self.splitstart-2):
            ## The index of the split we're looking at currently
            subjectSplitIndex = i+lowIndex
            self.labels[self.splitstart+i][0].configure(text=self.state.splitnames[subjectSplitIndex])
            if self.state.splitnum > subjectSplitIndex:
                if self.state.comparisons[self.state.currentCompare].segments[subjectSplitIndex]:
                    self.labels[self.splitstart+i][1].configure(text=timeh.timeToString(self.state.comparisons[self.state.currentCompare].totalDiffs[subjectSplitIndex],showSign=True,precision=2))
                else:
                    self.labels[self.splitstart+i][1].configure(text='-')
                self.labels[self.splitstart+i][2].configure(text=timeh.timeToString(self.state.currentRun.totals[subjectSplitIndex],precision=2))
                if timeh.greater(0,self.state.comparisons[0].segmentDiffs[subjectSplitIndex]):
                    self.labels[self.splitstart+i][1].configure(fg='gold')
                elif timeh.greater(0,self.state.comparisons[self.state.currentCompare].totalDiffs[subjectSplitIndex]):
                    self.labels[self.splitstart+i][1].configure(fg='green')
                else:
                    self.labels[self.splitstart+i][1].configure(fg='red')
            else:
                self.labels[self.splitstart+i][1].configure(text="")
                self.labels[self.splitstart+i][2].configure(text=timeh.timeToString(self.state.comparisons[self.state.currentCompare].totals[subjectSplitIndex],precision=2))
        if self.state.splitnum >= len(self.state.splitnames):
            self.labels[self.pbstart-2][1].configure(text=timeh.timeToString(self.state.comparisons[self.state.currentCompare].totalDiffs[-1],showSign=True,precision=2))
            self.labels[self.pbstart-2][2].configure(text=timeh.timeToString(self.state.currentRun.totals[-1],precision=2))
            if timeh.greater(0,self.state.comparisons[0].segmentDiffs[-1]):
                self.labels[self.pbstart-2][1].configure(fg='gold')
            elif timeh.greater(0,self.state.comparisons[self.state.currentCompare].totalDiffs[-1]):
                self.labels[self.pbstart-2][1].configure(fg='green')
            else:
                self.labels[self.pbstart-2][1].configure(fg='red')

    ##########################################################
    ## Update information about the comparison splits when the 
    ## comparison is changed
    ##########################################################
    def updateCompare(self):
        self.labels[0][3].configure(text=self.state.comparisons[self.state.currentCompare].totalHeader)
        self.labels[self.pbstart][0].configure(text=self.state.comparisons[self.state.currentCompare].segmentHeader+":")
        self.labels[self.pbstart-2][2].configure(text=timeh.timeToString(self.state.comparisons[self.state.currentCompare].totals[-1],precision=2))

    ##########################################################
    ## The function called when the 'Switch Compare' button is
    ## clicked
    ##########################################################
    def guiSwitchCompare(self,event=None):
        self.state.currentCompare = (self.state.currentCompare+1)%self.state.numComparisons
        lowIndex = self.state.getWindowStart()
        self.updateTimes(lowIndex)
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
        totalTime = Time.Time(5,floattime=0)
        splitTime = Time.Time(5,floattime=0)
        self.state.currentRun.addSegment("BLANK","BLANK")

        for i in range(self.state.numComparisons):
            self.state.comparisons[i].totalDiffs.append("BLANK")
            self.state.comparisons[i].segmentDiffs.append("BLANK")
        self.state.splitnum = self.state.splitnum + 1
        lowIndex = self.state.getWindowStart()
        self.updateTimes(lowIndex)
        self.updateCurrentColour()
        if self.state.splitnum < len(self.state.splitnames):
            self.updateInfo()
        self.state.splitstarttime = splitEnd

    def togglePause(self,event=None):
        currentTime = timer()
        if self.state.paused:
            self.state.paused = False
            elapsed = currentTime - self.state.pauseTime
            self.state.starttime = self.state.starttime + elapsed
            self.state.splitstarttime = self.state.splitstarttime + elapsed
            self.state.pauseTime = 0
        else:
            self.state.paused = True
            self.state.pauseTime = currentTime

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
        self.labels[self.bptstart+i][1].configure(text=timeh.timeToString(self.state.comparisons[2].totals[-1],precision=2))

    def timeSaveInfo(self,i):
        self.labels[self.bptstart+i][1].configure(text=timeh.timeToString(timeh.difference(self.state.comparisons[self.state.currentCompare].segments[self.state.splitnum],self.state.comparisons[0].segments[self.state.splitnum]),precision=2))

    def diffInfo(self,i):
        if self.state.splitnum > 0:
            self.labels[self.bptstart+i][1].configure(text=timeh.timeToString(self.state.comparisons[0].segmentDiffs[self.state.splitnum-1],showSign=True,precision=2))

    def bptInfo(self,i):
        self.labels[self.bptstart+i][1].configure(text=timeh.timeToString(self.state.bptList.total,precision=2))

    def sobInfo(self,i):
        self.labels[self.bptstart+i][1].configure(text=timeh.timeToString(self.state.currentBests.total,precision=2))

    def pbInfo(self,i):
        pass
