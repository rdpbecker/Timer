import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self,bg="black",width=200)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas,bg="black")

        self.scrollable_frame.bind(\
            "<Configure>",\
            lambda e: canvas.configure(\
                scrollregion=canvas.bbox("all")\
            )\
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class VarianceRow(tk.Frame):
    number = None
    name = None
    variance = None
    def __init__(self,parent,row):
        tk.Frame.__init__(self,parent)
        for i in range(12):
            self.columnconfigure(i,weight=1)
        self.number = tk.Label(self,text=f'{row[0]}:',fg="white",bg="black")
        self.name = tk.Label(self,text=row[1],fg="white",bg="black")
        self.variance = tk.Label(self,text=f'{row[2]:.2%}',fg="white",bg="black")

        self.number.grid(row=0,column=0,columnspan=1,sticky='W')
        self.name.grid(row=0,column=1,columnspan=6)
        self.variance.grid(row=0,column=7,columnspan=5,sticky='E')

    def remove(self):
        self.number.grid_forget()
        self.number.destroy()
        self.name.grid_forget()
        self.name.destroy()
        self.variance.grid_forget()
        self.variance.destroy()
        self.grid_forget()
        self.destroy()

class VarianceColumn(tk.Frame):
    def __init__(self,parent,header):
        super().__init__(parent)
        self.configure(bg="black")
        tk.Label(self,text=header,fg="white",bg="black").pack(side="top")
        self.scrollable = ScrollableFrame(self)
        self.scrollable.pack(side="bottom")
        self.rows = []

    def update(self,table):
        for row in self.rows:
            row.remove()
        self.rows = []
        for row in table:
            self.createRow(row)

    def createRow(self,row):
        new_row = VarianceRow(self.scrollable.scrollable_frame,[len(self.rows)+1,row[0],row[1]])
        new_row.pack(side="top")
        self.rows.append(new_row)
