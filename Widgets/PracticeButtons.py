import tkinter as tk
from Widgets import WidgetBase
from util import fileio

class Buttons(WidgetBase.WidgetBase):
    buttons = []
    rootWindow = None

    def __init__(self,parent,state,rootWindow):
        config = fileio.readJson("defaults/controlButtons.json")
        super().__init__(parent,state,config)
        self.rootWindow = rootWindow
        bg = config["colours"]["bg"]
        fg = config["colours"]["text"]
        font = config["font"]

        button1 = tk.Button(self, bg=bg, font=font, text="Split", fg=fg,command=rootWindow.onSplitEnd)
        button2 = tk.Button(self, bg=bg, font=font, text="Restart", fg=fg, command=rootWindow.restart)
        button3 = tk.Button(self, bg=bg, font=font, text="Start", fg=fg, command=rootWindow.start)
        button4 = tk.Button(self, bg=bg, font=font, text="Finish", fg=fg, command=rootWindow.finish)

        button1.grid(row=0,column=0,columnspan=6,sticky='WE')
        button2.grid(row=0,column=6,columnspan=6,sticky='WE')
        button3.grid(row=1,column=0,columnspan=6,sticky='WE')
        button4.grid(row=1,column=6,columnspan=6,sticky='WE')
        self.buttons.extend([button1,button2,button3,button4])
