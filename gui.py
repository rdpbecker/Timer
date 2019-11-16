# Run tkinter code in another thread

import Time
import Tkinter as tk
import threading
from timeit import default_timer as timer
import State, test, config 
import userInput as user

class Gui(threading.Thread):
    labels = []
    buttons = []
    splitstart = 2
    pbstart = 10
    timer = 12
    bptstart = 14
    buttonstart = 18
    starttime = 0
    splitstarttime = 0
    splitcount = -1
    state = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.run()

    def callback(self):
        self.root.quit()

    def run(self):
        ## Initialize the state. This picks the game and category
        self.state = State.State(self.pbstart,self.splitstart)
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.configure(background='black')

        ## Initialize the format of the gui and store references to all
        ## the labels so we can change them. References are stored in
        ## a grid
        for i in range(self.splitstart):
            label = tk.Label(self.root, bg='black', text="", fg="white", width=7, anchor="w")
            label.grid(row=i,column=0,columnspan=2)
            label2 = tk.Label(self.root, bg='black', text="", fg="white", width=23, anchor='w')
            label2.grid(row=i,column=2,columnspan=4)
            label3 = tk.Label(self.root, bg='black', text="", fg="white", width=15, anchor='e')
            label3.grid(row=i,column=6,columnspan=3)
            label4 = tk.Label(self.root, bg='black', text="", fg="white", width=15)
            label4.grid(row=i,column=9,columnspan=3)
            self.labels.append([label,label2,label3,label4])
        for i in range(self.splitstart,self.pbstart):
            label = tk.Label(self.root, bg='black', text="", fg="white", width=20, anchor="w")
            label.grid(row=i,column=0,columnspan=4)
            label2 = tk.Label(self.root, bg='black', text="", fg="green", width=20, anchor='e')
            label2.grid(row=i,column=4,columnspan=4)
            label3 = tk.Label(self.root, bg='black', text="", fg="white", width=20, anchor='e')
            label3.grid(row=i,column=8,columnspan=4)
            self.labels.append([label,label2,label3])
        for i in range(self.pbstart,self.timer):
            label = tk.Label(self.root, bg='black', text="", fg="white", width=10, anchor='w')
            label.grid(row=i,column=0,columnspan=2)
            label2 = tk.Label(self.root, bg='black', text="", fg="white", width=20, anchor='w')
            label2.grid(row=i,column=2,columnspan=4)
            label3 = tk.Label(self.root, bg='black', text="", fg="white", width=15, anchor='w')
            label3.grid(row=i,column=6,columnspan=3)
            label4 = tk.Label(self.root, bg='black', text="", fg="white", width=15, anchor='e')
            label4.grid(row=i,column=9,columnspan=3)
            self.labels.append([label,label2,label3,label4])
        anchorlist = ['e','c']
        fontlist = [("Liberation Sans",18),("Helvetica",24)]
        colourlist = ['blue','lime green']
        for i in range(self.timer,self.bptstart):
            label = tk.Label(self.root, bg='black', text="", fg=colourlist[i-self.timer], width=27, font=fontlist[i-self.timer], anchor=anchorlist[i-self.timer])
            label.grid(row=i,column=0,columnspan=12)
            self.labels.append([label])

        for i in range(self.bptstart,self.buttonstart):
            label = tk.Label(self.root, bg='black', text="", fg="white", width=30, anchor='w')
            label.grid(row=i,column=0,columnspan=6)
            label4 = tk.Label(self.root, bg='black', text="", fg="white", width=15, anchor='e')
            label4.grid(row=i,column=9,columnspan=3)
            self.labels.append([label,label4])

        button1 = tk.Button(self.root, bg='steel blue', text="Change Compare", fg='black', width=15, command=self.guiSwitchCompare)
        button1.grid(row=self.buttonstart,column=6,columnspan=3)
        button2 = tk.Button(self.root, bg='steel blue', text="Split", fg='black', width=10, command=self.guiSplit)
        self.root.bind('<Return>', self.guiSplit)
        button2.grid(row=self.buttonstart,column=4,columnspan=2)
        button3 = tk.Button(self.root, bg='steel blue', text="Reset", fg='black', width=10, command=self.reset)
        self.root.bind('<space>', self.reset)
        button3.grid(row=self.buttonstart,column=2,columnspan=2)
        button4 = tk.Button(self.root, bg='steel blue', text="Skip Split", fg='black', width=10, command=self.skip)
        self.root.bind('s', self.skip)
        button4.grid(row=self.buttonstart,column=0,columnspan=2)
        button5 = tk.Button(self.root, bg='steel blue', text="Start Run", fg='black', width=15, command=self.start)
        button5.grid(row=self.buttonstart,column=9,columnspan=3)
        self.buttons.append([button1,button2,button3])

        State.guiComplete=1

        ## Initialize the text in the gui and set the timer to update 
        ## at 60ish FPS
        self.initialize()
        self.root.after(17,self.update)

        self.root.mainloop()

    ##########################################################
    ## Set the timer to update every time this is called
    ##########################################################
    def update(self):
        if self.splitcount > -1:
            self.labels[self.timer][0].configure(text=str(Time.Time(2,floattime=timer()-self.starttime)))
            self.labels[self.timer+1][0].configure(text=str(Time.Time(2,floattime=timer()-self.splitstarttime)))
        self.root.after(17,self.update)

    ##########################################################
    ## Caller to all the functions that initialize text before
    ## the run is started
    ##########################################################
    def initialize(self):
        self.initHeader()
        self.initTimes()
        self.initInfo()
        self.updateCurrentColour()

    ##########################################################
    ## Initialize the header with game, category, and
    ## comparison name
    ##########################################################
    def initHeader(self):
        self.labels[0][0].configure(text=self.state.game)
        self.labels[0][1].configure(text=self.state.category)
        self.labels[0][2].configure(text="Comparing Against")
        self.labels[0][3].configure(text="Personal Best")

    ##########################################################
    ## Initialize the split names and times for the first few
    ## splits and the last one. This is based on the PB time
    ##########################################################
    def initTimes(self):
        for i in range(self.state.windowStart,self.pbstart-self.splitstart-2):
            self.labels[self.splitstart+i][0].configure(text=self.state.splitnames[i-self.state.windowStart])
            self.labels[self.splitstart+i][2].configure(text=self.state.compares[self.state.currentCompare].get(i-self.state.windowStart).__str__(precision=2))
        self.labels[self.pbstart-2][0].configure(text=self.state.splitnames[-1])
        self.labels[self.pbstart-2][2].configure(text=self.state.compares[self.state.currentCompare].get(-1).__str__(precision=2))

    ##########################################################
    ## Initialize all the info on the bottom, including split
    ## comparisons, time save, BPT, and PB
    ##########################################################
    def initInfo(self):
        self.labels[self.pbstart][0].configure(text="PB Split:")
        self.labels[self.pbstart+1][0].configure(text="Best Split:")

        self.labels[self.bptstart][0].configure(text="Possible Time Save:")
        self.labels[self.bptstart+1][0].configure(text="Last Split (vs Best):")
        self.labels[self.bptstart+2][0].configure(text="Best Possible Time:")
        self.labels[self.bptstart+3][0].configure(text="Personal Best:")
        self.labels[self.bptstart+3][1].configure(text=self.state.compares[2].get(-1).__str__(precision=2))
        self.updateInfo()

    ##########################################################
    ## Set the colours for the current and last splits based
    ## on the current split number
    ##########################################################
    def updateCurrentColour(self):
        for i in range(0,self.pbstart-self.splitstart-1):
            if i == self.state.splitnum-self.state.getWindowStart()+self.state.windowStart:
                self.labels[self.splitstart+i][0].configure(fg="DarkOrchid2")
                self.labels[self.splitstart+i][2].configure(fg="DarkOrchid2")
            else:
                self.labels[self.splitstart+i][0].configure(fg="white")
                self.labels[self.splitstart+i][2].configure(fg="white")
        self.labels[self.pbstart-2][0].configure(fg="maroon1")
        self.labels[self.pbstart-2][2].configure(fg="maroon1")

    ##########################################################
    ## Update current split and BPT information based on the
    ## current split
    ##########################################################
    def updateInfo(self):
        self.labels[self.pbstart][1].configure(text=self.state.compareSplits[self.state.currentCompare].get(self.state.splitnum).__str__(precision=2))
        self.labels[self.pbstart+1][1].configure(text=self.state.compareSplits[0].get(self.state.splitnum).__str__(precision=2))
        self.labels[self.bptstart][1].configure(text=self.state.compareSplits[self.state.currentCompare].get(self.state.splitnum).subtract(self.state.compareSplits[0].get(self.state.splitnum)).__str__(precision=2))
        if self.state.splitnum:
            self.labels[self.bptstart+1][1].configure(text=self.state.currentSplits.get(-1).subtract(self.state.compareSplits[0].get(self.state.splitnum-1)).__str__(1,precision=2))
        if not self.state.skip:
            self.labels[self.bptstart+2][1].configure(text=self.state.bptList.sum().__str__(precision=2))

    ##########################################################
    ## Initialize the start and first split times when the run
    ## starts
    ##########################################################
    def start(self):
        self.starttime = timer()
        self.splitstarttime = timer()
        self.splitcount = 0

    def guiSwitchCompare(self):
        config.choice = (config.choice+1)%4
        config.choiceChanged = 1

    def guiSplit(self,event=None):
        user.switch = 1
        pass

    def reset(self, event=None):
        print "Close the window to end the program"
        user.switch = 1
        config.reset = 1

    def skip(self,event=None):
        user.switch = 1
        config.skip = 1
