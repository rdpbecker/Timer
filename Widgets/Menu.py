import tkinter as tk

class ControlMenu(tk.Menu):
    def __init__(self,app):
        tk.Menu.__init__(self,app.root)
        menubar = tk.Menu(app.root, tearoff=False)
        self["tearoff"] = False

        self.add_cascade(label="Control", menu=menubar)

        menubar.add_command(label="Choose Layout", command=app.chooseLayout)
        menubar.add_command(label="Choose Run", command=app.chooseRun)
        menubar.add_command(label="Start", command=app.start)
        menubar.add_command(label="Split", command=app.onSplitEnd)
        menubar.add_command(label="Skip Split", command=app.skip)
        menubar.add_command(label="Reset", command=app.reset)
        menubar.add_command(label="Restart", command=app.restart)
        menubar.add_command(label="Change Compare", command=app.guiSwitchCompareCW)
        menubar.add_command(label="Pause", command=app.togglePause)
        menubar.add_command(label="Save", command=app.save)
        menubar.add_command(label="Finish", command=app.finish)
