import sys
from Apps import app as App
import WidgetLoader
import errors as Errors
from DataClasses import AllSplitNames
from DataClasses import Session
from Dialogs import AddRun
from States import State
from util import readConfig as rc

def setHotkeys(app,state):
    app.root.bind(state.config["hotkeys"]["decreaseComparison"],app.guiSwitchCompareCCW)
    app.root.bind(state.config["hotkeys"]["increaseComparison"],app.guiSwitchCompareCW)
    app.root.bind(state.config["hotkeys"]["split"], app.onSplitEnd)
    app.root.bind(state.config["hotkeys"]["reset"], app.reset)
    app.root.bind(state.config["hotkeys"]["skip"], app.skip)
    app.root.bind(state.config["hotkeys"]["start"], app.start)
    app.root.bind(state.config["hotkeys"]["pause"], app.togglePause)
    app.root.bind(state.config["hotkeys"]["restart"], app.restart)
    app.root.bind(state.config["hotkeys"]["finish"], app.finish)
    app.root.bind(state.config["hotkeys"]["save"], app.save),
    app.root.bind(state.config["hotkeys"]["partialSave"], app.partialSave),
    app.root.bind("<Control-L>", app.partialLoad),
    app.root.bind(state.config["hotkeys"]["chooseLayout"], app.chooseLayout)
    app.root.bind(state.config["hotkeys"]["chooseRun"], app.chooseRun)

splits = AllSplitNames.Splits()
if not len(splits.getGames()):
    AddRun.SplitEditorD().show()
    splits.update()
session = Session.Session(splits)
if session.exit:
    sys.exit()

app = None
exitCode = None

while not app or exitCode:
    rootWindow = None

    state = State.State(session)
    rc.validateHotkeys(state.config)

    app = App.App(state,session)
    app.setupGui(showMenu=session.layout["menu"])

    setHotkeys(app,state)
    rootWindow = app.root

    loader = WidgetLoader.WidgetLoader(app,state,rootWindow)

    for component in session.layout["components"]:
        try:
            if "config" in component.keys():
                app.addWidget(loader.loadWidget(component["type"],component["config"]))
            else:
                app.addWidget(loader.loadWidget(component["type"]))
        except Errors.WidgetTypeError as e:
            print(e)

    exitCode = app.startGui()

session.save()
