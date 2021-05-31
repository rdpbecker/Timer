import tkinter as tk
from Widgets import ScrollableFrame
from Variance import VarianceRow

class VarianceColumn(tk.Frame):
    def __init__(self,parent,header):
        super().__init__(parent)
        self.configure(bg="black")
        tk.Label(self,text=header,fg="white",bg="black").pack(side="top")
        self.scrollable = ScrollableFrame.ScrollableFrame(self)
        self.scrollable.pack(side="bottom")
        self.rows = []

    def update(self,table):
        for row in self.rows:
            row.remove()
        self.rows = []
        for row in table:
            self.createRow(row)

    def createRow(self,row):
        new_row = VarianceRow.VarianceRow(self.scrollable.scrollable_frame,[len(self.rows)+1,row[0],row[1]])
        new_row.pack(side="top",anchor="nw")
        self.rows.append(new_row)
