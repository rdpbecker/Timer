import gui
import State
from Components import CompareInfo, ControlButtons
import tkinter as tk

## Initialize the state. This picks the game and category
state = State.State()

app = gui.Gui(state)
app.setupGui()

rootWindow = app.root
app.addComponent(CompareInfo.CompareInfo(rootWindow,state))
app.addComponent(ControlButtons.Buttons(rootWindow,state,app))
app.startGui()
