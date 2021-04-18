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
app.addComponent(Spacer.Spacer(rootWindow,state))
app.addComponent(SegmentArea.SegmentArea(rootWindow,state))
app.addComponent(Spacer.Spacer(rootWindow,state))
app.addComponent(SegmentCompare.SegmentCompare(rootWindow,state))
app.addComponent(Spacer.Spacer(rootWindow,state))
app.addComponent(DetailedTimer.Timer(rootWindow,state))
app.addComponent(Spacer.Spacer(rootWindow,state))
if (state.config["infoShow"]["timeSave"]):
    app.addComponent(TimeSaveInfo.TimeSaveInfo(rootWindow,state))
if (state.config["infoShow"]["diff"]):
    app.addComponent(DiffInfo.DiffInfo(rootWindow,state))
if (state.config["infoShow"]["bpt"]):
    app.addComponent(BptInfo.BptInfo(rootWindow,state))
if (state.config["infoShow"]["sob"]):
    app.addComponent(SobInfo.SobInfo(rootWindow,state))
if (state.config["infoShow"]["pb"]):
    app.addComponent(PbInfo.PbInfo(rootWindow,state))
if (state.config["infoShow"]["comparison"]):
    app.addComponent(CompareInfo.CompareInfo(rootWindow,state))
if (state.config["infoShow"]["buttons"]):
    try:
        app.addComponent(loader.loadComponent("controlButtons"))
    except Errors.ComponentTypeError as e:
        print(e)

app.startGui()
