""" # parsing the docx file
import time
import docx
start_time = time.time()
doc = docx.Document('Mahmoud Saad.docx')
fullText = []
title_data = []
internal_list =[]
extra_list =[]
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
print("--- %s seconds ---" % (time.time() - start_time))

for path in fullText:
    print(path.encode("utf-8"))
for lists in title_data:
    print(lists)
print(extra_list) """




