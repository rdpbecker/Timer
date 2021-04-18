import app
from States import State
from Components import Title, DetailedTitle, Spacer, SegmentArea, SegmentCompare, Timer, DetailedTimer, CompareInfo, PbInfo, SobInfo, BptInfo, DiffInfo, TimeSaveInfo, ControlButtons
from util import readConfig as rc
import ComponentLoader
import errors as Errors

def setHotkeys(app,state):
    app.root.bind(state.config["hotkeys"]["decreaseComparison"],app.guiSwitchCompareCCW)
    app.root.bind(state.config["hotkeys"]["increaseComparison"],app.guiSwitchCompareCW)
    app.root.bind(state.config["hotkeys"]["split"], app.onSplitEnd)
    app.root.bind(state.config["hotkeys"]["reset"], app.reset)
    app.root.bind(state.config["hotkeys"]["skip"], app.skip)
    app.root.bind(state.config["hotkeys"]["start"], app.start)
    app.root.bind(state.config["hotkeys"]["pause"], app.togglePause)

## Initialize the state. This picks the game and category
state = State.State()
rc.validateHotkeys(state.config)

app = app.App(state)
app.setupGui()

setHotkeys(app,state)
rootWindow = app.root

loader = ComponentLoader.ComponentLoader(app,state,rootWindow)

app.addComponent(Title.Title(rootWindow,state))
try:
    app.addComponent(loader.loadComponent("spacer"))
except Errors.ComponentTypeError as e:
    print(e)
app.addComponent(SegmentArea.SegmentArea(rootWindow,state))
try:
    app.addComponent(loader.loadComponent("spacer"))
except Errors.ComponentTypeError as e:
    print(e)
app.addComponent(SegmentCompare.SegmentCompare(rootWindow,state))
try:
    app.addComponent(loader.loadComponent("spacer"))
except Errors.ComponentTypeError as e:
    print(e)
app.addComponent(DetailedTimer.Timer(rootWindow,state))
try:
    app.addComponent(loader.loadComponent("spacer"))
except Errors.ComponentTypeError as e:
    print(e)
if (state.config["infoShow"]["timeSave"]):
    try:
        app.addComponent(loader.loadComponent("timeSaveInfo"))
    except Errors.ComponentTypeError as e:
        print(e)
if (state.config["infoShow"]["diff"]):
    try:
        app.addComponent(loader.loadComponent("diffInfo"))
    except Errors.ComponentTypeError as e:
        print(e)
if (state.config["infoShow"]["bpt"]):
    try:
        app.addComponent(loader.loadComponent("bptInfo"))
    except Errors.ComponentTypeError as e:
        print(e)
if (state.config["infoShow"]["sob"]):
    try:
        app.addComponent(loader.loadComponent("sobInfo"))
    except Errors.ComponentTypeError as e:
        print(e)
if (state.config["infoShow"]["pb"]):
    try:
        app.addComponent(loader.loadComponent("pbInfo"))
    except Errors.ComponentTypeError as e:
        print(e)
if (state.config["infoShow"]["comparison"]):
    try:
        app.addComponent(loader.loadComponent("compareInfo"))
    except Errors.ComponentTypeError as e:
        print(e)
if (state.config["infoShow"]["buttons"]):
    try:
        app.addComponent(loader.loadComponent("controlButtons"))
    except Errors.ComponentTypeError as e:
        print(e)

app.startGui()
