import tkinter as tk
from Components import LayoutSelector
from Dialogs import Popup

class LayoutPopup(Popup.Popup):
    layoutVar = None
    session = None

    def __init__(self,master,callback,session):
        super().__init__(master,callback)
        self.session = session

        self.window.configure(bg="black")
        self.window.title("Choose Layout")

        self.layouts = LayoutSelector.Selector(self.window)
        self.layouts.pack()
        self.retVal["layoutName"] = self.session.layoutName
        self.layouts.layoutVar.set(self.session.layoutName)

        confirm = tk.Button(self.window,fg="black",bg="steel blue",text="Confirm Selection",command=self.accept)
        confirm.pack(fill="x")

    def setReturn(self):
        self.retVal["layoutName"] = self.layouts.layoutName
