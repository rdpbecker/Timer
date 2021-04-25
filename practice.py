import app
from States import PracticeState
from PracticeComponents import Buttons, Timer, Segment
from util import readConfig as rc
from DataClasses import AllSplitNames
from Dialogs import PracticeRunSelector

def setHotkeys(app,state):
    app.root.bind(state.config["hotkeys"]["split"], app.onSplitEnd)
    app.root.bind(state.config["hotkeys"]["start"], app.start)
    app.root.bind(state.config["hotkeys"]["restart"], app.restart)
    app.root.bind(state.config["hotkeys"]["finish"], app.finish)
    app.root.bind(state.config["hotkeys"]["save"], app.save)

splits = AllSplitNames.Splits()
session = PracticeRunSelector.RunSelector(splits).show()

state = PracticeState.State(session)
rc.validateHotkeys(state.config)

app = app.App(state)
app.setupGui()

setHotkeys(app,state)
rootWindow = app.root

app.addComponent(Segment.SegmentCompare(rootWindow,state))
app.addComponent(Timer.Timer(rootWindow,state))
app.addComponent(Buttons.Buttons(rootWindow,state,app))

app.startGui()
