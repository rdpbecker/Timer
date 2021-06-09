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

class ScrollableFramePin(tk.Frame):
    def __init__(self,root,**kwargs):
        super().__init__(root,**kwargs)
        self.pinHeight = 0
        self.pinWidth = 0
        self.kwargs = {**kwargs}

        yscrollbar = tk.Scrollbar(self, orient='vertical', command=self.yScroll)
        yscrollbar.grid(row=1,column=2,sticky="NS")
        xscrollbar = tk.Scrollbar(self, orient='horizontal', command=self.xScroll)
        xscrollbar.grid(row=2,column=1,sticky="EW")

        self.canvases = []
        self.frames = []
        for i in range(4):
            canvas = tk.Canvas(self, width=self.kwargs["width"]/2, height=self.kwargs["height"]/2)
            frame = tk.Frame(canvas)
            canvas.create_window((0,0), window=frame, anchor="nw")
            self.canvases.append(canvas)
            self.frames.append(frame)
        self.canvases[0].grid(row=0,column=0)
        self.canvases[1].grid(row=0,column=1)
        self.canvases[2].grid(row=1,column=0)
        self.canvases[3].grid(row=1,column=1)

        self.canvases[1].configure(xscrollcommand=xscrollbar.set)
        self.canvases[2].configure(yscrollcommand=yscrollbar.set)
        self.canvases[3].configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

        self.pinnedY().bind(\
            "<Configure>",\
            self.setTop\
        )
        self.pinnedX().bind(\
            "<Configure>",\
            self.setSide\
        )
        self.main().bind(\
            "<Configure>",\
            lambda e: self.canvases[3].configure(\
                scrollregion=self.canvases[3].bbox("all")\
            )\
        )

    def corner(self):
        return self.frames[0]

    def pinnedY(self):
        return self.frames[1]

    def pinnedX(self):
        return self.frames[2]

    def main(self):
        return self.frames[3]

    def xScroll(self,*args):
        self.canvases[1].xview(*args)
        self.canvases[3].xview(*args)

    def yScroll(self,*args):
        self.canvases[2].yview(*args)
        self.canvases[3].yview(*args)

    def mainArea(self):
        return {\
            "width": self.canvases[0].winfo_width() + self.canvases[1].winfo_width(),\
            "height": self.canvases[0].winfo_height() + self.canvases[2].winfo_height()\
        }

    def setTop(self,*args):
        self.canvases[1].configure(\
            scrollregion=self.canvases[1].bbox("all")\
        )
        event = args[0]
        area = self.mainArea()
        if event.height == self.pinHeight or area["height"] < self.kwargs["height"] - 20:
            return
        height = event.height
        self.canvases[0]["height"] = height
        self.canvases[1]["height"] = height
        self.canvases[2]["height"] = area["height"] - height
        self.canvases[3]["height"] = area["height"] - height
        self.pinHeight = height

    def setSide(self,*args):
        self.canvases[2].configure(\
            scrollregion=self.canvases[2].bbox("all")\
        )
        event = args[0]
        area = self.mainArea()
        if event.width == self.pinWidth or area["width"] < self.kwargs["width"] - 20:
            return
        width = event.width
        self.canvases[0]["width"] = width
        self.canvases[2]["width"] = width
        self.canvases[1]["width"] = area["width"] - width
        self.canvases[3]["width"] = area["width"] - width
        self.pinWidth = width
