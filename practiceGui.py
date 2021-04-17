# Run tkinter code in another thread

import tkinter as tk
import threading
from timeit import default_timer as timer
import practiceState, fileio 
import timeHelpers as timeh

class Gui(threading.Thread):
    labels = []
    buttons = []

    def __init__(self,state):
        threading.Thread.__init__(self)
        self.run()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)
        self.root.configure(background='black')

        ## Initialize the format of the gui and store references to all
        ## the labels so we can change them. References are stored in
        ## a grid
        anchor = 'w'
        font = ("Age",24)
        colour = 'lime green'

        label1 = tk.Label(self.root, bg='black', text="Best Split", fg='white', width=10, anchor='w')
        label1.grid(row=0,column=0,columnspan=3)
        label2 = tk.Label(self.root, bg='black', text=timeh.timeToString(self.state.bestTime,{"precision":2}), fg='white', width=12, anchor='w')
        label2.grid(row=0,column=3,columnspan=3)
        self.labels.append([label1,label2])

        label = tk.Label(self.root, bg='black', text="", fg=colour, width=12, font=font, anchor=anchor)
        label.grid(row=1,column=5,columnspan=8)
        self.labels.append([label])

        button1 = tk.Button(self.root, bg='steel blue', text="Split", fg='black', width=12, command=self.onSplitEnd)
        self.root.bind('<Return>', self.onSplitEnd)
        button1.grid(row=2,column=3,columnspan=3)
        button2 = tk.Button(self.root, bg='steel blue', text="Restart", fg='black', width=12, command=self.restart)
        self.root.bind('r', self.restart)
        button2.grid(row=2,column=0,columnspan=3)
        button3 = tk.Button(self.root, bg='steel blue', text="Start", fg='black', width=11, command=self.start)
        self.root.bind('<space>', self.start)
        button3.grid(row=2,column=6,columnspan=3)
        button4 = tk.Button(self.root, bg='steel blue', text="Finish", fg='black', width=12, command=self.finish)
        self.root.bind('f', self.finish)
        button4.grid(row=2,column=9,columnspan=3)
        self.buttons.append([button1,button2,button3])

        self.root.after(17,self.update)

        self.root.mainloop()

    ##########################################################
    ## Set the timer to update every time this is called
    ##########################################################
    def update(self):
        if self.state.started and not self.state.finished:
            self.labels[1][0].configure(text=timeh.timeToString(timer()-self.state.starttime,{"precision":2}))
        self.root.after(17,self.update)

    def restart(self,event=None):
        self.state.onRestart()
        self.labels[1][0].configure(text=timeh.timeToString(0,{"blankToDash":False,"precision":2}))

    def onSplitEnd(self,event=None):
        self.state.onSplitEnd(timer())
        self.labels[0][1].configure(text=timeh.timeToString(self.state.bestTime,{"precision":2}))

    def start(self,event=None):
        self.state.startRun(timer())

    def finish(self,event=None):
        self.state.saveTimes()
        self.root.quit()
