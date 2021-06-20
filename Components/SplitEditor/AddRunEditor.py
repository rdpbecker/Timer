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
        self.editor.saveButton.options["callback"] = self.save
        self.editor.saveButton.options["valid"] = self.validSave

    def updateRows(self,*args):
        self.editor.entries.pack_forget()
        if not self.splits.validPair(self.selection.game,self.selection.category):
            if not self.splits.validPair(self.oldGame,self.oldCategory):
                self.editor.entries.pack(side="left")
                return
            self.editor.entries = EntryGrid.EntryGrid(self.editor,dataManip.newComparisons())
        else:
            self.editor.entries = EntryGrid.EntryGrid(self.editor,fileio.csvReadStart(self.config["baseDir"],self.selection.game,self.selection.category,self.splits.getSplitNames(self.selection.game,self.selection.category))[1])
        self.editor.entries.pack(side="left")
        self.oldGame = self.selection.game
        self.oldCategory = self.selection.category

    def validSave(self):
        self.editor.saveWarning.pack_forget()
        if not (self.selection.game and self.selection.category):
            self.editor.saveButton.options["invalidMsg"] = "Runs must have a\nnon-empty game and\ncategory."
        elif not self.editor.entries.leftFrame.isValid():
            self.editor.saveButton.options["invalidMsg"] = "All split names\nmust be non-empty."
        elif self.editor.deleteSplitButton["state"] == "disabled":
            self.editor.saveButton.options["invalidMsg"] = "This run has no splits."
        elif self.editor.entries.shouldWarn():
            self.editor.saveWarning.pack(side="bottom",fill="both")

        return self.selection.game and self.selection.category and self.editor.entries.leftFrame.isValid() and (not self.editor.deleteSplitButton["state"] == "disabled")

    def save(self,retVal):
        if not retVal:
            return
        game = self.selection.game
        category = self.selection.category
        if self.splits.validPair(game,category):
            category = category + "Copy"
        csvs = self.editor.entries.generateCsvs()
        csvs["complete"] = dataManip.newCompleteCsv(csvs["names"])
        fileio.writeCSVs(self.config["baseDir"],game,category,csvs["complete"],csvs["comparisons"])
        self.splits.updateNames(game,category,csvs["names"])
