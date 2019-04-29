from GUI import GUI
from FileSystem import fileSystem
from GUI import ScanningGUI
import tkinter
import Filter

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
         self.FilterObj= Filter.Filter()

    def StartProgram(self):
        app= GUI.getInstance();
        app.mainloop()

    def StartScanning(self,JobDescription,Dir):
        self.CVsFiles=self.FileSys.GetFiles(Dir)
        self.ParsedFiles=self.FileSys.GetFiles(r"C:\Users\tarek\source\repos\PythonApplication5\PythonApplication5\Test Folder")
        self.FilteredFiles=self.FilterObj.FilterFiles(set(self.CVsFiles),set(self.ParsedFiles))
        print(JobDescription)
        print(Dir)
        print( self.FilteredFiles)
        List=[]
        t1=("Resume1","2.4")
        t2=("Resume2","9.5")
        List.append(t1)
        List.append(t2)
        self.gui=GUI.getInstance()
        self.ScanScreen= self.gui.frames[ScanningGUI]
        self.ScanScreen.FinishBtn.config(state="normal")
        self.gui.GetResumes(List)

