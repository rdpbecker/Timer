# Run tkinter code in another thread

import Time
import tkinter as tk
import threading
from timeit import default_timer as timer
import State, GeneralInfo, fileio 

class Gui(threading.Thread):
    labels = []
    buttons = []
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
        config = fileio.readJson("config.json")
        generalInfo = {\
            "timeSave": GeneralInfo.GeneralInfo(config["timeSaveShow"],self.timeSaveSet,self.timeSaveInfo),\
            "diff": GeneralInfo.GeneralInfo(config["diffShow"],self.diffSet,self.diffInfo),\
            "bpt": GeneralInfo.GeneralInfo(config["bptShow"],self.bptSet,self.bptInfo),\
            "sob": GeneralInfo.GeneralInfo(config["sobShow"],self.sobSet,self.sobInfo),\
            "pb": GeneralInfo.GeneralInfo(config["pbShow"],self.pbSet,self.pbInfo)\
        }
        generalInfoKeys = ["timeSave","diff","bpt","sob","pb"]
        self.setSectionStarts(config,generalInfo,generalInfoKeys)
        self.state = State.State(self.pbstart,self.splitstart,config)
        self.state.generalInfo = generalInfo
        self.state.generalInfoKeys = generalInfoKeys

        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.configure(background='black')

        ## Initialize the format of the gui and store references to all
        ## the labels so we can change them. References are stored in
        ## a grid
        for i in range(self.splitstart):
            label = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"], width=7, anchor="w")
            label.grid(row=i,column=0,columnspan=2)
            label2 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"], width=18, anchor='w')
            label2.grid(row=i,column=2,columnspan=3)
            label3 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"], width=20, anchor='e')
            label3.grid(row=i,column=5,columnspan=4)
            label4 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"], width=15)
            label4.grid(row=i,column=9,columnspan=3)
            self.labels.append([label,label2,label3,label4])
        for i in range(self.splitstart,self.pbstart):
            label = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"], width=20, anchor="w")
            label.grid(row=i,column=0,columnspan=4)
            label2 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"], width=20, anchor='e')
            label2.grid(row=i,column=4,columnspan=4)
            label3 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"], width=20, anchor='e')
            label3.grid(row=i,column=8,columnspan=4)
            self.labels.append([label,label2,label3])
        for i in range(self.pbstart,self.timer):
            label = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"], width=15, anchor='w')
            label.grid(row=i,column=0,columnspan=3)
            label2 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"], width=15, anchor='w')
            label2.grid(row=i,column=3,columnspan=3)
            label3 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"], width=15, anchor='w')
            label3.grid(row=i,column=6,columnspan=3)
            label4 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"], width=15, anchor='e')
            label4.grid(row=i,column=9,columnspan=3)
            self.labels.append([label,label2,label3,label4])
        anchorlist = ['e','c']
        fontlist = [config['segmentFont'],config['timerFont']]
        colourlist = [config["segmentColour"],config["timerColour"]]
        for i in range(self.timer,self.bptstart):
            label = tk.Label(self.root, bg='black', text="", fg=colourlist[i-self.timer], width=27, font=fontlist[i-self.timer], anchor=anchorlist[i-self.timer])
            label.grid(row=i,column=0,columnspan=12)
            self.labels.append([label])

        for i in range(self.bptstart,self.buttonstart):
            label = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"], width=30, anchor='w')
            label.grid(row=i,column=0,columnspan=6)
            label4 = tk.Label(self.root, bg='black', font=config["mainFont"], text="", fg=config["mainColour"], width=15, anchor='e')
            label4.grid(row=i,column=9,columnspan=3)
            self.labels.append([label,label4])

        button1 = tk.Button(self.root, bg=config["buttonBgColour"], font=config["buttonFont"], text="Change Compare", fg=config["buttonTextColour"], width=15, command=self.guiSwitchCompare)
        button1.grid(row=self.buttonstart,column=6,columnspan=3)
        button2 = tk.Button(self.root, bg=config["buttonBgColour"], font=config["buttonFont"], text="Split", fg=config["buttonTextColour"], width=33, command=self.onSplitEnd)
        self.root.bind('<Return>', self.onSplitEnd)
        button2.grid(row=self.buttonstart+1,column=0,columnspan=6)
        button3 = tk.Button(self.root, bg=config["buttonBgColour"], font=config["buttonFont"], text="Reset", fg=config["buttonTextColour"], width=15, command=self.reset)
        self.root.bind('r', self.reset)
        button3.grid(row=self.buttonstart,column=0,columnspan=3)
        button4 = tk.Button(self.root, bg=config["buttonBgColour"], font=config["buttonFont"], text="Skip Split", fg=config["buttonTextColour"], width=15, command=self.skip)
        self.root.bind('s', self.skip)
        button4.grid(row=self.buttonstart,column=3,columnspan=3)
        button5 = tk.Button(self.root, bg=config["buttonBgColour"], font=config["buttonFont"], text="Start Run", fg=config["buttonTextColour"], width=33, command=self.start)
        button5.grid(row=self.buttonstart+1,column=6,columnspan=6)
        self.root.bind('<space>', self.start)
        button6 = tk.Button(self.root, bg=config["buttonBgColour"], font=config["buttonFont"], text="Pause", fg=config["buttonTextColour"], width=15, command=self.togglePause)
        button6.grid(row=self.buttonstart,column=9,columnspan=3)
        self.root.bind('p', self.togglePause)
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
                elapsed = currentTime - self.state.lastUpdateTime
                self.state.starttime = self.state.starttime + elapsed
                self.state.splitstarttime = self.state.splitstarttime + elapsed
            self.labels[self.timer+1][0].configure(text=Time.Time(2,floattime=currentTime-self.state.starttime).__str__(flag2=0))
            self.labels[self.timer][0].configure(text=Time.Time(0,floattime=currentTime-self.state.splitstarttime).__str__(flag2=0))
            self.state.lastUpdateTime = currentTime
        if self.state.splitnum < len(self.state.splitnames) and not self.state.reset:
            self.root.after(8,self.update)
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
        self.labels[0][3].configure(text="Personal Best")

    ##########################################################
    ## Initialize the split names and times for the first few
    ## splits and the last one. This is based on the PB time
    ##########################################################
    def initTimes(self):
        for i in range(self.state.windowStart,self.pbstart-self.splitstart-2):
            self.labels[self.splitstart+i][0].configure(text=self.state.splitnames[i-self.state.windowStart])
            self.labels[self.splitstart+i][2].configure(text=self.state.compares[self.state.currentCompare].get(i-self.state.windowStart).__str__(precision=2))
        self.labels[self.pbstart-2][0].configure(text=self.state.splitnames[-1])
        self.labels[self.pbstart-2][2].configure(text=self.state.compares[self.state.currentCompare].get(-1).__str__(precision=2))

    ##########################################################
    ## Initialize all the info on the bottom, including split
    ## comparisons, time save, BPT, and PB
    ##########################################################
    def initInfo(self):
        self.labels[self.pbstart][0].configure(text="PB Split:")
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
        windowStart = self.state.getWindowStart()
        for i in range(0,self.pbstart-self.splitstart-1):
            if i == self.state.splitnum-windowStart+self.state.windowStart:
                self.labels[self.splitstart+i][0].configure(fg=self.state.config["activeColour"])
                self.labels[self.splitstart+i][2].configure(fg=self.state.config["activeColour"])
            else:
                self.labels[self.splitstart+i][0].configure(fg=self.state.config["mainColour"])
                self.labels[self.splitstart+i][2].configure(fg=self.state.config["mainColour"])
        self.labels[self.pbstart-2][0].configure(fg=self.state.config["endColour"])
        self.labels[self.pbstart-2][2].configure(fg=self.state.config["endColour"])

    ##########################################################
    ## Update current split and BPT information based on the
    ## current split
    ##########################################################
    def updateInfo(self):
        self.labels[self.pbstart][1].configure(text=self.state.compareSplits[self.state.currentCompare].get(self.state.splitnum).__str__(precision=2))
        self.labels[self.pbstart+1][1].configure(text=self.state.compareSplits[0].get(self.state.splitnum).__str__(precision=2))
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
        if not self.state.started:
            self.start()
            return
        splitEnd = timer()
        totalTime = Time.Time(5,floattime=splitEnd-self.state.starttime)
        splitTime = Time.Time(5,floattime=splitEnd-self.state.splitstarttime)
        self.state.currentSplits.insert(splitTime)
        self.state.currentTotals.insert(totalTime)

        self.state.bptList.replace(Time.Time(5,floattime=splitEnd-self.state.splitstarttime),self.state.splitnum)
        for i in range(4):
            self.state.diffs[i].insert(totalTime.subtract(self.state.compares[i].get(self.state.splitnum)))
            self.state.diffSplits[i].insert(self.state.currentSplits.get(self.state.splitnum).subtract(self.state.compareSplits[i].get(self.state.splitnum)))
        if self.state.diffSplits[0].get(self.state.splitnum).greater(Time.Time(5,timestring='-')) == -1:
            self.state.currentBests.replace(Time.Time(5,floattime=splitEnd-self.state.splitstarttime),self.state.splitnum)
        self.state.splitnum = self.state.splitnum + 1
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
        ## 
        ## windowStart is the index at which the window in the GUI starts
        ## This is determined only by the total number of splits, and
        ## for categories with more than 7 splits windowStart=0
        for i in range(self.state.windowStart,self.pbstart-self.splitstart-2):
            ## The index of the split we're looking at currently
            subjectSplitIndex = i+lowIndex-self.state.windowStart
            self.labels[self.splitstart+i][0].configure(text=self.state.splitnames[subjectSplitIndex])
            if self.state.splitnum > subjectSplitIndex:
                if not self.state.compareSplits[self.state.currentCompare].get(subjectSplitIndex).equal(Time.Time(5,timestring='-')):
                    self.labels[self.splitstart+i][1].configure(text=self.state.diffs[self.state.currentCompare].get(subjectSplitIndex).__str__(1,precision=2))
                else:
                    self.labels[self.splitstart+i][1].configure(text='-')
                self.labels[self.splitstart+i][2].configure(text=self.state.currentTotals.get(subjectSplitIndex).__str__(precision=2))
                if self.state.diffSplits[0].get(subjectSplitIndex).greater(Time.Time(5,timestring='-')) == -1:
                    self.labels[self.splitstart+i][1].configure(fg='gold')
                elif (self.state.diffs[self.state.currentCompare].get(subjectSplitIndex).greater(Time.Time(5,timestring='-')) == -1) or (self.state.compareSplits[self.state.currentCompare].get(subjectSplitIndex).equal(Time.Time(2,timestring='-'))):
                    self.labels[self.splitstart+i][1].configure(fg='green')
                else:
                    self.labels[self.splitstart+i][1].configure(fg='red')
            else:
                self.labels[self.splitstart+i][1].configure(text="")
                self.labels[self.splitstart+i][2].configure(text=self.state.compares[self.state.currentCompare].get(subjectSplitIndex).__str__(precision=2))
        if self.state.splitnum >= len(self.state.splitnames):
            self.labels[self.pbstart-2][1].configure(text=self.state.diffs[self.state.currentCompare].get(-1).__str__(1,precision=2))
            self.labels[self.pbstart-2][2].configure(text=self.state.currentTotals.get(-1).__str__(precision=2))
            if self.state.diffs[0].get(-1).greater(Time.Time(5,timestring='-')) == -1:
                self.labels[self.pbstart-2][1].configure(fg='gold')
            elif self.state.diffs[self.state.currentCompare].get(-1).greater(Time.Time(5,timestring='-')) == -1:
                self.labels[self.pbstart-2][1].configure(fg='green')
            else:
                self.labels[self.pbstart-2][1].configure(fg='red')

    ##########################################################
    ## Update information about the comparison splits when the 
    ## comparison is changed
    ##########################################################
    def updateCompare(self):
        self.labels[0][3].configure(text=self.state.compareHeaders[self.state.currentCompare])
        self.labels[self.pbstart][0].configure(text=self.state.splitCompareHeaders[self.state.currentCompare]+":")
        self.labels[self.pbstart-2][2].configure(text=self.state.compares[self.state.currentCompare].get(-1).__str__(precision=2))

    ##########################################################
    ## The function called when the 'Switch Compare' button is
    ## clicked
    ##########################################################
    def guiSwitchCompare(self,event=None):
        self.state.currentCompare = (self.state.currentCompare+1)%4
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
        self.state.currentSplits.insert(splitTime)
        self.state.currentTotals.insert(totalTime)

        for i in range(4):
            self.state.diffs[i].insert(Time.Time(5,floattime=0))
            self.state.diffSplits[i].insert(Time.Time(5,floattime=0))
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
            self.state.pauseTime = 0
        else:
            self.state.paused = True
            self.state.pauseTime = currentTime
        self.state.lastUpdateTime = currentTime

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
        self.labels[self.bptstart+i][1].configure(text=self.state.compares[2].get(-1).__str__(precision=2))

    def timeSaveInfo(self,i):
        self.labels[self.bptstart+i][1].configure(text=self.state.compareSplits[self.state.currentCompare].get(self.state.splitnum).subtract(self.state.compareSplits[0].get(self.state.splitnum)).__str__(precision=2))

    def diffInfo(self,i):
        if self.state.splitnum > 0:
            self.labels[self.bptstart+i][1].configure(text=self.state.currentSplits.get(-1).subtract(self.state.compareSplits[0].get(self.state.splitnum-1)).__str__(1,precision=2))

    def bptInfo(self,i):
        self.labels[self.bptstart+i][1].configure(text=self.state.bptList.sum().__str__(precision=2))

    def sobInfo(self,i):
        self.labels[self.bptstart+i][1].configure(text=self.state.currentBests.sum().__str__(precision=2))

    def pbInfo(self,i):
        pass
