import tkinter as tk
import copy
from DataClasses import AllSplitNames
from Dialogs import Popup
from Components.SplitEditor import EntryGrid
from Components.SplitEditor import MainEditor
from Components import SaveButton
from util import fileio
from util import dataManip

class SplitEditor(Popup.Popup):
    def __init__(self,master,callback,state):
        super().__init__(master,callback)
        self.state = state
        self.splits = AllSplitNames.Splits()

        self.editor = MainEditor.Editor(self.window,state.comparesCsv)
        self.editor.pack()
        self.editor.saveButton.options["callback"] = self.save
        self.editor.saveButton.options["valid"] = self.validSave

    def validSave(self):
        self.editor.saveWarning.pack_forget()
        if self.editor.deleteSplitButton["state"] == "disabled":
            self.editor.saveButton.options["invalidMsg"] = "This run has no splits."
        elif self.editor.entries.shouldWarn():
            self.editor.saveWarning.pack(side="bottom",fill="both")

        return not self.editor.deleteSplitButton["state"] == "disabled"

    def save(self,retVal):
        if not retVal:
            return
        csvs = self.editor.entries.generateCsvs()
        csvs["complete"] = dataManip.adjustNamesMismatch(csvs["names"],self.state.completeCsv,self.editor.entries.originals)
        fileio.writeCSVs(self.state.config["baseDir"],self.state.game,self.state.category,csvs["complete"],csvs["comparisons"])
        self.splits.updateNames(self.state.game,self.state.category,csvs["names"])
