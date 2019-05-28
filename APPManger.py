from Interface.GUI import GUI
from Interface.FileSystem import fileSystem
from Interface.GUI import ScanningGUI
from Interface.GUI import StartPage
from Ranker.ranking_class import Ranker

from Parser.Scanner import Scanner
from Parser.Classifier import Classifier
import json
from os.path import join,isfile
import tkinter
from Interface import Filter
from Interface.PragraphsPreprocessing import paragraphPreprocessing
import operator

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
         self.Splitter=paragraphPreprocessing()
         self.Ranker=Ranker()
         self.Scanner=Scanner()
         self.Classifier=Classifier()
    def StartProgram(self):
        List=[]
        self.app=GUI.getInstance()
        print("waiting for inputs.............")
        self.app.frames[StartPage].StartBtn.wait_variable(self.app.var)
        print("Inputs Taken")
        
        if(self.app.frames[StartPage].CheckVar.get()==1):
            self.Grade=True
            self.ChosenGrade= self.app.frames[StartPage].ComboBox.get()
            print(self.ChosenGrade)
        else:
            self.ChosenGrade="Fair"
        self.CVsFiles= self.FileSys.GetFiles_withext(self.app.CvsDir)
        self.JobDescription=self.Splitter.sentenceSplitter(self.app.JobDes)
        self.Classifier.ClassifySentenceList(self.JobDescription,"JobDescription",1)
        self.ParsedFiles= self.FileSys.GetFiles(r"InterStorage_vec")
        self.FilteredFiles=self.FilterObj.FilterFiles(set(self.CVsFiles),set(self.ParsedFiles))
        for file in self.FilteredFiles:
            lines=[]
            lines = self.Scanner.scan_docx(join(self.app.CvsDir,file))
            print("------------------------------------------------------------------------------------------")
            print(lines)
            yassora = open("testo.txt",'w')
            for line in lines:
                yassora.write(line)
                yassora.write("\n")
            yassora.close()
            print("------------------------------------------------------------------------------------------")
            self.Classifier.ClassifySentenceList(lines,file)
        self.ParsedFiles= self.FileSys.GetFiles(r"InterStorage_vec")
        for file in  self.ParsedFiles:
            with open(join('InterStorage',file+'.txt')) as json_file:  
                data = json.load(json_file)
            grade=data['grade']
            if file !="JobDescription":
                output=self.Ranker.ResumeRank(join('InterStorage_vec',file+'.txt'),"JobDescription\JobDescription_vec.txt",grade,self.ChosenGrade)
#                TotalScore= output[0]
#                CategoriesScoreList = output[1]
#                print(file,CategoriesScoreList)
                t1=(file,output)
                print(t1[1])
                print(type(t1[1]))
                List.append(t1)
        print(self.JobDescription)
        print(self.app.CvsDir)
        print(self.CVsFiles)
        print(self.ParsedFiles)
        print( self.FilteredFiles)
        self.ScanScreen= self.app.frames[ScanningGUI]
        divisions=10
        print("/////////////////////////////////////////////")
        print(List[0])
        print("/////////////////////////////////////////////")
        List.sort(key=lambda x:x[1],reverse=True)
#        List = List.sort(key=operator.itemgetter(1))
        for i in range(divisions):
            self.ScanScreen.currentValue=self.ScanScreen.currentValue+10
            self.ScanScreen.style.configure('text.Horizontal.TProgressbar', 
                    text='{:g} %'.format(self.ScanScreen.currentValue))
            self.ScanScreen.progressbar.after(500, self.ScanScreen.progress(self.ScanScreen.currentValue))
            self.ScanScreen.progressbar.update() # Force an update of the GUI
        self.ScanScreen.FinishBtn.config(state="normal")
        self.app.GetResumes(List)
        self.app.mainloop()


