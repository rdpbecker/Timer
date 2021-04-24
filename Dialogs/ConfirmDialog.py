import tkinter as tk
from Dialogs import BaseDialog

class ConfirmDialog(BaseDialog.Dialog):
    message = ""

    def __init__(self,message):
        BaseDialog.Dialog.__init__(self)
        self.root.columnconfigure(12,weight=1)
        self.message = message
        label = tk.Label(self.root,text=message,fg="white",bg="black",pady=10,padx=20)
        button1 = tk.Button(self.root,text="Yes",fg="black",bg="steel blue",command=self.accept)
        button2 = tk.Button(self.root,text="No",fg="black",bg="steel blue",command=self.reject)

        label.grid(row=0,column=0,columnspan=12,sticky="WE")
        button1.grid(row=1,column=0,columnspan=6,sticky="WE")
        button2.grid(row=1,column=6,columnspan=6,sticky="WE")

    def finish(self):
        self.root.quit()
        self.retVal = True
