import tkinter as tk

class SegmentRow(tk.Frame):
    header = None
    diff = None
    comparison = None

    def __init__(self,parent,bg,font,fg):
        tk.Frame.__init__(self,parent)
        self.configureColumns()
        self.configure(bg=bg)
        self.header = tk.Label(self, bg=bg, font=font, fg=fg)
        self.diff = tk.Label(self, bg=bg, font=font, fg=fg)
        self.comparison = tk.Label(self, bg=bg, font=font, fg=fg)

        self.header.grid(row=0,column=0,columnspan=7,sticky='W',padx=10)
        self.diff.grid(row=0,column=7,columnspan=2,sticky='E')
        self.comparison.grid(row=0,column=9,columnspan=3,sticky='E',padx=10)

    def configureColumns(self):
        for i in range(12):
            self.columnconfigure(i,minsize=27,weight=1)

    def setHeader(self,**kwargs):
        self.header.configure(kwargs)

    def setDiff(self,**kwargs):
        self.diff.configure(kwargs)

    def setComparison(self,**kwargs):
        self.comparison.configure(kwargs)
