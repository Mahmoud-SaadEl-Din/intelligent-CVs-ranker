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

#################################################################################

# creating JSON objects for each Heading 1
import json
stuctured_format = ["Honors","Education","Experience","Projects","Skills"]
JSON_list = []

for j in range(len(stuctured_format)):
    x=""
    x += "\""+stuctured_format[j]+"\"" + ": ["
    for i in range(len(stuctured_format)):
        x+="\""+stuctured_format[i]+"\""
        if i != len(stuctured_format)-1:
            x+=","
    x+="]"
    # if j != len(stuctured_format)-1:
    #      x+=", "
    JSON_list.append(x)

#d = json.loads(y)
#print(d)
#print(json.dumps(y))
#print(d.get("Skills"))
#print(JSON_list[0])


################################################################################

# Create big JSON object
y = "{ " + JSON_list[0] + ", "+ JSON_list[1] + ", "+ JSON_list[2] + ", "+ JSON_list[3] + ", "+ JSON_list[4] +" }"

#print(y)
d = json.loads(y)
print(json.dumps(d, indent=4, sort_keys=True))