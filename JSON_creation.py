#############################################################################

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