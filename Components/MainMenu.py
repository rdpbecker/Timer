import tkinter as tk

class Menu(tk.Menu):
    def __init__(self,app):
        super().__init__(app.root)
        self.menubar = tk.Menu(app.root, tearoff=False)
        self["tearoff"] = False

        self.add_cascade(label="Control", menu=self.menubar)

        self.entries = [\
            {\
                "name": "Choose Layout", \
                "command": app.chooseLayout, \
                "before": "normal", \
                "during": "disabled", \
                "last": "disabled", \
                "after": "disabled"\
            },\
            {\
                "name": "Choose Run", \
                "command": app.chooseRun, \
                "before": "normal", \
                "during": "disabled", \
                "last": "disabled", \
                "after": "disabled"\
            },\
            {\
                "name": "Start", \
                "command": app.start, \
                "before": "normal", \
                "during": "disabled", \
                "last": "disabled", \
                "after": "disabled"\
            },\
            {\
                "name": "Split", \
                "command": app.onSplitEnd, \
                "before": "disabled", \
                "during": "normal", \
                "last": "normal", \
                "after": "disabled"\
            },\
            {\
                "name": "Skip Split", \
                "command": app.skip, \
                "before": "disabled", \
                "during": "normal", \
                "last": "disabled", \
                "after": "disabled"\
            },\
            {\
                "name": "Reset", \
                "command": app.reset, \
                "before": "disabled", \
                "during": "normal", \
                "last": "normal", \
                "after": "disabled"\
            },\
            {\
                "name": "Restart", \
                "command": app.restart, \
                "before": "disabled", \
                "during": "disabled", \
                "last": "disabled", \
                "after": "normal"\
            },\
            {\
                "name": "Change Compare", \
                "command": app.guiSwitchCompareCW, \
                "before": "normal", \
                "during": "normal", \
                "last": "normal", \
                "after": "normal"\
            },\
            {\
                "name": "Pause", \
                "command": app.togglePause, \
                "before": "disabled", \
                "during": "normal", \
                "last": "normal", \
                "after": "disabled"\
            },\
            {\
                "name": "Save", \
                "command": app.save, \
                "before": "normal", \
                "during": "disabled", \
                "last": "disabled", \
                "after": "normal"\
            },\
            {\
                "name": "Finish", \
                "command": app.finish, \
                "before": "normal", \
                "during": "disabled", \
                "last": "disabled", \
                "after": "normal"\
            },\
            {\
                "name": "Edit Splits", \
                "command": app.editSplits, \
                "before": "active", \
                "during": "disabled", \
                "last": "disabled", \
                "after": "disabled"\
            },\
            {\
                "name": "Add New Run", \
                "command": app.addRun, \
                "before": "active", \
                "during": "disabled", \
                "last": "disabled", \
                "after": "disabled"\
            }\
        ]

        for item in self.entries:
            self.menubar.add_command(label=item["name"], command=item["command"])
        self.updateMenuState("before")

    def updateMenuState(self,state):
        for item in self.entries:
            self.menubar.entryconfig(item["name"],state=item[state])

class PracticeMenu(tk.Menu):
    def __init__(self,app):
        super().__init__(app.root)
        self.menubar = tk.Menu(app.root, tearoff=False)
        self["tearoff"] = False
        self.add_cascade(label="Control", menu=self.menubar)

        self.entries = [\
            {\
                "name": "Choose Split", \
                "command": app.chooseSplit, \
                "before": "normal", \
                "during": "disabled", \
                "after": "disabled"\
            },\
            {\
                "name": "Start", \
                "command": app.start, \
                "before": "normal", \
                "during": "disabled", \
                "after": "disabled"\
            },\
            {\
                "name": "Split", \
                "command": app.onSplitEnd, \
                "before": "disabled", \
                "during": "normal", \
                "after": "disabled"\
            },\
            {\
                "name": "Restart", \
                "command": app.restart, \
                "before": "disabled", \
                "during": "disabled", \
                "after": "normal"\
            },\
            {\
                "name": "Save", \
                "command": app.save, \
                "before": "normal", \
                "during": "disabled", \
                "after": "normal"\
            },\
            {\
                "name": "Finish", \
                "command": app.finish, \
                "before": "normal", \
                "during": "disabled", \
                "after": "normal"\
            }\
        ]

        for item in self.entries:
            self.menubar.add_command(label=item["name"], command=item["command"])
        self.updateMenuState("before")

    def updateMenuState(self,state):
        for item in self.entries:
            self.menubar.entryconfig(item["name"],state=item[state])
