import tkinter as tk
from Components import PracticeSelectorFrame
from Components import RunsMenu
from Components import SplitSelector
from Dialogs import BaseDialog
from Dialogs import Popup

class RunSelector(BaseDialog.Dialog):
    def __init__(self):
        super().__init__()
        self.root.title("Choose Run and Split")

        self.content = PracticeSelectorFrame.Frame(self.root,self.accept)
        self.content.pack(fill="x")

        self.root.configure(bg="black",menu=RunsMenu.PracticeMenu(self.root,self.content))

        self.error = None

    def accept(self):
        if not self.content.selector.game or not self.content.selector.category or not self.content.selector.split:
            if not self.error:
                self.error = tk.Label(self.root,bg="black",fg="white",text="A game, category, and segment must all be selected.")
                self.error.pack(fill="x")
            return
        super().accept()

    def finish(self):
        self.accept()

    def setReturn(self):
        self.retVal["game"] = self.content.selector.game
        self.retVal["category"] = self.content.selector.category
        self.retVal["split"] = self.content.selector.split

class SelectorP(Popup.Popup):
    def __init__(self,master,callback,session):
        super().__init__(master,callback)
        self.window.title("Choose Run and Split")

        self.content = PracticeSelectorFrame.Frame(self.window,self.accept)
        self.content.selector.gameVar.set(session.game)
        self.content.selector.cateVar.set(session.category)
        self.content.selector.splitVar.set(session.split)
        self.content.pack(fill="x")

        self.window.configure(bg="black",menu=RunsMenu.PracticeMenu(self.window,self.content))

        self.error = None

    def accept(self):
        if not self.content.selector.game or not self.content.selector.category or not self.content.selector.split:
            if not self.error:
                self.error = tk.Label(self.window,bg="black",fg="white",text="A game, category, and segment must all be selected.")
                self.error.pack(fill="x")
            return
        super().accept()

    def setReturn(self):
        self.retVal["game"] = self.content.selector.game
        self.retVal["category"] = self.content.selector.category
        self.retVal["split"] = self.content.selector.split
