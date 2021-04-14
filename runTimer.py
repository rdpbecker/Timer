import gui
import State
from Components import CompareName, ControlButtons
import tkinter as tk

## Initialize the state. This picks the game and category
state = State.State()

app = gui.Gui(state)
app.setupGui()

rootWindow = app.root
app.addComponent(CompareName.CompareName(rootWindow,state))
app.addComponent(ControlButtons.Buttons(rootWindow,state,app))
app.startGui()
