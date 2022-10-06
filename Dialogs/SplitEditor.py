from DataClasses import AllSplitNames
from Dialogs import Popup
from Components.SplitEditor import MainEditor
from util import fileio
from util import dataManip

class SplitEditor(Popup.Popup):
    def __init__(self,master,callback,state):
        super().__init__(master,{"accepted": callback})
        self.state = state
        self.splits = AllSplitNames.Splits()

        self.editor = MainEditor.Editor(self.window,state.comparesCsv)
        self.editor.pack()
        self.editor.saveButton.options["save"] = self.save
        self.editor.saveButton.options["valid"] = self.validSave

    def validSave(self):
        self.editor.saveWarning.pack_forget()
        check1 = len(self.editor.entries.rows) > 0
        check2 = self.editor.entries.leftFrame.isValid()
        if not check1:
            self.editor.saveButton.options["invalidMsg"] = "This run has no splits."
        elif not check2:
            self.editor.saveButton.options["invalidMsg"] = "All split names\nmust be non-empty."
        elif self.editor.entries.shouldWarn():
            self.editor.saveWarning.pack(side="bottom",fill="both")

        return check1 and check2

    def save(self):
        csvs = self.editor.entries.generateGrid()
        csvs["complete"] = dataManip.adjustNamesMismatch(csvs["names"],self.state.completeCsv,self.editor.entries.originals)
        fileio.writeCSVs(self.state.config["baseDir"],self.state.game,self.state.category,csvs["complete"],csvs["comparisons"])
        self.splits.updateNames(self.state.game,self.state.category,csvs["names"])
