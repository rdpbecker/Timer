import tkinter as tk
from Components import Component
from util import timeHelpers as timeh

class Title(Component.Component):
    game = None
    category = None
    compHeader = None
    compName = None

    def __init__(self,parent,state,config):
        Component.Component.__init__(self,parent,state,config)
        bg = config["colours"]["bg"]
        font = config["font"]
        textColour = config["colours"]["text"]

        self.configure(bg=bg)
        self.game = tk.Label(self, bg=bg, font=font, fg=textColour)
        self.category = tk.Label(self, bg=bg, font=font, fg=textColour)
        self.compHeader = tk.Label(self, bg=bg, font=font, fg=textColour)
        self.compName = tk.Label(self, bg=bg, font=font, fg=textColour)

        self.game.configure(text=self.state.game)
        self.category.configure(text=self.state.category)
        self.compHeader.configure(text="Comparing Against")
        self.compName.configure(text=self.state.currentComparison.totalHeader)

        self.game.grid(row=0,column=0,columnspan=2,sticky='W',ipadx=10)
        self.category.grid(row=0,column=2,columnspan=3,sticky='W')
        self.compHeader.grid(row=0,column=5,columnspan=4,sticky='E')
        self.compName.grid(row=0,column=9,columnspan=3,sticky='E',ipadx=10)

    def onComparisonChanged(self):
        self.compName.configure(text=self.state.currentComparison.totalHeader)
