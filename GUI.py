import sys
import tkinter as tk
from tkinter import *
from tkinter.ttk import Treeview
from PIL import ImageTk,Image
from tkinter import filedialog
from tkinter import messagebox


class GUI(tk.Tk):
    __instance = None

    @staticmethod 
    def getInstance():
      if GUI.__instance == None:
        GUI()
      return GUI.__instance
    
    def __init__(self):
        if GUI.__instance != None:
         raise Exception("GUI class is a singleton!")
        else:
         GUI.__instance = self
         tk.Tk.__init__(self)
         self.geometry("500x500")
         self.title("CV Hunter")
         self.resizable(0,0)
         self.var=tk.IntVar()
         self.iconbitmap(r'CV_Hunter_MaroonBG.ico')
         self.container = tk.Frame(self)
         self.container.pack(side="top",fill="both",expand=True)
         self.container.grid_rowconfigure(0, weight=1)   # make the cell in grid cover the entire window
         self.container.grid_columnconfigure(0,weight=1) # make the cell in grid cover the entire window
         self.frames = {} # these are pages we want to navigate to
         for F in (StartPage,ScanningGUI,CVsView): # for each page
            frame = F(self.container, self) # create the page
            self.frames[F] = frame  # store into frames
            frame.grid(row=0, column=0,sticky="nsew") # grid it to container
        self.show_StartPage(StartPage) # let the first page is StartPage

    def show_ScanningPage(self, name):
        self.startPage= self.frames[StartPage]
        self.CvsDir = self.startPage.DirTxt.get()
        self.JobDes=self.startPage.JobDescription.get("1.0",END)
        if (self.CvsDir  !="" and len(self.JobDes)>2):
            frame = self.frames[name]
            frame.tkraise()
            self.var.set(1)
        else:
            messagebox.showinfo("Error", "please write the Cvs directory or job description")

    def show_CVs(self, name):
        frame = self.frames[name]
        frame.tkraise()
        frame.DrawWindow(self.List)

    def show_StartPage(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def GetResumes(self,List):
        self.List=List

class StartPage(tk.Frame): 
   def __init__(self, parent, controller):
       StartPage.__instance = self
       tk.Frame.__init__(self, parent)
       #BackgroungImage = ImageTk.PhotoImage(file="technology_resume-100690687-large.jpg")
       #self.BackgroundLabel= Label(window,image=BackgroungImage)
       #self.BackgroundLabel.photo=BackgroungImage
       #self.BackgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)
       self.DicLabel= Label(self,text="Enter CVs Directory",font=("Arial",14))
       self.DicLabel.grid(column=0,row=0)
       self.DirTxt= Entry(self,width=55);
       self.DirTxt.place(x=0,y=30);
       self.DirTxt.focus()
       self.BrowseBtn= Button(self,text="Browse",command=self.Browse)
       self.BrowseBtn.place(x=350,y=30)
       self.JobLabel= Label(self,text="Enter Your Job Description",font=("Arial",14))
       self.JobLabel.place(x=0,y=50)
       self.JobDescription= Text(self,height=15,width=40,font=("Arial",12))
       self.JobDescription.place(x=0,y=80)
       self.StartBtn= Button(self,text="Start Scanning",fg="blue",width=30,font=28,command=lambda : controller.show_ScanningPage(ScanningGUI))
       self.StartBtn.place(x=80,y=400)
            
   def Browse(self):
        print("Browse Button is Clicked")
        self.DirTxt.delete(0,'end')
        Dir=tk.filedialog.askdirectory()
        self.DirTxt.insert(0,Dir) #index???

class ScanningGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        BackgroungImage = ImageTk.PhotoImage(file="CTA_scan_your_resume-03-02.png")
        self.BackgroundLabel = Label(self, image=BackgroungImage)
        self.BackgroundLabel.photo=BackgroungImage
        self.BackgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)
        self.BackgroundLabel.bind('<Configure>', self.resize_image)
        self.FinishBtn= Button(self,text="Finish",fg="blue",width=10,font=28,command=lambda : controller.show_CVs(CVsView))
        self.FinishBtn.place(x=165,y=425)
        self.FinishBtn.config(state="disable")
       
    def resize_image(self,event):
        new_width = event.width
        new_height = event.height
        image3=Image.open('CTA_scan_your_resume-03-02.png')
        image = image3.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(image)
        self.BackgroundLabel.config(image = photo)
        self.BackgroundLabel = photo #avoid garbage collection

class CVsView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

    def DrawWindow(self,ResumeList):
       self.CreateUI()
       self.LoadTable(ResumeList)
       self.treeview.grid(sticky = (N,S,W,E))
       self.grid_rowconfigure(0, weight = 1)
       self.grid_columnconfigure(0, weight = 1)

    def CreateUI(self):
        tv = Treeview(self)
        tv['columns'] = ('rank')
        tv.heading("#0", text='Sources', anchor='w')
        tv.column("#0", anchor="w")
        tv.heading('rank', text='Rank')
        tv.column('rank', anchor='center', width=100)
        tv.grid(sticky = (N,S,W,E))
        self.treeview = tv
        self.treeview.grid_rowconfigure(0, weight = 1)
        self.treeview.grid_columnconfigure(0, weight = 1)

    def LoadTable(self,ResumeList):
        for tuples in ResumeList:
            self.treeview.insert('', 'end', text=tuples[0], values=(tuples[1]))
