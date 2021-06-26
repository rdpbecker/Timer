import tkinter as tk
from DataClasses import AllSplitNames
from Components.SplitEditor import EntryGrid
from Components.SplitEditor import MainEditor
from Components import GameSelector
from util import fileio
from util import dataManip
from util import readConfig as rc

class SplitEditor(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.config = rc.getUserConfig()
        self.splits = AllSplitNames.Splits()

        self.selection = GameSelector.Selector(self)
        self.selection.pack(side="top",fill="x")
        self.selection.followup = self.updateRows
        self.oldGame = ""
        self.oldCategory = ""

        self.editor = MainEditor.Editor(self,dataManip.newComparisons())
        self.editor.pack(side="bottom")
        self.editor.saveButton.options["save"] = self.save
        self.editor.saveButton.options["valid"] = self.validSave

        self.savedGame = ""
        self.savedCategory = ""

    def updateRows(self,*args):
        self.editor.entries.pack_forget()
        if not self.splits.validPair(self.selection.game,self.selection.category):
            if not self.splits.validPair(self.oldGame,self.oldCategory):
                self.editor.entries.pack(side="left")
                return
            self.editor.entries = EntryGrid.EntryGrid(self.editor,dataManip.newComparisons(),self.editor)
        else:
            self.editor.entries = EntryGrid.EntryGrid(self.editor,fileio.csvReadStart(self.config["baseDir"],self.selection.game,self.selection.category,self.splits.getSplitNames(self.selection.game,self.selection.category))[1],self.editor)
        self.editor.entries.pack(side="left")
        self.oldGame = self.selection.game
        self.oldCategory = self.selection.category

    def hasSaved(self,game,category):
        return game == self.savedGame and category == self.savedCategory

    def validSave(self):
        self.editor.saveWarning.pack_forget()
        check1 = self.selection.game and self.selection.category
        check2 = self.editor.entries.leftFrame.isValid()
        check3 = len(self.editor.entries.rows) > 0
        if not check1:
            self.editor.saveButton.options["invalidMsg"] = "Runs must have a\nnon-empty game and\ncategory."
        elif not check2:
            self.editor.saveButton.options["invalidMsg"] = "All split names\nmust be non-empty."
        elif not check3:
            self.editor.saveButton.options["invalidMsg"] = "This run has no splits."
        elif self.editor.entries.shouldWarn():
            self.editor.saveWarning.pack(side="bottom",fill="both")

        return check1 and check2 and check3

    def save(self,retVal):
        if not retVal:
            return
        game = self.selection.game
        category = self.selection.category
        while self.splits.validPair(game,category) and not self.hasSaved(game,category):
            category = category + "Copy"
        if self.splits.validPair(self.savedGame,self.savedCategory):
            self.splits.removePair(self.savedGame,self.savedCategory)
            fileio.removeCategory(self.config["baseDir"],self.savedGame,self.savedCategory)
        csvs = self.editor.entries.generateGrid()
        csvs["complete"] = dataManip.newCompleteCsv(csvs["names"])
        fileio.writeCSVs(self.config["baseDir"],game,category,csvs["complete"],csvs["comparisons"])
        self.splits.updateNames(game,category,csvs["names"])
        self.savedGame = game
        self.savedCategory = category
