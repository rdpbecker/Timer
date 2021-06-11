import tkinter as tk
from DataClasses import AllSplitNames
from Dialogs import Popup
from Components.SplitEditor import EntryGrid
from Components import SaveButton
from util import fileio
from util import dataManip

class SplitEditor(Popup.Popup):
    def __init__(self,master,callback,state):
        super().__init__(master,callback)
        self.localComparisons = dataManip.newComparisons()
        self.splits = AllSplitNames.Splits()

        self.entries = EntryGrid.EntryGrid(self.window,self.localComparisons)
        self.entries.pack(side="left")

        self.addSplitButton = tk.Button(self.window, text="Add Split", command=self.addSplit)
        self.addSplitButton.pack(fill="x")

        self.deleteSplitButton = tk.Button(self.window, text="Delete Split", command=self.deleteSplit)
        self.deleteSplitButton.pack(fill="x")

        self.addComparisonButton = tk.Button(self.window, text="Add Comparison", command=self.addComparison)
        self.addComparisonButton.pack(fill="x")

        if len(self.entries.comparisons) < 5:
            enabled = "active"
        else:
            enabled = "disabled"
        self.deleteComparisonButton = tk.Button(self.window, text="Delete Comparison", command=self.deleteComparison, state=enabled)
        self.deleteComparisonButton.pack(fill="x")

        self.saveButton = SaveButton.SaveButton(self.window, {"callback": self.save})
        self.saveButton.pack(side="bottom",fill="x")

        self.retVal = {"game": "", "category": ""}

    def addSplit(self,event=None):
        self.entries.addSplit()

    def deleteSplit(self,event=None):
        self.entries.removeSplit()

    def addComparison(self,event=None):
        self.entries.addComparison()
        self.deleteComparisonButton["state"] = "active"

    def deleteComparison(self,event=None):
        self.entries.removeComparison()
        if len(self.entries.comparisons) <= 5:
            self.deleteComparisonButton["state"] = "disabled"

    def save(self,retVal):
        csvs = self.entries.generateCsvs()
        csvs["complete"] = dataManip.newCompleteCsv(csvs["names"])
        fileio.writeCSVs(self.state.config["baseDir"],self.state.game,self.state.category,csvs["complete"],csvs["comparisons"])
        self.splits.updateNames(self.state.game,self.state.category,csvs["names"])
