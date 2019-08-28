# Run tkinter code in another thread

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

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.configure(background='black')

        for i in range(self.splitstart):
            label = tk.Label(self.root, bg='black', text="", fg="white", width=7, anchor="w")
            label.grid(row=i,column=0,columnspan=2)
            label2 = tk.Label(self.root, bg='black', text="", fg="white", width=13, anchor='w')
            label2.grid(row=i,column=2,columnspan=2)
            label3 = tk.Label(self.root, bg='black', text="", fg="white", width=25, anchor='e')
            label3.grid(row=i,column=4,columnspan=5)
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
        button2 = tk.Button(self.root, bg='steel blue', text="Split", fg='black', width=15, command=self.guiSplit)
        self.root.bind('<Return>', self.guiSplit)
        button2.grid(row=self.buttonstart,column=9,columnspan=3)
        button3 = tk.Button(self.root, bg='steel blue', text="Reset", fg='black', width=15, command=self.reset)
        self.root.bind('<space>', self.reset)
        button3.grid(row=self.buttonstart,column=3,columnspan=3)
        button4 = tk.Button(self.root, bg='steel blue', text="Skip Split", fg='black', width=15, command=self.skip)
        self.root.bind('s', self.skip)
        button4.grid(row=self.buttonstart,column=0,columnspan=3)
        self.buttons.append([button1,button2,button3])

        State.guiComplete=1

        self.root.mainloop()

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
