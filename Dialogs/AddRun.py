import tkinter as tk
from Dialogs import BaseDialog
from Dialogs import Popup
from Components.SplitEditor import AddRunEditor

class SplitEditorP(Popup.Popup):
    def __init__(self,master,callback):
        super().__init__(master,callback)
        self.editFrame = AddRunEditor.SplitEditor(self.window)
        self.editFrame.pack(fill="both")
        self.retVal = {"game": "", "category": ""}

class SplitEditorD(BaseDialog.Dialog):
    def __init__(self):
        super().__init__()
        self.editFrame = AddRunEditor.SplitEditor(self.root)
        self.editFrame.pack(side="bottom",fill="both")
        self.editFrame.saveButton.options["callback"] = self.preSave
        self.root.protocol("WM_DELETE_WINDOW", self.preFinish)
        self.warning = None
        self.saved = False

    def setReturn(self):
        self.retVal["game"] = self.editFrame.selection.game
        self.retVal["category"] = self.editFrame.selection.category

    def preFinish(self):
        if not self.saved:
            if not self.warning:
                self.warning = tk.Label(self.root,text="A run must be saved before the window is closed")
                self.warning.pack(side="top")
            return
        self.finish()

    def preSave(self,*args):
        self.saved = True
        self.editFrame.save({})
