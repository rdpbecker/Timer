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
        self.editFrame.pack(fill="both")

    def setReturn(self):
        self.retVal["game"] = self.editFrame.selection.game
        self.retVal["category"] = self.editFrame.selection.category
