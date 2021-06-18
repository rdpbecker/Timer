import tkinter as tk
from DataClasses import AllSplitNames
from Dialogs import Popup
from Components.SplitEditor import EntryGrid
from Components import GameSelector
from Components import SaveButton
from util import fileio
from util import dataManip
from util import readConfig as rc

class SplitEditor(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.localComparisons = dataManip.newComparisons()
        self.splits = AllSplitNames.Splits()
        self.config = rc.getUserConfig()

        self.selection = GameSelector.Selector(self)
        self.selection.pack(side="top",fill="x")
        self.selection.followup = self.updateRows
        self.oldGame = ""
        self.oldCategory = ""

        self.buttonFrame = tk.Frame(self)
        self.buttonFrame.pack(side="right",fill="y")

        self.entries = EntryGrid.EntryGrid(self,self.localComparisons)
        self.entries.pack(side="left")

        self.addSplitButton = tk.Button(self.buttonFrame, text="Add Split", command=self.addSplit)
        self.addSplitButton.pack(fill="x")

        self.deleteSplitButton = tk.Button(self.buttonFrame, text="Delete Split", command=self.deleteSplit)
        self.deleteSplitButton.pack(fill="x")
        if not len(self.entries.rows):
            self.deleteSplitButton["state"] = "disabled"

        self.addComparisonButton = tk.Button(self.buttonFrame, text="Add Comparison", command=self.addComparison)
        self.addComparisonButton.pack(fill="x")

        self.deleteComparisonButton = tk.Button(self.buttonFrame, text="Delete Comparison", command=self.deleteComparison)
        self.deleteComparisonButton.pack(fill="x")
        if len(self.entries.comparisons) <= 5:
            self.deleteComparisonButton["state"] = "disabled"

        self.saveButton = SaveButton.SaveButton(self.buttonFrame, {"callback": self.save})
        self.saveButton.pack(side="bottom",fill="x")

    def updateRows(self,*args):
        self.entries.pack_forget()
        if not self.splits.validPair(self.selection.game,self.selection.category):
            if not self.splits.validPair(self.oldGame,self.oldCategory):
                self.entries.pack(side="left")
                return
            self.entries = EntryGrid.EntryGrid(self,dataManip.newComparisons())
        else:
            self.entries = EntryGrid.EntryGrid(self,fileio.csvReadStart(self.config["baseDir"],self.selection.game,self.selection.category,self.splits.getSplitNames(self.selection.game,self.selection.category))[1])
        self.entries.pack(side="left")
        self.oldGame = self.selection.game
        self.oldCategory = self.selection.category

    def addSplit(self,event=None):
        self.entries.addSplit()
        self.deleteSplitButton["state"] = "active"

    def deleteSplit(self,event=None):
        self.entries.removeSplit()
        if not len(self.entries.rows):
            self.deleteSplitButton["state"] = "disabled"

    def addComparison(self,event=None):
        self.entries.addComparison()
        self.deleteComparisonButton["state"] = "active"

    def deleteComparison(self,event=None):
        self.entries.removeComparison()
        if len(self.entries.comparisons) <= 5:
            self.deleteComparisonButton["state"] = "disabled"

    def save(self,retVal):
        game = self.selection.game
        category = self.selection.category
        if self.splits.validPair(game,category):
            category = category + "Copy"
        csvs = self.entries.generateCsvs()
        csvs["complete"] = dataManip.newCompleteCsv(csvs["names"])
        fileio.writeCSVs(self.config["baseDir"],game,category,csvs["complete"],csvs["comparisons"])
        self.splits.updateNames(game,category,csvs["names"])
