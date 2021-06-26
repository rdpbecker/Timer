import tkinter as tk
from tkinter import ttk
from Components import GameSelector
from Components import LayoutSelector
from Components import RunsMenu
from Dialogs import BaseDialog
from util import fileio
from util import layoutHelper as lh

class RunSelector(BaseDialog.Dialog):
    layoutName = "System Default"
    layoutVar = None

    def __init__(self,splits):
        super().__init__()

        self.root.title("Choose Run and Layout")
        self.root.configure(bg="black",menu=RunsMenu.Menu(self.root,self.setRun))

        self.selector = GameSelector.Selector(self.root)
        self.selector.pack(fill="x")

        self.layouts = LayoutSelector.Selector(self.root)
        self.layouts.pack(fill="x")

        confirm = tk.Button(self.root,fg="black",bg="steel blue",text="Confirm Selection",command=self.accept)
        confirm.pack(fill="x")

        self.error = None

    def setRun(self,game,category):
        self.selector.game = game
        self.selector.gameVar.set(game)
        self.selector.category = category
        self.selector.cateVar.set(category)
        self.selector.updateCateCombo()

    def accept(self):
        if not self.selector.game or not self.selector.category or not self.layouts.layoutName:
            if not self.error:
                self.error = tk.Label(self.root,bg="black",fg="white",text="A game and category must both be selected.")
                self.error.pack(fill="x")
            return
        self.setReturn()
        self.retVal["exitCode"] = "accept"
        self.root.destroy()

    def finish(self):
        self.accept()

    def setReturn(self):
        self.retVal["game"] = self.selector.game
        self.retVal["category"] = self.selector.category
        self.retVal["splitNames"] = self.selector.splits.getSplitNames(self.selector.game,self.selector.category)
        self.retVal["layoutName"] = self.layouts.layoutName
