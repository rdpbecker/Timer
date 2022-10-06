import tkinter as tk
from Dialogs import BaseDialog
from Dialogs import Popup
from Components.SplitEditor import AddRunEditor

class SplitEditorP(Popup.Popup):
    def __init__(self,master,callback):
        super().__init__(master,{"accepted": callback})
        self.editFrame = AddRunEditor.SplitEditor(self.window)
        self.editFrame.pack(fill="both")
        self.retVal = {"game": "", "category": ""}

class SplitEditorD(BaseDialog.Dialog):
    def __init__(self):
        super().__init__()
        self.editFrame = AddRunEditor.SplitEditor(self.root)
        self.editFrame.pack(side="bottom",fill="both")
        self.editFrame.editor.saveButton.options["save"] = self.preSave
        self.root.protocol("WM_DELETE_WINDOW", self.preFinish)
        self.warning = None
        self.note = None
        self.saved = False

    def setReturn(self):
        self.retVal["game"] = self.editFrame.selection.game
        self.retVal["category"] = self.editFrame.selection.category

    def preFinish(self):
        if not self.saved:
            if not self.warning:
                self.warning = tk.Label(self.root,text="A run must be saved before the window is closed",fg="red")
                self.warning.pack(side="top")
            return
        self.finish()

    def preSave(self,*_):
        self.saved = True
        self.editFrame.save(True)
        if not self.note:
            self.note = tk.Label(self.root,text="To start the run, close this window.",fg="green")
            self.note.pack()
        if self.warning:
            self.warning.pack_forget()
            self.warning = None
