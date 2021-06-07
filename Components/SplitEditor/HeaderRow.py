import tkinter as tk
from Components import ValidationEntry as VE

class HeaderRow(tk.Frame):
    cellWidth = 10
    def __init__(self,parent,headerRow):
        super().__init__(parent)
        self.entries = []
        for i in range(len(headerRow)):
            if not i in [8,9]:
                self.addHeader(headerRow[i])
            else:
                entry = tk.Label(self,text=headerRow[i],width=self.cellWidth)
                entry.pack(side="left")
                self.entries.append(entry)

    def headers(self):
        return\
            [self.entries[i].val for i in range(8)]\
            + [self.entries[8]["text"],self.entries[9]["text"]]\
            + [self.entries[i].val for i in range(10,len(self.entries))]

    def addHeaders(self,newHeaders):
        for header in newHeaders:
            self.addHeader(header)

    def addHeader(self,text):
        entry = VE.Entry(self,text,{"validate": lambda name: name.find(",") < 0}, width=self.cellWidth)
        entry.pack(side="left")
        self.entries.append(entry)
