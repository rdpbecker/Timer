import os
from Dialogs import RunSelector
from util import fileio
from util import layoutHelper as lh
from util import readConfig as rc

class Session:
    game = ""
    category = ""
    splitNames = []
    layoutName = ""
    layout = []

    # splits = []
    config = None
    saveFile = ""

    def __init__(self,splits):
        self.splits = splits
        self.config = rc.getUserConfig()
        self.saveFile = self.config["baseDir"] + "/.save"
        self.exit = False
        if os.path.exists(self.saveFile):
            self.loadSave()
        else:
            self.getSession()

    def loadSave(self):
        saved = fileio.readJson(self.saveFile)
        self.setRun(saved["game"],saved["category"])
        self.setLayout(saved["layoutName"])

    def save(self):
        fileio.writeJson(self.saveFile,{\
            "game": self.game,\
            "category": self.category,\
            "layoutName": self.layoutName\
        })

    def getSession(self):
        session = RunSelector.RunSelector(self.splits).show()
        if not session["exitCode"]:
            self.exit = True
        self.setRun(session["game"],session["category"])
        self.setLayout(session["layoutName"])

    def setRun(self,game,category):
        if not game or not category:
            return
        self.game = game
        self.category = category
        self.splitNames = self.splits.getSplitNames(self.game,self.category)

    def setLayout(self,layoutName):
        if not layoutName:
            return
        self.layoutName = layoutName
        self.layout = lh.resolveLayout(self.layoutName)
