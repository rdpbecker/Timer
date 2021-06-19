import tkinter as tk
import copy
from DataClasses import AllSplitNames
from Dialogs import Popup
from Components.SplitEditor import EntryGrid
from Components import SaveButton
from util import fileio
from util import dataManip

class SplitEditor(Popup.Popup):
    def __init__(self,master,callback,state):
        super().__init__(master,callback)
        self.localComparisons = copy.deepcopy(state.comparesCsv)
        self.state = state
        self.splits = AllSplitNames.Splits()

        self.entries = EntryGrid.EntryGrid(self.window,self.localComparisons)
        self.entries.pack(side="left")

        self.addSplitButton = tk.Button(self.window, text="Add Split", command=self.addSplit)
        self.addSplitButton.pack(fill="x")

        self.deleteSplitButton = tk.Button(self.window, text="Delete Split", command=self.deleteSplit)
        self.deleteSplitButton.pack(fill="x")
        if not len(self.entries.rows):
            self.deleteSplitButton["state"] = "disabled"

        self.addComparisonButton = tk.Button(self.window, text="Add Comparison", command=self.addComparison)
        self.addComparisonButton.pack(fill="x")

        if len(self.entries.comparisons) < 5:
            enabled = "active"
        else:
            enabled = "disabled"
        self.deleteComparisonButton = tk.Button(self.window, text="Delete Comparison", command=self.deleteComparison, state=enabled)
        self.deleteComparisonButton.pack(fill="x")

        self.saveButton = SaveButton.SaveButton(self.window, \
            {"callback": self.save, \
            "valid": self.validSave, \
            "invalidMsg": "Runs must have a\nnon-empty game and\ncategory"})
        self.saveButton.pack(side="bottom",fill="x")
        self.saveWarning = tk.Label(self.window,text="Warning: some\ncurrent values are\ninvalid. For invalid\nvalues, the most\nrecent valid value\n will be saved.",fg="orange")

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

    def validSave(self):
        self.saveWarning.pack_forget()
        if self.deleteSplitButton["state"] == "disabled":
            self.saveButton.options["invalidMsg"] = "This run has no splits."
        elif self.entries.shouldWarn():
            self.saveWarning.pack(side="bottom",fill="both")

        return not self.deleteSplitButton["state"] == "disabled"

    def save(self,retVal):
        if not retVal:
            return
        csvs = self.entries.generateCsvs()
        csvs["complete"] = dataManip.adjustNamesMismatch(csvs["names"],self.state.completeCsv,self.entries.originals)
        fileio.writeCSVs(self.state.config["baseDir"],self.state.game,self.state.category,csvs["complete"],csvs["comparisons"])
        self.splits.updateNames(self.state.game,self.state.category,csvs["names"])
