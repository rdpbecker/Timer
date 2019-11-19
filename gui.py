# Run tkinter code in another thread

import Time
import Tkinter as tk
import threading
from timeit import default_timer as timer
import State, test, config, fileio 
import userInput as user

class Gui(threading.Thread):
    labels = []
    buttons = []
    splitstart = 2
    pbstart = 10
    timer = 12
    bptstart = 14
    buttonstart = 18
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
            label2 = tk.Label(self.root, bg='black', text="", fg="white", width=18, anchor='w')
            label2.grid(row=i,column=2,columnspan=3)
            label3 = tk.Label(self.root, bg='black', text="", fg="white", width=20, anchor='e')
            label3.grid(row=i,column=5,columnspan=4)
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
            label = tk.Label(self.root, bg='black', text="", fg="white", width=15, anchor='w')
            label.grid(row=i,column=0,columnspan=3)
            label2 = tk.Label(self.root, bg='black', text="", fg="white", width=15, anchor='w')
            label2.grid(row=i,column=3,columnspan=3)
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
        button2 = tk.Button(self.root, bg='steel blue', text="Split", fg='black', width=10, command=self.onSplitEnd)
        self.root.bind('<Return>', self.onSplitEnd)
        button2.grid(row=self.buttonstart,column=4,columnspan=2)
        button3 = tk.Button(self.root, bg='steel blue', text="Reset", fg='black', width=10, command=self.reset)
        self.root.bind('r', self.reset)
        button3.grid(row=self.buttonstart,column=2,columnspan=2)
        button4 = tk.Button(self.root, bg='steel blue', text="Skip Split", fg='black', width=10, command=self.skip)
        self.root.bind('s', self.skip)
        button4.grid(row=self.buttonstart,column=0,columnspan=2)
        button5 = tk.Button(self.root, bg='steel blue', text="Start Run", fg='black', width=15, command=self.start)
        button5.grid(row=self.buttonstart,column=9,columnspan=3)
        self.root.bind('<space>', self.start)
        self.buttons.append([button1,button2,button3])

        ## Initialize the text in the gui and set the timer to update 
        ## at 60ish FPS
        self.initialize()
        self.root.after(17,self.update)

        self.root.mainloop()

    ##########################################################
    ## Set the timer to update every time this is called
    ##########################################################
    def update(self):
        if self.state.started:
            self.labels[self.timer+1][0].configure(text=Time.Time(2,floattime=timer()-self.state.starttime).__str__(flag2=0))
            self.labels[self.timer][0].configure(text=Time.Time(0,floattime=timer()-self.state.splitstarttime).__str__(flag2=0))
        if self.state.splitnum < len(self.state.splitnames) and not self.state.reset:
            self.root.after(8,self.update)
        else:
            self.root.after(1,self.state.doEnd)

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
        windowStart = self.state.getWindowStart()
        for i in range(0,self.pbstart-self.splitstart-1):
            if i == self.state.splitnum-windowStart+self.state.windowStart:
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
        if self.state.splitnum > 0:
            self.labels[self.bptstart+1][1].configure(text=self.state.currentSplits.get(-1).subtract(self.state.compareSplits[0].get(self.state.splitnum-1)).__str__(1,precision=2))
        if not self.state.skip:
            self.labels[self.bptstart+2][1].configure(text=self.state.bptList.sum().__str__(precision=2))

    ##########################################################
    ## Initialize the start and first split times when the run
    ## starts
    ##########################################################
    def start(self, event=None):
        self.state.starttime = timer()
        self.state.splitstarttime = timer()
        self.state.started = True

    ##########################################################
    ## At the end of each split, record and store the times, 
    ## calculate all the diffs, and call the helper functions 
    ## to update the GUI
    ##########################################################
    def onSplitEnd(self,event=None):
        splitEnd = timer()
        totalTime = Time.Time(5,floattime=splitEnd-self.state.starttime)
        splitTime = Time.Time(5,floattime=splitEnd-self.state.splitstarttime)
        self.state.currentSplits.insert(splitTime)
        self.state.currentTotals.insert(totalTime)

        self.state.bptList.replace(Time.Time(5,floattime=splitEnd-self.state.splitstarttime),self.state.splitnum)
        for i in range(4):
            self.state.diffs[i].insert(totalTime.subtract(self.state.compares[i].get(self.state.splitnum)))
            self.state.diffSplits[i].insert(self.state.currentSplits.get(self.state.splitnum).subtract(self.state.compareSplits[i].get(self.state.splitnum)))
        self.state.splitnum = self.state.splitnum + 1
        lowIndex = self.state.getWindowStart()
        self.updateTimes(lowIndex)
        self.updateCurrentColour()
        if self.state.splitnum < len(self.state.splitnames):
            self.updateInfo()
        self.state.splitstarttime = splitEnd

    ##########################################################
    ## Update the times and split names in the split portion 
    ## of the GUI. This includes shifting entries as needed so
    ## the current split is the third entry in the list, and 
    ## colouring the diff numbers properly
    ##
    ## Parameters: lowIndex - the index in state.splitNames of
    ##                        the split at the top of the 
    ##                        section
    ##########################################################
    def updateTimes(self,lowIndex):
        ## i is the number from the top of the list of splits. For the 
        ## top entry i=0, the next one down has i=1, and so on
        ##
        ## lowIndex is the index in the list of splits of the top split
        ## in the gui - if split #5 is at the top of the view area in
        ## the gui, then lowIndex=5
        ## 
        ## windowStart is the index at which the window in the GUI starts
        ## This is determined only by the total number of splits, and
        ## for categories with more than 7 splits windowStart=0
        for i in range(self.state.windowStart,self.pbstart-self.splitstart-2):
            ## The index of the split we're looking at currently
            subjectSplitIndex = i+lowIndex-self.state.windowStart
            self.labels[self.splitstart+i][0].configure(text=self.state.splitnames[subjectSplitIndex])
            if self.state.splitnum > subjectSplitIndex:
                if not self.state.compareSplits[self.state.currentCompare].get(subjectSplitIndex).equal(Time.Time(5,timestring='-')):
                    self.labels[self.splitstart+i][1].configure(text=self.state.diffs[self.state.currentCompare].get(subjectSplitIndex).__str__(1,precision=2))
                else:
                    self.labels[self.splitstart+i][1].configure(text='-')
                self.labels[self.splitstart+i][2].configure(text=self.state.currentTotals.get(subjectSplitIndex).__str__(precision=2))
                if self.state.diffSplits[0].get(subjectSplitIndex).greater(Time.Time(5,timestring='-')) == -1:
                    self.labels[self.splitstart+i][1].configure(fg='gold')
                elif (self.state.diffs[self.state.currentCompare].get(subjectSplitIndex).greater(Time.Time(5,timestring='-')) == -1) or (self.state.compareSplits[self.state.currentCompare].get(subjectSplitIndex).equal(Time.Time(2,timestring='-'))):
                    self.labels[self.splitstart+i][1].configure(fg='green')
                else:
                    self.labels[self.splitstart+i][1].configure(fg='red')
            else:
                self.labels[self.splitstart+i][1].configure(text="")
                self.labels[self.splitstart+i][2].configure(text=self.state.compares[self.state.currentCompare].get(subjectSplitIndex).__str__(precision=2))
        if self.state.splitnum >= len(self.state.splitnames):
            self.labels[self.pbstart-2][1].configure(text=self.state.diffs[self.state.currentCompare].get(-1).__str__(1,precision=2))
            self.labels[self.pbstart-2][2].configure(text=self.state.currentTotals.get(-1).__str__(precision=2))
            if self.state.diffs[0].get(-1).greater(Time.Time(5,timestring='-')) == -1:
                self.labels[self.pbstart-2][1].configure(fg='gold')
            elif self.state.diffs[self.state.currentCompare].get(-1).greater(Time.Time(5,timestring='-')) == -1:
                self.labels[self.pbstart-2][1].configure(fg='green')
            else:
                self.labels[self.pbstart-2][1].configure(fg='red')

    ##########################################################
    ## Update information about the comparison splits when the 
    ## comparison is changed
    ##########################################################
    def updateCompare(self):
        self.labels[0][3].configure(text=self.state.compareHeaders[self.state.currentCompare])
        self.labels[self.pbstart][0].configure(text=self.state.splitCompareHeaders[self.state.currentCompare]+":")
        self.labels[self.pbstart-2][2].configure(text=self.state.compares[self.state.currentCompare].get(-1).__str__(precision=2))

    ##########################################################
    ## The function called when the 'Switch Compare' button is
    ## clicked
    ##########################################################
    def guiSwitchCompare(self,event=None):
        self.state.currentCompare = (self.state.currentCompare+1)%4
        lowIndex = self.state.getWindowStart()
        self.updateTimes(lowIndex)
        self.updateInfo()
        self.updateCompare()

    ##########################################################
    ## Stop the run here
    ##########################################################
    def reset(self, event=None):
        self.state.reset = True

    ##########################################################
    ## Skip a split
    ##########################################################
    def skip(self,event=None):
        splitEnd = timer()
        totalTime = Time.Time(5,floattime=0)
        splitTime = Time.Time(5,floattime=0)
        self.state.currentSplits.insert(splitTime)
        self.state.currentTotals.insert(totalTime)

        self.state.bptList.replace(Time.Time(5,floattime=splitEnd-self.state.splitstarttime),self.state.splitnum)
        for i in range(4):
            self.state.diffs[i].insert(Time.Time(5,floattime=0))
            self.state.diffSplits[i].insert(Time.Time(5,floattime=0))
        self.state.splitnum = self.state.splitnum + 1
        lowIndex = self.state.getWindowStart()
        self.updateTimes(lowIndex)
        self.updateCurrentColour()
        if self.state.splitnum < len(self.state.splitnames):
            self.updateInfo()
        self.state.splitstarttime = splitEnd
