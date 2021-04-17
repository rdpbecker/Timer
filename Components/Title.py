import tkinter as tk
from Components import Component
import timeHelpers as timeh

class Title(Component.Component):
    game = None
    category = None

    def __init__(self,parent,state):
        Component.Component.__init__(self,parent,state)
        bg = state.config["root"]["colours"]["bg"]
        font = state.config["root"]["font"]
        textColour = state.config["root"]["colours"]["text"]

        self.configure(bg=bg)
        self.game = tk.Label(self, bg=bg, font=font, fg=textColour)
        self.category = tk.Label(self, bg=bg, font=font, fg=textColour)

        self.game.configure(text=self.state.game)
        self.category.configure(text=self.state.category)

        self.game.grid(row=0,column=3,columnspan=3,sticky='W')
        self.category.grid(row=0,column=6,columnspan=3,sticky='E')
