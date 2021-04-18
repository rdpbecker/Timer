import app
from States import PracticeState
from PracticeComponents import Buttons, Timer, Segment
from util import readConfig as rc

def setHotkeys(app,state):
    app.root.bind(state.config["hotkeys"]["split"], app.onSplitEnd)
    app.root.bind(state.config["hotkeys"]["start"], app.start)
    app.root.bind(state.config["hotkeys"]["restart"], app.restart)
    app.root.bind(state.config["hotkeys"]["finish"], app.finish)

state = PracticeState.State()
rc.validateHotkeys(state.config)

app = app.App(state)
app.setupGui()

setHotkeys(app,state)
rootWindow = app.root

app.addComponent(Segment.SegmentCompare(rootWindow,state))
app.addComponent(Timer.Timer(rootWindow,state))
app.addComponent(Buttons.Buttons(rootWindow,state,app))

app.startGui()
