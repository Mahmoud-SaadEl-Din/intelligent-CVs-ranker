from GUI import GUI
from FileSystem import fileSystem
from GUI import ScanningGUI
from GUI import StartPage
import tkinter
import Filter
from PragraphsPreprocessing import paragraphPreprocessing

class AppManger:
    __instance = None

    @staticmethod 
    def getInstance():
      if AppManger.__instance == None:
        AppManger()
      return AppManger.__instance

    def __init__(self):
        if AppManger.__instance != None:
         raise Exception("AppManger class is a singleton!")
        else:
         AppManger.__instance = self
         self.FileSys=fileSystem()
         self.FilterObj= Filter.Filter()
         self.splitter=paragraphPreprocessing()
         

    def StartProgram(self):
        self.app=GUI.getInstance()
        print("waiting for inputs.............")
        self.app.frames[StartPage].StartBtn.wait_variable(self.app.var)
        print("Inputs Taken")
        self.CVsFiles= self.FileSys.GetFiles(self.app.CvsDir)
        self.JobDescription=self.splitter.sentenceSplitter(self.app.JobDes)
        self.ParsedFiles= self.FileSys.GetFiles(r"C:\Users\tarek\source\repos\PythonApplication5\PythonApplication5\Test Folder")
        self.FilteredFiles=self.FilterObj.FilterFiles(set(self.CVsFiles),set(self.ParsedFiles))
        print(self.JobDescription)
        print(self.app.CvsDir)
        print( self.FilteredFiles)
        List=[]
        t1=("Resume1","2.4")
        t2=("Resume2","9.5")
        List.append(t1)
        List.append(t2)
        self.ScanScreen= self.app.frames[ScanningGUI]
        divisions=10
        for i in range(divisions):
            self.ScanScreen.currentValue=self.ScanScreen.currentValue+10
            self.ScanScreen.style.configure('text.Horizontal.TProgressbar', 
                    text='{:g} %'.format(self.ScanScreen.currentValue))
            self.ScanScreen.progressbar.after(500, self.ScanScreen.progress(self.ScanScreen.currentValue))
            self.ScanScreen.progressbar.update() # Force an update of the GUI
        self.ScanScreen.FinishBtn.config(state="normal")
        self.app.GetResumes(List)
        self.app.mainloop()


