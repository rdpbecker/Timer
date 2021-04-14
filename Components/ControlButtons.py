import tkinter as tk
from Components import Component

class Buttons(Component.Component):
    buttons = []
    rootWindow = None

    def __init__(self,parent,state,rootWindow):
        Component.Component.__init__(self,parent,state)
        self.rootWindow = rootWindow
        button1 = tk.Button(self, bg=state.config["buttons"]["colours"]["bg"], font=state.config["buttons"]["font"], text="Change Compare", fg=state.config["buttons"]["colours"]["text"],command=rootWindow.guiSwitchCompareCW)

        button2 = tk.Button(self, bg=state.config["buttons"]["colours"]["bg"], font=state.config["buttons"]["font"], text="Split", fg=state.config["buttons"]["colours"]["text"], command=rootWindow.onSplitEnd)

        button3 = tk.Button(self, bg=state.config["buttons"]["colours"]["bg"], font=state.config["buttons"]["font"], text="Reset", fg=state.config["buttons"]["colours"]["text"], command=rootWindow.reset)

        button4 = tk.Button(self, bg=state.config["buttons"]["colours"]["bg"], font=state.config["buttons"]["font"], text="Skip Split", fg=state.config["buttons"]["colours"]["text"], command=rootWindow.skip)

        button5 = tk.Button(self, bg=state.config["buttons"]["colours"]["bg"], font=state.config["buttons"]["font"], text="Start Run", fg=state.config["buttons"]["colours"]["text"], command=rootWindow.start)

        button6 = tk.Button(self, bg=state.config["buttons"]["colours"]["bg"], font=state.config["buttons"]["font"], text="Pause", fg=state.config["buttons"]["colours"]["text"], command=rootWindow.togglePause)

        button3.grid(row=0,column=0,columnspan=6,sticky='WE')
        button4.grid(row=0,column=6,columnspan=6,sticky='WE')
        button1.grid(row=1,column=0,columnspan=6,sticky='WE')
        button6.grid(row=1,column=6,columnspan=6,sticky='WE')
        button2.grid(row=2,column=0,columnspan=6,sticky='WE')
        button5.grid(row=2,column=6,columnspan=6,sticky='WE')
        self.buttons.extend([button1,button2,button3,button4,button5,button6])
