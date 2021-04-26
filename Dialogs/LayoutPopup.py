import tkinter as tk
from tkinter import ttk
from Dialogs import Popup
from util import layoutHelper as lh

class LayoutPopup(Popup.Popup):
    layoutVar = None

    def __init__(self,master,callback):
        Popup.Popup.__init__(self,master,callback)

    def show(self):
        self.retVal = "System Default"
        self.window.configure(bg="black")

        self.layoutVar = tk.StringVar()
        self.layoutVar.set("System Default")
        self.layoutVar.trace('w',self.setLayout)
        layoutCombo = tk.ttk.Combobox(self.window,values=lh.getLayouts(),textvariable=self.layoutVar)
        layoutLabel = tk.Label(self.window,bg="black",fg="white",text="Layout:")
        layoutCombo.grid(row=0,column=4,columnspan=8,sticky="WE")
        layoutLabel.grid(row=0,column=0,columnspan=4,sticky="W")

        confirm = tk.Button(self.window,fg="black",bg="steel blue",text="Confirm Selection",command=self.accept)
        confirm.grid(row=1,column=0,columnspan=12,sticky="WE")

    def setLayout(self,*args):
        self.retVal = self.layoutVar.get()
