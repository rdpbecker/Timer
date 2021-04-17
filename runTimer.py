import app
import State
from Components import Title, DetailedTitle, Spacer, SegmentArea, SegmentCompare, DetailedTimer, CompareInfo, PbInfo, SobInfo, BptInfo, DiffInfo, TimeSaveInfo, ControlButtons
import tkinter as tk

## Initialize the state. This picks the game and category
state = State.State()

app = app.App(state)
app.setupGui()

rootWindow = app.root

app.addComponent(Title.Title(rootWindow,state))
app.addComponent(Spacer.Spacer(rootWindow,state))
app.addComponent(SegmentArea.SegmentArea(rootWindow,state))
app.addComponent(Spacer.Spacer(rootWindow,state))
app.addComponent(SegmentCompare.SegmentCompare(rootWindow,state))
app.addComponent(DetailedTimer.DetailedTimer(rootWindow,state))
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
    app.addComponent(ControlButtons.Buttons(rootWindow,state,app))

app.startGui()
