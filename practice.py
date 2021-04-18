import app, practiceState
from Components import PracticeButtons, PracticeTimer, PracticeSegment

def setHotkeys(app,state):
    app.root.bind(state.config["hotkeys"]["split"], app.onSplitEnd)
    app.root.bind(state.config["hotkeys"]["start"], app.start)
    app.root.bind(state.config["hotkeys"]["restart"], app.restart)
    app.root.bind(state.config["hotkeys"]["finish"], app.finish)

state = practiceState.State()
app = app.App(state)
app.setupGui()

setHotkeys(app,state)
rootWindow = app.root

app.addComponent(PracticeSegment.SegmentCompare(rootWindow,state))
app.addComponent(PracticeTimer.Timer(rootWindow,state))
app.addComponent(PracticeButtons.Buttons(rootWindow,state,app))

app.startGui()
