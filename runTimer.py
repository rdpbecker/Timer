import app as App
import ComponentLoader
import errors as Errors
from DataClasses import AllSplitNames
from DataClasses import Session
from Dialogs import RunSelector
from States import State
from util import fileio
from util import layoutHelper as lh
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
    app.root.bind(state.config["hotkeys"]["chooseLayout"], app.chooseLayout)
    app.root.bind(state.config["hotkeys"]["chooseRun"], app.chooseRun)

splits = AllSplitNames.Splits()
session = Session.Session(splits)

app = None
exitCode = None

while not app or exitCode:
    rootWindow = None

    state = State.State(session)
    rc.validateHotkeys(state.config)

    app = App.App(state,session)
    app.setupGui()

    setHotkeys(app,state)
    rootWindow = app.root

    loader = ComponentLoader.ComponentLoader(app,state,rootWindow)

    for component in session.layout:
        try:
            if "config" in component.keys():
                app.addComponent(loader.loadComponent(component["type"],component["config"]))
            else:
                app.addComponent(loader.loadComponent(component["type"]))
        except Errors.ComponentTypeError as e:
            print(e)

    exitCode = app.startGui()

session.save()
