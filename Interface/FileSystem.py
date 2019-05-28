from os import listdir
from os.path import join,isfile
import os

class fileSystem:
    def GetFiles(self,CvsDir):
        OnlyFiles=[]
        for f in listdir(CvsDir):
            if isfile(join(CvsDir,f)):
                OnlyFiles.append(os.path.splitext(f)[0])
        return OnlyFiles
    def GetFiles_withext(self,CvsDir):
        OnlyFiles=[]
        for f in listdir(CvsDir):
            if isfile(join(CvsDir,f)):
                OnlyFiles.append(f)
        return OnlyFiles