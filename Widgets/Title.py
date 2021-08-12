import tkinter as tk
from Widgets import WidgetBase

class Title(WidgetBase.WidgetBase):
    # game = None
    # category = None

    def __init__(self,parent,state,config):
        WidgetBase.WidgetBase.__init__(self,parent,state,config)
        bg = config["colours"]["bg"]
        font = config["font"]
        textColour = config["colours"]["text"]

        self.configure(bg=bg)
        self.game = tk.Label(self, bg=bg, font=font, fg=textColour)
        self.category = tk.Label(self, bg=bg, font=font, fg=textColour)

        self.game.grid(row=0,column=2,columnspan=4,sticky='W')
        self.category.grid(row=0,column=6,columnspan=4,sticky='E')

        self.resetUI()

    def resetUI(self):
        self.game.configure(text=self.state.game)
        self.category.configure(text=self.state.category)
