import tkinter as tk
from Components import Component

class Info(Component.Component):
    header = None
    info = None

    def __init__(self,parent,state):
        Component.Component.__init__(self,parent,state)
        self.configure(bg=state.config["root"]["colours"]["bg"])
        self.header = tk.Label(self, fg=state.config["root"]["colours"]["text"], bg=state.config["root"]["colours"]["bg"])
        self.info = tk.Label(self, fg=state.config["root"]["colours"]["text"], bg=state.config["root"]["colours"]["bg"])
        self.header.grid(row=0,column=0,columnspan=7,sticky='W',ipadx=state.config["padx"])
        self.info.grid(row=0,column=7,columnspan=5,sticky='E',ipadx=state.config["padx"])
