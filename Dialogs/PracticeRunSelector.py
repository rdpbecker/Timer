import tkinter as tk
from Components import RunsMenu
from Components import SplitSelector
from Dialogs import BaseDialog

class RunSelector(BaseDialog.Dialog):
    def __init__(self):
        super().__init__()
        self.root.title("Choose Run and Split")

        self.root.configure(bg="black",menu=RunsMenu.PracticeMenu(self.root,self.setSplit))

        self.selector = SplitSelector.Selector(self.root)
        self.selector.grid(row=0,column=0,columnspan=12,sticky="WE")

        confirm = tk.Button(self.root,fg="black",bg="steel blue",text="Confirm Selection",command=self.accept)
        confirm.grid(row=1,column=0,columnspan=12,sticky="WE")

    def setSplit(self,game,category,split):
        self.selector.game = game
        self.selector.gameVar.set(game)
        self.selector.category = category
        self.selector.cateVar.set(category)
        self.selector.split = split
        self.selector.splitVar.set(split)
        self.selector.updateCateCombo()
        self.selector.updateNameCombo()

    def accept(self):
        if not self.selector.game or not self.selector.category or not self.selector.split:
            error = tk.Label(self.root,bg="black",fg="white",text="A game, category, and segment must all be selected.")
            error.grid(row=2,column=0,columnspan=12,sticky="WE")
            return
        self.retVal["exitCode"] = "accept"
        self.setReturn()
        self.root.destroy()

    def finish(self):
        self.accept()

    def setReturn(self):
        self.retVal["game"] = self.selector.game
        self.retVal["category"] = self.selector.category
        self.retVal["split"] = self.selector.split
        self.retVal["splitNames"] = self.selector.splits.getSplitNames(self.selector.game,self.selector.category)
