from GUI import GUI
from FileSystem import fileSystem
from GUI import ScanningGUI
import tkinter

class AppManger:
    __instance = None

    @staticmethod 
    def getInstance():
      if AppManger.__instance == None:
        AppManger()
      return AppManger.__instance

    def __init__(self):
        if AppManger.__instance != None:
         raise Exception("This class is a singleton!")
        else:
         AppManger.__instance = self
        self.FileSys=fileSystem()

    def StartProgram(self):
        app= GUI.getInstance();
        app.mainloop()

    def StartScanning(self,JobDescription,Dir):
        self.Files=self.FileSys.GetFiles(Dir)
        print(JobDescription)
        print(Dir)
        print(self.Files)
        List=[]
        t1=("Resume1","2.4")
        t2=("Resume2","9.5")
        List.append(t1)
        List.append(t2)
        self.gui=GUI.getInstance()
        self.ScanScreen= self.gui.frames[ScanningGUI]
        self.ScanScreen.FinishBtn.config(state="normal")
        self.gui.GetResumes(List)

