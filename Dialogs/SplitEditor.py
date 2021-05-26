import tkinter as tk
from Dialogs import Popup

class SplitEditor(Popup.Popup):
    def __init__(self,master,callback,state):
        Popup.Popup.__init__(self,master,callback)
