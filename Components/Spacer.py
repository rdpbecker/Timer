import tkinter as tk
from Components import Component

class Spacer(Component.Component):
    def __init__(self,parent,state):
        Component.Component.__init__(self,parent,state)
        self.configure(\
            height=state.config["spacerHeight"],\
            bg=state.config["root"]["colours"]["bg"]\
        )
