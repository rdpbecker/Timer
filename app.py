# Run tkinter code in another thread

import tkinter as tk
from tkinter import messagebox as mb
import threading
from timeit import default_timer as timer
from Components import Menu
from Dialogs import ConfirmPopup
from Dialogs import RunPopup
from Dialogs import LayoutPopup
from States import State

class App(threading.Thread):
    state = None
    components = []
    numComponents = 0
    retVal = None
    updated = None

    ##########################################################
    ## Initialize the app in a different thread than the state
    ##
    ## Parameters: state - the state of the program
    ##########################################################
    def __init__(self,state,session):
        threading.Thread.__init__(self)
        self.state = state
        self.session = session
        self.components = []
        self.numComponents = 0

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
        component.grid(row=self.numComponents,column=0,columnspan=12,sticky='NSWE')
        self.numComponents = self.numComponents + 1
        self.components.append(component)

    ##########################################################
    ## Calls the signal on the given component of the
    ## specified type.
    ##
    ## Parameters: component - the component to update
    ##             signalType - the signal to dispatch
    ##########################################################
    def switchSignal(self,component,signalType,**kwargs):
        signals = {
            "frame": component.frameUpdate,
            "start": component.onStarted,
            "split": component.onSplit,
            "comp": component.onComparisonChanged,
            "pause": component.onPaused,
            "skip": component.onSplitSkipped,
            "reset": component.onReset,
            "restart": component.onRestart,
            "runChanged": component.runChanged,
            "preStart": component.preStart
        }
        signals.get(signalType)(**kwargs)

    ##########################################################
    ## Updates all the components with a given signal type.
    ##
    ## Parameters: signalType - the type of signal to dispatch
    ##########################################################
    def updateComponents(self,signalType,**kwargs):
        for component in self.components:
            self.switchSignal(component,signalType,**kwargs)

    ##########################################################
    ## Creates the window with the destruction callback, and
    ## sets control callbacks.
    ##########################################################
    def setupGui(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.finish)
        self.root.title("Base Timer")
        for i in range(12):
            self.root.columnconfigure(i,weight=1)
        if (self.state.config["showMenu"]):
            self.root.configure(menu=Menu.ControlMenu(self))

    ##########################################################
    ## Show the window, and call the first update after one
    ## frame.
    ##########################################################
    def startGui(self):
        self.root.after(17,self.update)
        self.root.mainloop()
        return self.retVal

    ##########################################################
    ## Set the timer to update every time this is called
    ##########################################################
    def update(self):
        exitCode = self.state.frameUpdate(timer())
        if not exitCode:
            self.updateComponents("frame")
        elif exitCode == 1:
            self.updateComponents("preStart")
        self.updater = self.root.after(17,self.update)

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
        if not self.state.onComparisonChanged(rotation):
            self.updateComponents("comp")

    ##########################################################
    ## Stop the run here
    ##########################################################
    def reset(self, event=None):
        if not self.state.onReset():
            self.updateComponents("reset")

    ##########################################################
    ## Skip a split
    ##########################################################
    def skip(self,event=None):
        if not self.state.onSplitSkipped(timer()):
            self.updateComponents("skip")

    ##########################################################
    ## If paused, unpause. If not paused, pause.
    ##########################################################
    def togglePause(self,event=None):
        if not self.state.onPaused(timer()):
            self.updateComponents("pause")

    ##########################################################
    ## Restart the run by resetting the timer state.
    ##########################################################
    def restart(self,event=None):
        if not self.state.onRestart():
            self.updateComponents("restart")

    ##########################################################
    ## Saves the data stored in the state.
    ##########################################################
    def save(self,event=None):
        self.state.saveTimes()

    ##########################################################
    ## Opens a window to change the current layout
    ##########################################################
    def chooseLayout(self,event=None):
        if self.state.started:
            return
        LayoutPopup.LayoutPopup(self.root,self.setLayout,self.session).show()

    def setLayout(self,layoutName):
        if not layoutName == self.session.layoutName:
            self.session.setLayout(layoutName)
            self.retVal = 1
            self.finish()

    ##########################################################
    ## Opens a window to change the current run
    ##########################################################
    def chooseRun(self,event=None):
        if self.state.started:
            return
        newRun = RunPopup.RunPopup(self.root,self.setRun,self.session).show()

    def setRun(self,newSession):
        if newSession["game"] == self.state.game\
            and newSession["category"] == self.state.category:
            return
        if self.state.unSaved:
            self.confirmSave(self.saveIfDesired)
        compareNum = self.state.compareNum
        self.session.setRun(newSession["game"],newSession["category"])
        self.state = State.State(self.session)
        self.state.setComparison(compareNum)
        self.updateComponents("runChanged",state=self.state)

    def saveIfDesired(self,desired):
        if desired:
            self.save()

    ##########################################################
    ## Save the splits before closing the window or changing the
    ## run.
    ##########################################################
    def confirmSave(self,callback):
        ConfirmPopup.ConfirmPopup(\
            self.root,\
            callback,\
            "Save",\
            "Save local changes (closing will save automatically)?"\
        )

    ##########################################################
    ## Finish the run by saving the splits and closing the
    ## window.
    ##########################################################
    def finish(self,event=None):
        if not self.state.shouldFinish():
            return
        if self.state.unSaved:
            self.confirmSave(self.close)
        else:
            self.close(False)

    def close(self,shouldSave):
        if shouldSave:
            self.save()
        if self.updater:
            self.root.after_cancel(self.updater)
        self.root.destroy()
