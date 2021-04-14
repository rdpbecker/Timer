import tkinter as tk

class Component(tk.Frame):
    state = None

    def __init__(self,parent,state):
        tk.Frame.__init__(self,parent)
        self.state = state
        self.configureColumns()

    def configureColumns(self):
        for i in range(12):
            self.columnconfigure(i,weight=1)
