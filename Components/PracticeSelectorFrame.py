import tkinter as tk
from Components import SplitSelector

class Frame(tk.Frame):
    def __init__(self,parent,callback):
        super().__init__(parent)
        self.selector = SplitSelector.Selector(parent)
        self.selector.pack(fill="x")

        confirm = tk.Button(parent,fg="black",bg="steel blue",text="Confirm Selection",command=callback)
        confirm.pack(fill="x")

        self.error = None

    def setSplit(self,game,category,split):
        self.selector.gameVar.set(game)
        self.selector.cateVar.set(category)
        self.selector.splitVar.set(split)
        self.selector.updateCateCombo()
        self.selector.updateNameCombo()
