import json

from os import listdir
from os.path import join,isfile
from functions import cosine_similarity_measure

indexed_string = ["courses","education","others","faculty","grade","project","techskills","personalskills","language","experience"]


def resume_rank(resume_file_name,job_description_name):
    resume_file=open(resume_file_name, "r")
    job_description_file=open(job_description_name, "r")
    sentence_count =0
    if resume_file.mode == 'r':
        contents =resume_file.read()
        parsed_json_resume = json.loads(contents)
        #print(parsed_json["education"])

    if job_description_file.mode == 'r':
        contents =job_description_file.read()
        parsed_json_job = json.loads(contents)
        
    max_global_similarity = 0
    for idx, val in enumerate(indexed_string):
        data_arr_in_resume = parsed_json_resume[val]
        data_arr_in_job = parsed_json_job[val]
        #for resume_arr_val in enumerate(data_arr_in_resume):
        #        if resume_arr_val[0] != "NAN" :
        #            sentence_count+=1
        sentence_count+=len(data_arr_in_resume)
        print(sentence_count)
        for job_arr_index, job_arr_val in enumerate(data_arr_in_job):
            max_local_similarity = 0
            job_sentence = job_arr_val
            for resume_arr_index, resume_arr_val in enumerate(data_arr_in_resume):
                max_local_similarity = max(max_local_similarity,cosine_similarity_measure(resume_arr_val,job_sentence))
            
            max_global_similarity+= (max_local_similarity*10)
    return max_global_similarity/sentence_count



def read_parsed_files(files_dir):
    onlyfiles = [f for f in listdir(files_dir ) if isfile(join(files_dir , f))]
    print(onlyfiles)
    ranks=[]
    for file in onlyfiles:
       ranks.append(resume_rank("InterStorage_vec\\"+file,"A:\\Desktop\intelligent-CVs-ranker-gui_branch\\InterStorage_vec\\JobDescription.txt"))
    return ranks
    
rank=read_parsed_files("InterStorage_vec")