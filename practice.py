import sys
from Apps import app
from States import PracticeState
from Widgets import PracticeButtons, PracticeTimer, PracticeSegment
from util import readConfig as rc
from DataClasses import AllSplitNames
from DataClasses import PracticeSession
from Dialogs import AddRun
from Dialogs import PracticeRunSelector

def setHotkeys(app,state):
    app.root.bind(state.config["hotkeys"]["split"], app.onSplitEnd)
    app.root.bind(state.config["hotkeys"]["start"], app.start)
    app.root.bind(state.config["hotkeys"]["restart"], app.restart)
    app.root.bind(state.config["hotkeys"]["finish"], app.finish)
    app.root.bind(state.config["hotkeys"]["save"], app.save)
    app.root.bind(state.config["hotkeys"]["chooseSplit"], app.chooseSplit)

splits = AllSplitNames.Splits()
if not len(splits.getGames()):
    AddRun.SplitEditorD().show()
    splits.update()
session = PracticeSession.Session(splits)
if session.exit:
    sys.exit()

state = PracticeState.State(session)
rc.validateHotkeys(state.config)

app = app.App(state,session)
app.setupGui(True)

setHotkeys(app,state)
rootWindow = app.root

app.addWidget(PracticeSegment.SegmentCompare(rootWindow,state))
app.addWidget(PracticeTimer.Timer(rootWindow,state))
app.addWidget(PracticeButtons.Buttons(rootWindow,state,app))

app.startGui()

session.save()
