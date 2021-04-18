import tkinter as tk
from Components import Component

class Spacer(Component.Component):
    def __init__(self,parent,state,config):
        Component.Component.__init__(self,parent,state,config)
        self.configure(\
            height=config["height"],\
            bg=config["colours"]["bg"]\
        )
