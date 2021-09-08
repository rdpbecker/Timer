import tkinter as tk
from Components import GameSelector
from Components import RunsMenu
from Dialogs import Popup

class RunPopup(Popup.Popup):
    def __init__(self,master,callback,session):
        super().__init__(master,callback)
        self.session = session

        self.window.title("Choose Run")
        self.window.configure(bg="black",menu=RunsMenu.Menu(self.window,self.setRun))

        self.selector = GameSelector.Selector(self.window)
        self.selector.gameVar.set(session.game)
        self.selector.cateVar.set(session.category)
        self.selector.pack()

        confirm = tk.Button(self.window,fg="black",bg="steel blue",text="Confirm Selection",command=self.accept)
        confirm.pack(fill="x")

    def setRun(self,game,category):
        self.selector.gameVar.set(game)
        self.selector.cateVar.set(category)

    def setReturn(self):
        self.retVal["game"] = self.selector.game
        self.retVal["category"] = self.selector.category
