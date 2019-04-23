import json
import cosine_similarity as similarity_measure

indexed_string = ["courses","education","others","faculty","grade","project","techskills","personalskills","language","experience"]


def resume_rank(resume_file_name,job_description_name):
    resume_file=open(resume_file_name, "r")
    job_description_file=open(job_description_name, "r")

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
        for resume_arr_index, resume_arr_val in enumerate(data_arr_in_resume):
            max_local_similarity = 0
            resume_sentence = resume_arr_val
            for job_arr_index, job_arr_val in enumerate(data_arr_in_job):
                max_local_similarity = max(max_local_similarity,similarity_measure.cosine_similarity_measure(job_arr_val,resume_sentence))
            max_global_similarity+= max_local_similarity
    return max_global_similarity




    