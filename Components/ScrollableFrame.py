import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self,**kwargs)
        scrollbary = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbarx = tk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        self.scrollable_frame = tk.Frame(canvas,bg="black")

        self.scrollable_frame.bind(\
            "<Configure>",\
            lambda e: canvas.configure(\
                scrollregion=canvas.bbox("all")\
            )\
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbary.set)
        canvas.configure(xscrollcommand=scrollbarx.set)

        scrollbary.pack(side="right", fill="y")
        scrollbarx.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
