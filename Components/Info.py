import tkinter as tk
from Components import Component

class Info(Component.Component):
    header = None
    info = None

    def __init__(self,parent,state):
        Component.Component.__init__(self,parent,state)
        self.configure(bg=state.config["root"]["colours"]["bg"])
        self.state = state
        self.header = tk.Label(self, text="Comparing Against:", fg=state.config["root"]["colours"]["text"], bg=state.config["root"]["colours"]["bg"])
        self.info = tk.Label(self, text=state.currentComparison.totalHeader, fg=state.config["root"]["colours"]["text"], bg=state.config["root"]["colours"]["bg"])
        self.header.grid(row=0,column=0,columnspan=8,sticky='W',ipadx=state.config["padx"])
        self.info.grid(row=0,column=8,columnspan=4,sticky='E',ipadx=state.config["padx"])
