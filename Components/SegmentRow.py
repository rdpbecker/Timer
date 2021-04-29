import tkinter as tk
import tkinter.font as tkfont

class SegmentRow(tk.Frame):
    header = None
    diff = None
    comparison = None

    def __init__(self,parent,bg,font,fg):
        tk.Frame.__init__(self,parent)
        self.configureColumns()
        self.configure(bg=bg)
        self.font = tkfont.Font(font=font)
        self.header = tk.Label(self, bg=bg, font=font, fg=fg)
        self.diff = tk.Label(self, bg=bg, font=font, fg=fg)
        self.comparison = tk.Label(self, bg=bg, font=font, fg=fg)

        self.header.grid(row=0,column=0,columnspan=7,sticky='W',padx=10)
        self.diff.grid(row=0,column=7,columnspan=2,sticky='E')
        self.comparison.grid(row=0,column=9,columnspan=3,sticky='E',padx=10)

    def configureColumns(self):
        for i in range(12):
            self.columnconfigure(i,minsize=27,weight=1)

    def adjustTextLength(self,maxLength,text):
        ellipsis = "..."
        low = 0
        high = len(text)
        current = int(len(text)/2)
        last = 0
        while low < high - 1:
            if self.font.measure(text[:current]+ellipsis) <= maxLength:
                low = current
                current = low + int((high-low)/2)
            else:
                high = current
                current = low + int((high-low)/2)
        return text[:low] + ellipsis

    def setHeaderText(self,text):
        self.update()
        frameLength = self.winfo_width()
        textLength = self.font.measure(text)
        if textLength <= 7*frameLength/12:
            self.header["text"] = text
        else:
            self.header["text"] = self.adjustTextLength(7*frameLength/12,text)

    def setHeader(self,**kwargs):
        self.header.configure(kwargs)

    def setDiff(self,**kwargs):
        self.diff.configure(kwargs)

    def setComparison(self,**kwargs):
        self.comparison.configure(kwargs)
