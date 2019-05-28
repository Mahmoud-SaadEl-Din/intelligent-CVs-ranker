import re
import time
import docx

class Scanner:
    def __init__(self):
        self.sentences_list = []
        self.time_to_scan = 0
    
    def scan_docx(self,file_name):
        
        start_time = time.time()
        doc = docx.Document(file_name)
        for para in doc.paragraphs:
            if para.text != "" :
                data2 = re.sub(r'[^A-Za-z0-9.+\\]',' ',para.text)
                self.sentences_list.append(data2)
        self.time_to_scan = time.time() - start_time
        print("---it took %s seconds to scan the docx ---" % self.time_to_scan )
        MySentences=self.get_sentence_list()
        self.sentences_list=[]
        return MySentences
        
        
    def get_sentence_list(self):
        return self.sentences_list
    
    def get_reading_time(self):
        return self.time_to_scan
    