import gui
import State
from Components import CompareInfo, PbInfo, SobInfo, BptInfo, ControlButtons
import tkinter as tk

## Initialize the state. This picks the game and category
state = State.State()

app = gui.Gui(state)
app.setupGui()

rootWindow = app.root
if (state.config["infoShow"]["bpt"]):
    app.addComponent(BptInfo.BptInfo(rootWindow,state))
if (state.config["infoShow"]["sob"]):
    app.addComponent(SobInfo.SobInfo(rootWindow,state))
if (state.config["infoShow"]["pb"]):
    app.addComponent(PbInfo.PbInfo(rootWindow,state))
if (state.config["infoShow"]["comparison"]):
    app.addComponent(CompareInfo.CompareInfo(rootWindow,state))
if (state.config["infoShow"]["buttons"]):
    app.addComponent(ControlButtons.Buttons(rootWindow,state,app))
app.startGui()
