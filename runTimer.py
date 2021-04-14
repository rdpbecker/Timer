import gui
import State
import tkinter as tk

## Initialize the state. This picks the game and category
state = State.State()

app = gui.Gui(state)
app.setupGui()

rootWindow = app.root
bottom = tk.Frame(rootWindow, bg="red")
app.addComponent(bottom)
app.startGui()
