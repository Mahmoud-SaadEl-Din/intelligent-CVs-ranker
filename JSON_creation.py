#############################################################################

# creating JSON objects for each Heading 1
import json
stuctured_format_titles = []
stuctured_format_titles_bodies = []
JSON_list = []
JSON_object = {}
def set_JSON_title(titles):
    global stuctured_format_titles
    stuctured_format_titles = titles

def set_JSON_bodies(bodies):
    global stuctured_format_titles_bodies
    stuctured_format_titles_bodies = bodies


def build_JSON_parts():
    global stuctured_format_titles
    global stuctured_format_titles_bodies
    global JSON_list
    for j in range(len(stuctured_format_titles)):
        x=""
        x += "\""+stuctured_format_titles[j]+"\"" + ": ["
        for i in range(len(stuctured_format_titles_bodies[j])):
            x+="\""+stuctured_format_titles_bodies[j][i]+"\""
            if i != len(stuctured_format_titles_bodies[j])-1:
                x+=","
        x+="]"
        JSON_list.append(x)


def finalize_JSON():
    global JSON_list
    global JSON_object
    y = "{ "
    for i in range(len(JSON_list)):
        y+= JSON_list[i]
        if i != len(JSON_list)-1:
            y+="," 
    y+=" }"    
    d = json.loads(y)
    JSON_object = d