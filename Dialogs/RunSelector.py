import tkinter as tk
from tkinter import ttk
from Components import GameSelector
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
        self.selector.grid(row=0,column=0,columnspan=12,sticky="WE")

        self.layoutVar = tk.StringVar()
        self.layoutVar.set("System Default")
        self.layoutVar.trace('w',self.setLayout)
        self.layoutCombo = tk.ttk.Combobox(self.root,values=lh.getLayouts(),textvariable=self.layoutVar)
        layoutLabel = tk.Label(self.root,bg="black",fg="white",text="Layout:")
        self.layoutCombo.grid(row=1,column=4,columnspan=8,sticky="WE")
        layoutLabel.grid(row=1,column=0,columnspan=4,sticky="W")

        confirm = tk.Button(self.root,fg="black",bg="steel blue",text="Confirm Selection",command=self.accept)
        confirm.grid(row=2,column=0,columnspan=12,sticky="WE")

    def setRun(self,game,category):
        self.selector.game = game
        self.selector.gameVar.set(game)
        self.selector.category = category
        self.selector.cateVar.set(category)
        self.selector.updateCateCombo()

    def setLayout(self,*args):
        self.layoutName = self.layoutVar.get()

    def accept(self):
        if not self.selector.game or not self.selector.category or not self.layoutName:
            error = tk.Label(self.root,bg="black",fg="white",text="A game and category must both be selected.")
            error.grid(row=3,column=0,columnspan=12,sticky="WE")
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
        self.retVal["layoutName"] = self.layoutName
