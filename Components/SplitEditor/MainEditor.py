import tkinter as tk
import copy
from DataClasses import AllSplitNames
from Components.SplitEditor import EntryGrid
from Components import SaveButton

class Editor(tk.Frame):
    def __init__(self,master,comparisons):
        super().__init__(master)
        self.localComparisons = copy.deepcopy(comparisons)
        self.splits = AllSplitNames.Splits()

        self.buttonFrame = tk.Frame(self)
        self.buttonFrame.pack(side="right",fill="y")

        self.entries = EntryGrid.EntryGrid(self,self.localComparisons,self)
        self.entries.pack(side="left")

        self.addSplitButton = tk.Button(self.buttonFrame, text="Add Split", command=self.addSplit)
        self.addSplitButton.pack(fill="x")

        self.deleteSplitButton = tk.Button(self.buttonFrame, text="Delete Split", command=self.deleteSplit, state="disabled")
        self.deleteSplitButton.pack(fill="x")

        self.addComparisonButton = tk.Button(self.buttonFrame, text="Add Comparison", command=self.addComparison)
        self.addComparisonButton.pack(fill="x")

        self.deleteComparisonButton = tk.Button(self.buttonFrame, text="Delete Comparison", command=self.deleteComparison)
        self.deleteComparisonButton.pack(fill="x")
        if len(self.entries.comparisons) <= 5:
            self.deleteComparisonButton["state"] = "disabled"

        self.saveButton = SaveButton.SaveButton(self.buttonFrame, \
            {"save": self.save, \
            "valid": self.validSave, \
            "invalidMsg": "Current data is invalid."})
        self.saveButton.pack(side="bottom",fill="x")
        self.saveWarning = tk.Label(self.buttonFrame,text="Warning: some\ncurrent values are\ninvalid. For invalid\nvalues, the most\nrecent valid value\n will be saved.",fg="orange")

    def addSplit(self,event=None):
        self.entries.addSplit()
        self.deleteSplitButton["state"] = "active"

    def deleteSplit(self,event=None):
        self.entries.removeSplit()
        self.updateDeleteState()

    def addComparison(self,event=None):
        self.entries.addComparison()
        self.deleteComparisonButton["state"] = "active"

    def deleteComparison(self,event=None):
        self.entries.removeComparison()
        if len(self.entries.comparisons) <= 5:
            self.deleteComparisonButton["state"] = "disabled"

    def updateDeleteState(self):
        if not len(self.entries.rows) or self.entries.leftFrame.currentSplit < 0:
            self.deleteSplitButton["state"] = "disabled"
        else:
            self.deleteSplitButton["state"] = "active"

    def validSave(self):
        pass

    def save(self,retVal):
        pass
