# Run tkinter code in another thread

import tkinter as tk
import threading
from timeit import default_timer as timer
from Components import MainMenu
from DataClasses import AllSplitNames
from DataClasses import Session
from Dialogs import AddRun
from Dialogs import ConfirmPopup
from Dialogs import RunPopup
from Dialogs import LayoutPopup
from Dialogs import PracticeRunSelector
from Dialogs import SplitEditor
from States import PracticeState
from States import State
from util import timeHelpers as timeh

class App(threading.Thread):
    # state = None
    # components = []
    # numWidgets = 0
    # session = None
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
        signals.get(signalType,component.frameUpdate)(**kwargs)

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
    def setupGui(self,isPractice=False,showMenu=True):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.finish)
        self.root.title("Base Timer")
        for i in range(12):
            self.root.columnconfigure(i,weight=1)
        if isPractice:
            self.menu = MainMenu.PracticeMenu(self)
            self.root.configure(menu=self.menu)
        elif (showMenu):
            self.menu = MainMenu.Menu(self)
            self.root.configure(menu=self.menu)
        else:
            self.menu = None

    ##########################################################
    ## Show the window, and call the first update after one
    ## frame.
    ##########################################################
    def startGui(self):
        self.root.after(17,self.update)
        self.root.mainloop()
        return self.retVal

    def updateWeights(self,*_):
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
    def start(self, _=None):
        if not self.state.onStarted(timer()):
            self.updateWidgets("start")
            if self.menu:
                self.menu.updateMenuState("during")

    ##########################################################
    ## If the event is really an event, replace it with a
    ## dictionary that has a single key indicating the current
    ## system time. This is a hacky way of detecting whether
    ## we've called a function directly or by the user
    ## pressing a button, and doesn't break anything because
    ## we don't actually use event properties for anything. 
    ##
    ## Functions are only called directly when loading a
    ## partially completed run.
    ##########################################################
    def misconstrueEvent(self,event):
        if type(event) != dict:
            event = {}
        event["system"] = timer()
        return event
        
    ##########################################################
    ## At the end of each split, record and store the times, 
    ## calculate all the diffs, and call the helper functions 
    ## to update the GUI
    ##########################################################
    def onSplitEnd(self,event=None):
        event = self.misconstrueEvent(event)
        exitCode = self.state.onSplit(event)
        if exitCode == 1:
            return
        elif exitCode and exitCode > 6:
            self.togglePause()
        if exitCode and self.menu:
            if exitCode%3 == 1:
                self.menu.updateMenuState("after")
            elif exitCode%3 == 2:
                self.menu.updateMenuState("last")
        self.updateWidgets("split")

    ##########################################################
    ## Move the comparison counter-clockwise (backwards)
    ##########################################################
    def guiSwitchCompareCCW(self,_=None):
        self.rotateCompare(-1)

    ##########################################################
    ## Move the comparison clockwise (forwards)
    ##########################################################
    def guiSwitchCompareCW(self,_=None):
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
    def reset(self, _=None):
        if not self.state.onReset():
            self.updateWidgets("reset")
            if self.menu:
                self.menu.updateMenuState("after")

    ##########################################################
    ## Skip a split
    ##########################################################
    def skip(self,event=None):
        event = self.misconstrueEvent(event)
        if not self.state.onSplitSkipped(event):
            self.updateWidgets("skip")

    ##########################################################
    ## If paused, unpause. If not paused, pause.
    ##########################################################
    def togglePause(self,event=None):
        event = self.misconstrueEvent(event)
        if not self.state.onPaused(event["system"]):
            self.updateWidgets("pause")
            if self.menu:
                if self.menu.state == "paused":
                    self.menu.updateMenuState(self.beforePauseState)
                else:
                    self.beforePauseState = self.menu.state
                    self.menu.updateMenuState("paused")

    ##########################################################
    ## Restart the run by resetting the timer state.
    ##########################################################
    def restart(self,_=None):
        if not self.state.onRestart():
            self.updateWidgets("restart")
            if self.menu:
                self.menu.updateMenuState("before")

    ##########################################################
    ## Saves the data stored in the state.
    ##########################################################
    def save(self,_=None):
        self.state.saveTimes()

    ##########################################################
    ## Saves the data stored in the state partway through a
    ## run.
    ##########################################################
    def partialSave(self,_=None):
        self.state.partialSave()

    ##########################################################
    ## Loads previously saved partial run data.
    ##########################################################
    def partialLoad(self,_=None):
        partialState = self.state.partialLoad()

        # Start so we can split
        self.start()
        # Do all the splits
        for i in range(len(partialState["splits"]["segments"])):
            if (timeh.isBlank(partialState["splits"]["totals"][i])):
                # skipped
                self.skip({"total": ""})
            else:
                # not skipped
                self.onSplitEnd({"segment": partialState["splits"]["segments"][i], "total": partialState["splits"]["totals"][i]})

        # Pause the timer
        self.togglePause({})
        # Update the total and segment timers so they are accurate
        self.state.starttime = self.state.pauseTime - partialState["times"]["total"]
        self.state.splitstarttime = self.state.pauseTime - partialState["times"]["segment"]

    ##########################################################
    ## Opens a window to change the current layout
    ##########################################################
    def chooseLayout(self,_=None):
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
    def chooseRun(self,_=None):
        if self.state.started:
            return
        RunPopup.RunPopup(self.root,self.setRun,self.session).show()

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

    ##########################################################
    ## Opens a window to change the current split (practice
    ## only)
    ##########################################################
    def chooseSplit(self,_=None):
        if self.state.started:
            return
        PracticeRunSelector.SelectorP(self.root,self.setSplit,self.session).show()

    def setSplit(self,newSession):
        if newSession["game"] == self.state.game\
            and newSession["category"] == self.state.category:
            return
        if self.state.unSaved:
            self.confirmSave(self.saveIfDesired)
        self.session.setRun(newSession["game"],newSession["category"],newSession["split"])
        self.state = PracticeState.State(self.session)
        self.updateWidgets("runChanged",state=self.state)

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
    def finish(self,_=None):
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

    def newEditedState(self,_):
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
