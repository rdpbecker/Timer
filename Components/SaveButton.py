import tkinter as tk
from Dialogs import ConfirmPopup

class SaveButton(tk.Frame):
    def __init__(self,parent,options):
        super().__init__(parent)
        self.parent = parent
        self.options = {**{"text": "Save", "save": self.save, "valid": self.validSave, "invalidMsg": ""},**options}
        self.button = tk.Button(self)
        self.button["command"] = self.confirmSave
        self.button["text"] = self.options["text"]
        self.button.pack(side="bottom",fill="both")
        self.warning = None

    def validSave(self):
        return True

    def removeWarning(self):
        if not self.warning:
            return
        self.warning.pack_forget()
        self.warning.destroy()
        self.warning = None

    def confirmSave(self,event=None):
        if not self.options["valid"]():
            self.removeWarning()
            self.warning = tk.Label(self,text=self.options["invalidMsg"],fg="red")
            self.warning.pack(fill="both")
            return
        self.removeWarning()
        ConfirmPopup.ConfirmPopup(\
            self.parent,\
            self.options["save"],\
            "Save",\
            "Save local changes? (Closing this window will save automatically)"\
        )

    def save(self,retVal):
        pass
