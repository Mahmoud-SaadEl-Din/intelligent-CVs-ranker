# scanning the docx file
import time
import docx

fullText = [] # headings in the docx
title_data = [] # list of list of string (string is paragraph in the heading).. 
                #for example fullText[0] is the first Heading & title_data[0] is list contains fullText[0] internal statment
internal_list =[] # used in code
extra_list =[] # contains non-categorized data
time_to_scan = 0

def scan_docx(file_name):
    global fullText
    global title_data
    global internal_list
    global extra_list
    global time_to_scan
    start_time = time.time()
    doc = docx.Document(file_name)
    inside_heading = False
    for para in doc.paragraphs:
        if para.style.name == "Heading 1":
            fullText.append(para.text)
            if inside_heading == True:
                title_data.append(internal_list)
                #internal_list.clear()  
                internal_list = []
            inside_heading = True
        else:
            if inside_heading == True:
                internal_list.append(para.text)
            else:
                extra_list.append(para.text)
    title_data.append(internal_list)
    time_to_scan = time.time() - start_time
    print("---it took %s seconds to scan the docx ---" % time_to_scan )


def print_docx_heading():
    for path in fullText:
        print(path.encode("utf-8"))

def print_docx_heading_data():
    for lists in title_data:
        print(lists)

def print_uncategorized_data_in_docx():
    print(extra_list)

def get_heading_list():
    return fullText

def get_heading_internal_data():
    return title_data

def get_uncategorized_data():
    return extra_list

def get_scanning_time():
    return time_to_scan
