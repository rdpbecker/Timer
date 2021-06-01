from Apps import app
from States import PracticeState
from PracticeWidgets import Buttons, Timer, Segment
from util import readConfig as rc
from DataClasses import AllSplitNames
from DataClasses import PracticeSession
from Dialogs import PracticeRunSelector

def setHotkeys(app,state):
    app.root.bind(state.config["hotkeys"]["split"], app.onSplitEnd)
    app.root.bind(state.config["hotkeys"]["start"], app.start)
    app.root.bind(state.config["hotkeys"]["restart"], app.restart)
    app.root.bind(state.config["hotkeys"]["finish"], app.finish)
    app.root.bind(state.config["hotkeys"]["save"], app.save)

splits = AllSplitNames.Splits()
session = PracticeSession.Session(splits)

state = PracticeState.State(session)
rc.validateHotkeys(state.config)

app = app.App(state,session)
app.setupGui()

setHotkeys(app,state)
rootWindow = app.root

app.addWidget(Segment.SegmentCompare(rootWindow,state))
app.addWidget(Timer.Timer(rootWindow,state))
app.addWidget(Buttons.Buttons(rootWindow,state,app))

app.startGui()

session.save()
