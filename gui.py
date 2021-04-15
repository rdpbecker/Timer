# Run tkinter code in another thread

import timeHelpers as timeh
import tkinter as tk
import threading
from timeit import default_timer as timer
import readConfig as rc

class Gui(threading.Thread):
    labels = []
    backgrounds = []
    splitstart = 2
    pbstart = 10
    timer = 12
    state = None
    components = []

    def __init__(self,state):
        threading.Thread.__init__(self)
        self.state = state

    def callback(self):
        self.root.quit()

    def addComponent(self,component):
        component.grid(row=self.numComponents,column=0,columnspan=12,sticky='WE')
        self.numComponents = self.numComponents + 1
        self.components.append(component)

    def switchSignal(self,component,signalType):
        signals = {
            "frame": component.frameUpdate,
            "start": component.onStarted,
            "split": component.onSplit,
            "comp": component.onComparisonChanged,
            "pause": component.onPaused,
            "skip": component.onSplitSkipped,
            "reset": component.onReset
        }
        signals.get(signalType)()

    def updateComponents(self,signalType):
        for component in self.components:
            self.switchSignal(component,signalType)

    def setupGui(self):
        config = self.state.config
        self.setSectionStarts(config)

        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.configure(background=config["root"]["colours"]["bg"])

        for i in range(12):
            self.root.columnconfigure(i,minsize=40,weight=1)

        ## Initialize the format of the gui and store references to all
        ## the labels so we can change them. References are stored in
        ## a grid

        ## The Title rows
        for i in range(self.splitstart):
            label = tk.Label(self.root, bg=config["root"]["colours"]["bg"], font=config["root"]["font"], text="", fg=config["root"]["colours"]["text"])
            label.grid(row=i,column=0,columnspan=2,sticky='W',ipadx=10)
            label2 = tk.Label(self.root, bg=config["root"]["colours"]["bg"], font=config["root"]["font"], text="", fg=config["root"]["colours"]["text"])
            label2.grid(row=i,column=2,columnspan=3,sticky='W')
            label3 = tk.Label(self.root, bg=config["root"]["colours"]["bg"], font=config["root"]["font"], text="", fg=config["root"]["colours"]["text"])
            label3.grid(row=i,column=5,columnspan=4,sticky='E')
            label4 = tk.Label(self.root, bg=config["root"]["colours"]["bg"], font=config["root"]["font"], text="", fg=config["root"]["colours"]["text"])
            label4.grid(row=i,column=9,columnspan=3,sticky='E',ipadx=10)
            self.labels.append([label,label2,label3,label4])

        ## Splits and comparisons
        for i in range(self.splitstart,self.pbstart):
            background = tk.Frame(self.root, bg=config["root"]["colours"]["bg"])
            background.grid(row=i,column=0,columnspan=12,sticky='NSWE')
            self.backgrounds.append(background)
            label = tk.Label(self.root, bg=config["root"]["colours"]["bg"], font=config["root"]["font"], text="", fg=config["root"]["colours"]["text"])
            label.grid(row=i,column=0,columnspan=8,sticky='W',padx=10)
            label2 = tk.Label(self.root, bg=config["root"]["colours"]["bg"], font=config["root"]["font"], text="", fg=config["root"]["colours"]["text"])
            label2.grid(row=i,column=8,columnspan=2,sticky='E')
            label3 = tk.Label(self.root, bg=config["root"]["colours"]["bg"], font=config["root"]["font"], text="", fg=config["root"]["colours"]["text"])
            label3.grid(row=i,column=10,columnspan=2,sticky='E',padx=10)
            self.labels.append([label,label2,label3])

        ## Current segment comparisons
        for i in range(self.pbstart,self.timer):
            label = tk.Label(self.root, bg=config["root"]["colours"]["bg"], font=config["root"]["font"], text="", fg=config["root"]["colours"]["text"])
            label.grid(row=i,column=0,columnspan=3,sticky='W',padx=10)
            label2 = tk.Label(self.root, bg=config["root"]["colours"]["bg"], font=config["root"]["font"], text="", fg=config["root"]["colours"]["text"])
            label2.grid(row=i,column=3,columnspan=3,sticky='W')
            label3 = tk.Label(self.root, bg=config["root"]["colours"]["bg"], font=config["root"]["font"], text="", fg=config["root"]["colours"]["text"])
            label3.grid(row=i,column=6,columnspan=3,sticky='W')
            label4 = tk.Label(self.root, bg=config["root"]["colours"]["bg"], font=config["root"]["font"], text="", fg=config["root"]["colours"]["text"])
            label4.grid(row=i,column=9,columnspan=3,sticky='E',padx=10)
            self.labels.append([label,label2,label3,label4])

        self.setHotkeys()

        ## Initialize the text in the gui and set the timer to update 
        ## at 125ish FPS
        self.initialize()

    def startGui(self):
        self.root.after(8,self.update)

        self.root.mainloop()

    def setSectionStarts(self,config):
        self.pbstart = self.splitstart + config["numSplits"] + 1
        self.timer = self.pbstart + 2
        self.numComponents = self.timer + 2

    def setHotkeys(self):
        rc.validateHotkeys(self.state.config)
        self.root.bind(self.state.config["hotkeys"]["decreaseComparison"],self.guiSwitchCompareCCW)
        self.root.bind(self.state.config["hotkeys"]["increaseComparison"],self.guiSwitchCompareCW)
        self.root.bind(self.state.config["hotkeys"]["split"], self.onSplitEnd)
        self.root.bind(self.state.config["hotkeys"]["reset"], self.reset)
        self.root.bind(self.state.config["hotkeys"]["skip"], self.skip)
        self.root.bind(self.state.config["hotkeys"]["start"], self.start)
        self.root.bind(self.state.config["hotkeys"]["pause"], self.togglePause)

    ##########################################################
    ## Set the timer to update every time this is called
    ##########################################################
    def update(self):
        if self.state.started:
            currentTime = timer()
            if self.state.paused:
                currentTime = self.state.pauseTime
            self.state.setTimes(currentTime)
            # if behind gold or behind current comparison total,
            # show the diff column for the current split in the
            # split area. If either is blank, ignore the comparison
            if self.state.splitnum < len(self.state.splitnames) \
                and (not timeh.greater(self.state.currentComparison.totals[self.state.splitnum],self.state.totalTime)\
                or not timeh.greater(self.state.comparisons[0].segments[self.state.splitnum],self.state.segmentTime)):
                self.showCurrentSplitDiff()
            self.updateComponents("frame")
        if self.state.splitnum < len(self.state.splitnames) and not self.state.reset:
            self.root.after(17,self.update)
        else:
            self.root.after(1,self.state.doEnd)

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
        self.labels[self.pbstart][0].configure(text=self.state.currentComparison.segmentHeader+":")
        self.labels[self.pbstart+1][0].configure(text="Best Split:")

        self.updateInfo()

    ##########################################################
    ## Set the colours for the current and last splits based
    ## on the current split number
    ##########################################################
    def updateCurrentColour(self):
        lowIndex = self.state.getTopSplitIndex()
        for i in range(0,self.pbstart-self.splitstart-1):
            if i == self.state.splitnum-lowIndex:
                self.labels[self.splitstart+i][0].configure(fg=self.state.config["activeHighlight"]["colours"]["text"],bg=self.state.config["activeHighlight"]["colours"]["bg"])
                self.labels[self.splitstart+i][1].configure(bg=self.state.config["activeHighlight"]["colours"]["bg"])
                self.labels[self.splitstart+i][2].configure(fg=self.state.config["activeHighlight"]["colours"]["text"],bg=self.state.config["activeHighlight"]["colours"]["bg"])
                self.backgrounds[i].configure(bg=self.state.config["activeHighlight"]["colours"]["bg"])
            else:
                self.labels[self.splitstart+i][0].configure(fg=self.state.config["root"]["colours"]["text"],bg=self.state.config["root"]["colours"]["bg"])
                self.labels[self.splitstart+i][1].configure(bg=self.state.config["root"]["colours"]["bg"])
                self.labels[self.splitstart+i][2].configure(fg=self.state.config["root"]["colours"]["text"],bg=self.state.config["root"]["colours"]["bg"])
                self.backgrounds[i].configure(bg=self.state.config["root"]["colours"]["bg"])
        self.labels[self.pbstart-2][0].configure(fg=self.state.config["endColour"])
        self.labels[self.pbstart-2][2].configure(fg=self.state.config["endColour"])

    ##########################################################
    ## Update current split and BPT information based on the
    ## current split
    ##########################################################
    def updateInfo(self):
        self.labels[self.pbstart][1].configure(text=self.state.currentComparison.getString("segments",self.state.splitnum,{"precision":2}))
        self.labels[self.pbstart+1][1].configure(text=self.state.comparisons[0].getString("segments",self.state.splitnum,{"precision":2}))

    ##########################################################
    ## Initialize the start and first split times when the run
    ## starts
    ##########################################################
    def start(self, event=None):
        currentTime = timer()
        if self.state.started:
            return
        self.state.starttime = currentTime
        self.state.splitstarttime = currentTime
        self.state.started = True
        self.updateComponents("start")

    ##########################################################
    ## At the end of each split, record and store the times, 
    ## calculate all the diffs, and call the helper functions 
    ## to update the GUI
    ##########################################################
    def onSplitEnd(self,event=None):
        splitEnd = timer()
        if not self.state.started:
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
        self.updateComponents("split")

    def getCurrentDiffColour(self,segmentDiff,totalDiff):
        if timeh.greater(0,totalDiff):
            # if comparison segment is blank or current segment is
            # ahead
            if timeh.greater(0,segmentDiff):
                return self.state.config["diff"]["colours"]["aheadGaining"]
            else:
                return self.state.config["diff"]["colours"]["aheadLosing"]
        else:
            # if comparison segment is blank or current segment is
            # behind
            if timeh.greater(segmentDiff,0):
                return self.state.config["diff"]["colours"]["behindLosing"]
            else:
                return self.state.config["diff"]["colours"]["behindGaining"]

    def findDiffColour(self,splitIndex):
        # Either the split in this run is blank, or we're comparing
        # to something that's blank
        if \
            timeh.isBlank(self.state.currentRun.totals[splitIndex]) \
            or timeh.isBlank(self.state.currentComparison.totals[splitIndex]):
            return self.state.config["diff"]["colours"]["skipped"]
        # This split is the best ever. Mark it with the gold colour
        elif not timeh.isBlank(self.state.comparisons[0].segmentDiffs[splitIndex]) \
            and timeh.greater(0,self.state.comparisons[0].segmentDiffs[splitIndex]):
            return self.state.config["diff"]["colours"]["gold"]
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

    def guiSwitchCompareCCW(self,event=None):
        self.rotateCompare(-1)

    def guiSwitchCompareCW(self,event=None):
        self.rotateCompare(1)

    ##########################################################
    ## The function called when the 'Switch Compare' button is
    ## clicked
    ##########################################################
    def rotateCompare(self,rotation):
        self.state.compareNum = (self.state.compareNum+rotation)%self.state.numComparisons
        self.state.currentComparison = self.state.comparisons[self.state.compareNum]
        self.updateTimes()
        self.updateInfo()
        self.updateCompare()
        self.updateComponents("comp")

    ##########################################################
    ## Stop the run here
    ##########################################################
    def reset(self, event=None):
        self.state.reset = True
        self.updateComponents("reset")

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
        self.updateComponents("skip")

    def togglePause(self,event=None):
        currentTime = timer()
        if self.state.paused:
            self.state.endPause(currentTime)
        else:
            self.state.startPause(currentTime)
        self.updateComponents("pause")
