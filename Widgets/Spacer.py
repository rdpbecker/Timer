import tkinter as tk
from Widgets import WidgetBase

class Spacer(WidgetBase.WidgetBase):
    def __init__(self,parent,state,config):
        WidgetBase.WidgetBase.__init__(self,parent,state,config)
        self.configure(\
            height=config["height"],\
            bg=config["colours"]["bg"]\
        )
