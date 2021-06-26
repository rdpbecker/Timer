# Run tkinter code in another thread

import tkinter as tk
import threading
from timeit import default_timer as timer
from Components import Menu
from DataClasses import AllSplitNames
from DataClasses import Session
from Dialogs import AddRun
from Dialogs import ConfirmPopup
from Dialogs import RunPopup
from Dialogs import LayoutPopup
from Dialogs import SplitEditor
from States import State

class App(threading.Thread):
    state = None
    components = []
    numWidgets = 0
    retVal = None
    updated = None

    ##########################################################
    ## Initialize the app in a different thread than the state
    ##
    ## Parameters: state - the state of the program
    ##########################################################
    def __init__(self,state,session):
        super().__init__()
        self.state = state
        self.session = session
        self.components = []
        self.numWidgets = 0

    ##########################################################
    ## Add a component to the bottom of the app, and track the
    ## new component.
    ##
    ## Parameters: component - the component to add to the app.
    ##                         Must extend the
    ##                         WidgetBase.WidgetBase class so it
    ##                         has the appropriate signals.
    ##########################################################
    def addWidget(self,component):
        component.grid(row=self.numWidgets,column=0,columnspan=12,sticky='NSWE')
        component.bind('<Configure>',self.updateWeights)
        self.root.rowconfigure(self.numWidgets,weight=1)
        self.numWidgets = self.numWidgets + 1
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
    def updateWidgets(self,signalType,**kwargs):
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

    def updateWeights(self,*args):
        for i in range(self.numWidgets):
            self.root.rowconfigure(i, weight=self.components[i].winfo_height())
        if not len(list(filter(lambda x: x==1,[self.components[i].winfo_height() for i in range(self.numWidgets)]))):
            for component in self.components:
                component.unbind('<Configure>')

    ##########################################################
    ## Set the timer to update every time this is called
    ##########################################################
    def update(self):
        exitCode = self.state.frameUpdate(timer())
        if not exitCode:
            self.updateWidgets("frame")
        elif exitCode == 1:
            self.updateWidgets("preStart")
        self.updater = self.root.after(17,self.update)

    ##########################################################
    ## Initialize the start and first split times when the run
    ## starts
    ##########################################################
    def start(self, event=None):
        if not self.state.onStarted(timer()):
            self.updateWidgets("start")

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
        self.updateWidgets("split")

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
            self.updateWidgets("comp")

    ##########################################################
    ## Stop the run here
    ##########################################################
    def reset(self, event=None):
        if not self.state.onReset():
            self.updateWidgets("reset")

    ##########################################################
    ## Skip a split
    ##########################################################
    def skip(self,event=None):
        if not self.state.onSplitSkipped(timer()):
            self.updateWidgets("skip")

    ##########################################################
    ## If paused, unpause. If not paused, pause.
    ##########################################################
    def togglePause(self,event=None):
        if not self.state.onPaused(timer()):
            self.updateWidgets("pause")

    ##########################################################
    ## Restart the run by resetting the timer state.
    ##########################################################
    def restart(self,event=None):
        if not self.state.onRestart():
            self.updateWidgets("restart")

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

    def setLayout(self,retVal):
        layoutName = retVal["layoutName"]
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
        self.updateWidgets("runChanged",state=self.state)
        self.updateWeights()

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

    def editSplits(self):
        SplitEditor.SplitEditor(self.root,self.newEditedState,self.state)

    def newEditedState(self,retVal):
        compareNum = self.state.compareNum
        session = Session.Session(AllSplitNames.Splits())
        session.setRun(self.state.game,self.state.category)
        self.state = State.State(session)
        self.state.setComparison(compareNum)
        self.updateWidgets("runChanged",state=self.state)

    def addRun(self):
        AddRun.SplitEditorP(self.root,self.addRunState)

    def addRunState(self,retVal):
        compareNum = self.state.compareNum
        session = Session.Session(AllSplitNames.Splits())
        if retVal["game"] and retVal["category"]:
            session.setRun(retVal["game"],retVal["category"])
        else:
            session.setRun(self.state.game,self.state.category)
        self.state = State.State(session)
        self.state.setComparison(compareNum)
        self.updateWidgets("runChanged",state=self.state)
