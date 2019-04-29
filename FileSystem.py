from os import listdir
from os.path import join,isfile

class fileSystem:
    def GetFiles(self,CvsDir):
        OnlyFiles = [f for f in listdir(CvsDir) if isfile(join(CvsDir,f))]
        return OnlyFiles
