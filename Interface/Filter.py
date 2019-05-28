import sys

class Filter:

    def FilterFiles(self,filesDic,filesList):
        return list(filesDic.difference(filesList))

