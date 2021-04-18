# Run tkinter code in another thread

import tkinter as tk
import threading
from timeit import default_timer as timer

class App(threading.Thread):
    state = None
    components = []
    numComponents = 0

    ##########################################################
    ## Initialize the app in a different thread than the state
    ##
    ## Parameters: state - the state of the program
    ##########################################################
    def __init__(self,state):
        threading.Thread.__init__(self)
        self.state = state

    ##########################################################
    ## Add a component to the bottom of the app, and track the
    ## new component.
    ##
    ## Parameters: component - the component to add to the app.
    ##                         Must extend the
    ##                         Component.Component class so it
    ##                         has the appropriate signals.
    ##########################################################
    def addComponent(self,component):
        component.grid(row=self.numComponents,column=0,columnspan=12,sticky='WE')
        self.numComponents = self.numComponents + 1
        self.components.append(component)

    ##########################################################
    ## Calls the signal on the given component of the
    ## specified type.
    ##
    ## Parameters: component - the component to update
    ##             signalType - the signal to dispatch
    ##########################################################
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

    ##########################################################
    ## Updates all the components with a given signal type.
    ##
    ## Parameters: signalType - the type of signal to dispatch
    ##########################################################
    def updateComponents(self,signalType):
        for component in self.components:
            self.switchSignal(component,signalType)

    ##########################################################
    ## Creates the window with the destruction callback, and
    ## sets control callbacks.
    ##########################################################
    def setupGui(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)
        self.setHotkeys()

    ##########################################################
    ## Show the window, and call the first update after one
    ## frame.
    ##########################################################
    def startGui(self):
        self.root.after(17,self.update)
        self.root.mainloop()

    ##########################################################
    ## Sets the hotkeys for the window.
    ##########################################################
    def setHotkeys(self):
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
        if not self.state.frameUpdate(timer()):
            self.updateComponents("frame")
        self.root.after(17,self.update)

    ##########################################################
    ## Initialize the start and first split times when the run
    ## starts
    ##########################################################
    def start(self, event=None):
        if not self.state.onStarted(timer()):
            self.updateComponents("start")

    ##########################################################
    ## At the end of each split, record and store the times, 
    ## calculate all the diffs, and call the helper functions 
    ## to update the GUI
    ##########################################################
    def onSplitEnd(self,event=None):
        exitCode = self.state.onSplit(timer())
        if exitCode == 1:
            return
        elif exitCode == 2:
            self.togglePause()
        self.updateComponents("split")

    ##########################################################
    ## Move the comparison counter-clockwise (backwards)
    ##########################################################
    def guiSwitchCompareCCW(self,event=None):
        self.rotateCompare(-1)

    ##########################################################
    ## Move the comparison clockwise (forwards)
    ##########################################################
    def guiSwitchCompareCW(self,event=None):
        self.rotateCompare(1)

    ##########################################################
    ## The function called when the 'Switch Compare' button is
    ## clicked
    ##########################################################
    def rotateCompare(self,rotation):
        self.state.onComparisonChanged(rotation)
        self.updateComponents("comp")

    ##########################################################
    ## Stop the run here
    ##########################################################
    def reset(self, event=None):
        self.state.onReset()
        self.updateComponents("reset")

    ##########################################################
    ## Skip a split
    ##########################################################
    def skip(self,event=None):
        self.state.onSplitSkipped(timer())
        self.updateComponents("skip")

    ##########################################################
    ## If paused, unpause. If not paused, pause.
    ##########################################################
    def togglePause(self,event=None):
        self.state.onPaused(timer())
        self.updateComponents("pause")
