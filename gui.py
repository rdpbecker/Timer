# Run tkinter code in another thread

import timeHelpers as timeh
import tkinter as tk
import threading
from timeit import default_timer as timer
import readConfig as rc

class Gui(threading.Thread):
    labels = []
    backgrounds = []
    state = None
    components = []
    numComponents = 0

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

        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.configure(background=config["root"]["colours"]["bg"])

        for i in range(12):
            self.root.columnconfigure(i,minsize=40,weight=1)

        self.setHotkeys()

    def startGui(self):
        self.root.after(8,self.update)
        self.root.mainloop()

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
            self.updateComponents("frame")
        if self.state.splitnum < len(self.state.splitnames) and not self.state.reset:
            self.root.after(17,self.update)
        else:
            self.root.after(1,self.state.doEnd)

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
        self.updateComponents("split")

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
        self.updateComponents("skip")

    def togglePause(self,event=None):
        currentTime = timer()
        if self.state.paused:
            self.state.endPause(currentTime)
        else:
            self.state.startPause(currentTime)
        self.updateComponents("pause")
