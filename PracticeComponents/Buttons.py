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

        button1 = tk.Button(self, bg=bg, font=font, text="Split", fg=fg,command=rootWindow.guiSwitchCompareCW)
        button2 = tk.Button(self, bg=bg, font=font, text="Restart", fg=fg, command=rootWindow.onSplitEnd)
        button3 = tk.Button(self, bg=bg, font=font, text="Start", fg=fg, command=rootWindow.reset)
        button4 = tk.Button(self, bg=bg, font=font, text="Finish", fg=fg, command=rootWindow.skip)

        button1.grid(row=0,column=0,columnspan=6,sticky='WE')
        button2.grid(row=0,column=6,columnspan=6,sticky='WE')
        button3.grid(row=1,column=0,columnspan=6,sticky='WE')
        button4.grid(row=1,column=6,columnspan=6,sticky='WE')
        self.buttons.extend([button1,button2,button3,button4])
