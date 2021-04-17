import tkinter as tk
from Components import Component

class Buttons(Component.Component):
    buttons = []
    rootWindow = None

    def __init__(self,parent,state,rootWindow):
        Component.Component.__init__(self,parent,state)
        self.rootWindow = rootWindow
        bg = state.config["buttons"]["colours"]["bg"]
        fg = state.config["buttons"]["colours"]["text"]
        font = state.config["buttons"]["font"]

        button1 = tk.Button(self, bg=bg, font=font, text="Change Compare", fg=fg,command=rootWindow.guiSwitchCompareCW)
        button2 = tk.Button(self, bg=bg, font=font, text="Split", fg=fg, command=rootWindow.onSplitEnd)
        button3 = tk.Button(self, bg=bg, font=font, text="Reset", fg=fg, command=rootWindow.reset)
        button4 = tk.Button(self, bg=bg, font=font, text="Skip Split", fg=fg, command=rootWindow.skip)
        button5 = tk.Button(self, bg=bg, font=font, text="Start Run", fg=fg, command=rootWindow.start)
        button6 = tk.Button(self, bg=bg, font=font, text="Pause", fg=fg, command=rootWindow.togglePause)

        button3.grid(row=0,column=0,columnspan=6,sticky='WE')
        button4.grid(row=0,column=6,columnspan=6,sticky='WE')
        button1.grid(row=1,column=0,columnspan=6,sticky='WE')
        button6.grid(row=1,column=6,columnspan=6,sticky='WE')
        button2.grid(row=2,column=0,columnspan=6,sticky='WE')
        button5.grid(row=2,column=6,columnspan=6,sticky='WE')
        self.buttons.extend([button1,button2,button3,button4,button5,button6])
