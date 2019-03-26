import PyPDF2
import sys

def scan_pdf(filename):
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    size=pdfReader.numPages
    pages=[]
    for i in range(0,size):
        pageObj = pdfReader.getPage(i)
        NewString=[]
        splitted_text=[]
        txt=[]
        NewString.append(pageObj.extractText())
        for i in NewString:
            splitted_text.append(i.split('\n'))
        txt=splitted_text[0]
        txt = [ elem for elem in txt if elem!=' ']
        pages=pages+txt
    return pages


