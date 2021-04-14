import gui
import State

## Initialize the state. This picks the game and category
state = State.State()

app = gui.Gui(state)
app.setupGui()
app.startGui()
