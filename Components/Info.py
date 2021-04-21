import tkinter as tk
from Components import Component

class Info(Component.Component):
    header = None
    info = None

    def __init__(self,parent,state,config):
        Component.Component.__init__(self,parent,state,config)
        self.configure(bg=config["colours"]["bg"],padx=state.config["padx"])
        self.header = tk.Label(self, fg=config["colours"]["text"], bg=config["colours"]["bg"])
        self.info = tk.Label(self, fg=config["colours"]["text"], bg=config["colours"]["bg"])
        self.header.pack(side="left",anchor="w")
        self.info.pack(side="right",anchor="e")
