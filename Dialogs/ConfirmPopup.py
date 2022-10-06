import tkinter as tk
from Dialogs import Popup

class ConfirmPopup(Popup.Popup):
    def __init__(self,master,callbacks,title,message):
        super().__init__(master,callbacks)
        self.window.title(title)
        for i in range(12):
            self.window.columnconfigure(i,weight=1)
        label = tk.Label(self.window,text=message,fg="white",bg="black",pady=10,padx=20)
        button1 = tk.Button(self.window,text="Yes",fg="black",bg="steel blue",command=self.accept)
        button2 = tk.Button(self.window,text="No",fg="black",bg="steel blue",command=self.reject)

        label.grid(row=0,column=0,columnspan=12,sticky="WE")
        button1.grid(row=1,column=0,columnspan=6,sticky="WE")
        button2.grid(row=1,column=6,columnspan=6,sticky="WE")
