import os
from Dialogs import PracticeRunSelector
from util import fileio
from util import layoutHelper as lh
from util import readConfig as rc

class Session:
    game = ""
    category = ""
    split = ""
    layoutName = ""
    layout = []

    splits = []
    config = None
    saveFile = ""

    def __init__(self,splits):
        self.splits = splits
        self.config = rc.getUserConfig()
        self.saveFile = self.config["baseDir"] + "/.practiceSave"
        self.exit = False
        if os.path.exists(self.saveFile):
            self.loadSave()
        else:
            self.getSession()

    def loadSave(self):
        saved = fileio.readJson(self.saveFile)
        self.setRun(saved["game"],saved["category"],saved["split"])

    def save(self):
        fileio.writeJson(self.saveFile,{\
            "game": self.game,\
            "category": self.category,\
            "split": self.split,\
        })

    def getSession(self):
        session = PracticeRunSelector.RunSelector().show()
        if not session["exitType"]:
            self.exit = True
            return
        self.setRun(session["game"],session["category"],session["split"])

    def setRun(self,game,category,split):
        if not game or not category or not split:
            return
        self.game = game
        self.category = category
        self.split = split
        self.splitNames = self.splits.getSplitNames(self.game,self.category)
