import tkinter as tk
from Components import Component

class Buttons(Component.Component):
    buttons = []
    rootWindow = None

    def __init__(self,parent,state,config,rootWindow):
        Component.Component.__init__(self,parent,state,config)
        self.rootWindow = rootWindow
        bg = config["colours"]["bg"]
        fg = config["colours"]["text"]
        font = config["font"]

        button1 = tk.Button(self, bg=bg, font=font, text="Change Compare", fg=fg,command=rootWindow.guiSwitchCompareCW)
        button2 = tk.Button(self, bg=bg, font=font, text="Split", fg=fg, command=rootWindow.onSplitEnd)
        button3 = tk.Button(self, bg=bg, font=font, text="Reset", fg=fg, command=rootWindow.reset)
        button4 = tk.Button(self, bg=bg, font=font, text="Skip Split", fg=fg, command=rootWindow.skip)
        button5 = tk.Button(self, bg=bg, font=font, text="Start Run", fg=fg, command=rootWindow.start)
        button6 = tk.Button(self, bg=bg, font=font, text="Pause", fg=fg, command=rootWindow.togglePause)
        button7 = tk.Button(self, bg=bg, font=font, text="Restart", fg=fg, command=rootWindow.restart)
        button8 = tk.Button(self, bg=bg, font=font, text="Finish", fg=fg, command=rootWindow.finish)
        button9 = tk.Button(self, bg=bg, font=font, text="Save", fg=fg, command=rootWindow.save)
        button10 = tk.Button(self, bg=bg, font=font, text="Choose Layout", fg=fg, command=rootWindow.chooseLayout)
        button11 = tk.Button(self, bg=bg, font=font, text="Choose Run", fg=fg, command=rootWindow.chooseRun)

        button10.grid(row=0,column=0,columnspan=6,sticky='WE')
        button11.grid(row=0,column=6,columnspan=6,sticky='WE')
        button3.grid(row=1,column=0,columnspan=6,sticky='WE')
        button7.grid(row=1,column=6,columnspan=6,sticky='WE')
        button1.grid(row=2,column=0,columnspan=6,sticky='WE')
        button6.grid(row=2,column=6,columnspan=6,sticky='WE')
        button4.grid(row=3,column=0,columnspan=6,sticky='WE')
        button5.grid(row=3,column=6,columnspan=6,sticky='WE')
        button8.grid(row=4,column=0,columnspan=6,sticky='WE')
        button9.grid(row=4,column=6,columnspan=6,sticky='WE')
        button2.grid(row=5,column=0,columnspan=12,sticky='WE')
        self.buttons.extend([button1,button2,button3,button4,button5,button6,button7,button8,button9,button10,button11])
