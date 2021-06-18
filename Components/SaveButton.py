import tkinter as tk
from Dialogs import ConfirmPopup

class SaveButton(tk.Button):
    def __init__(self,parent,options):
        super().__init__(parent)
        self.parent = parent
        self.options = {**{"text": "Save", "callback": self.save},**options}
        self["command"] = self.confirmSave
        self["text"] = self.options["text"]

    def confirmSave(self,event=None):
        ConfirmPopup.ConfirmPopup(\
            self.parent,\
            self.options["callback"],\
            "Save",\
            "Save local changes?"\
        )

    def save(self,retVal):
        pass
