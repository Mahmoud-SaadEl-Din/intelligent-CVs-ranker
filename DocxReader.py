# scanning the docx file
import re
import time
import docx

sentences_list = []
time_to_scan = 0

def scan_docx(file_name):
    global sentences_list
    global time_to_scan
    start_time = time.time()
    doc = docx.Document(file_name)
    for para in doc.paragraphs:
        if para.text != "" :
            data2 = re.sub(r'[^A-Za-z0-9.+\\]',' ',para.text)
            sentences_list.append(data2)
    time_to_scan = time.time() - start_time
    print("---it took %s seconds to scan the docx ---" % time_to_scan )


def get_sentence_list():
    global sentences_list
    return sentences_list

def get_reading_time():
    global time_to_scan
    return time_to_scan