import app
from States import State
from util import readConfig as rc
import ComponentLoader
import errors as Errors
from util import fileio

def setHotkeys(app,state):
    app.root.bind(state.config["hotkeys"]["decreaseComparison"],app.guiSwitchCompareCCW)
    app.root.bind(state.config["hotkeys"]["increaseComparison"],app.guiSwitchCompareCW)
    app.root.bind(state.config["hotkeys"]["split"], app.onSplitEnd)
    app.root.bind(state.config["hotkeys"]["reset"], app.reset)
    app.root.bind(state.config["hotkeys"]["skip"], app.skip)
    app.root.bind(state.config["hotkeys"]["start"], app.start)
    app.root.bind(state.config["hotkeys"]["pause"], app.togglePause)
    app.root.bind(state.config["hotkeys"]["restart"], app.restart)

## Initialize the state. This picks the game and category
state = State.State()
rc.validateHotkeys(state.config)

app = app.App(state)
app.setupGui()

setHotkeys(app,state)
rootWindow = app.root

loader = ComponentLoader.ComponentLoader(app,state,rootWindow)
layout = fileio.getLayout()

for component in layout:
    try:
        if "config" in component.keys():
            app.addComponent(loader.loadComponent(component["type"],component["config"]))
        else:
            app.addComponent(loader.loadComponent(component["type"]))
    except Errors.ComponentTypeError as e:
        print(e)

app.startGui()
