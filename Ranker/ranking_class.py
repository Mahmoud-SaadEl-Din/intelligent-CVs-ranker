import math
import json
from Ranker.GradeFilter import gradeFilter
import numpy as np
from numpy.linalg import norm
class Ranker:

    indexed_string = ["courses","education","faculty","grade","project","techskills","personalskills","language","experience"]
    
    
    def __init__(self):
        self.Filter=gradeFilter()


    def cosine_similarity_measure(self,vectorization1,vectorization2):
        vector_dim=300
        NVI=norm(vectorization1)
        NVJ=norm(vectorization2)

        dotVij =0
        NVI=0
        for x in range(vector_dim):
            NVI=NVI +  vectorization1[x] * vectorization1[x]

        NVJ=0
        for x in range(vector_dim):
            NVJ=NVJ +  vectorization2[x] * vectorization2[x]

        for x in range(vector_dim):
            dotVij = dotVij + vectorization1[x] * vectorization2[x]
        return (dotVij / (NVI*NVJ))
#        sum_x_squared, sum_x_y, sum_y_squared = 0, 0, 0
#        for i in range(len(vectorization1)): # both have the same length
#            x = vectorization1[i]; y = vectorization2[i]
#            sum_x_squared += x*x
#            sum_y_squared += y*y
#            sum_x_y += x*y
#        return sum_x_y/math.sqrt(sum_x_squared*sum_y_squared)

    def find_weakness(self,resume_score,job_description_score,confident_value):
        weakness_list = []
        for idx, val in enumerate(resume_score):
            if  (job_description_score[idx] != 0) and ((resume_score[idx] / job_description_score[idx]) < confident_value) : 
                weak_msg = "You are weak in category " + str(self.indexed_string[idx]) + " with score :" + str(resume_score[idx]) +" /" + str(job_description_score[idx])
                weakness_list.append(weak_msg)   
        return weakness_list


    def resume_rank(self,resume_file_name,job_description_name):
        resume_file=open(resume_file_name, "r")
        job_description_file=open(job_description_name, "r")
        categories_score_list = [] # the contribution of each category in the final score
        categories_score_max_job =[] # MAX score can resume get in the Category score (each statment scaled from 10)
        categories_score_max_resume =[] # The score get by resume (each statment scaled from 10)
        weakness_list =[]
        sentence_count =0
        if resume_file.mode == 'r':
            contents =resume_file.read()
            parsed_json_resume = json.loads(contents)
            #print(parsed_json["education"])

        if job_description_file.mode == 'r':
            contents =job_description_file.read()
            parsed_json_job = json.loads(contents)
            
        for idx, val in enumerate(self.indexed_string):
            data_arr_in_job = parsed_json_job[val]
            data_arr_in_resume = parsed_json_resume[val]
            sentence_count+=len(data_arr_in_job)
            categories_score_max_job.append(len(data_arr_in_job)*10)
            
        max_global_similarity = 0
        for idx, val in enumerate(self.indexed_string):
            data_arr_in_resume = parsed_json_resume[val]
            data_arr_in_job = parsed_json_job[val]
            
            category_score = 0
            for job_arr_index, job_arr_val in enumerate(data_arr_in_job):
                max_local_similarity = 0
                job_sentence = job_arr_val
                for resume_arr_index, resume_arr_val in enumerate(data_arr_in_resume):
                    max_local_similarity = max(max_local_similarity,self.cosine_similarity_measure(resume_arr_val,job_sentence))
                    print("Category:",self.indexed_string[idx]," _Job description:",job_arr_index,"with ", resume_arr_index," _with score: ", self.cosine_similarity_measure(resume_arr_val,job_sentence))
                category_score += (max_local_similarity*10)
                max_global_similarity += (max_local_similarity*10)
            categories_score_list.append(category_score/sentence_count)
            categories_score_max_resume.append(category_score)
        weakness_list = self.find_weakness(categories_score_max_resume,categories_score_max_job,0.5)
        return [(max_global_similarity/sentence_count), categories_score_list,categories_score_max_resume ,categories_score_max_job,weakness_list]


    def GradeCalc(self,sentence,JobSentence):
        dic={"Excellent":4,"Very Good":3,"Good":2,"Pass":1,"Fair":0}
        self.grade=self.Filter.GradeTranform(sentence)
        print("-----------------------------------------------------------------------------------")
        print(sentence)
        print(self.grade)
        print("-----------------------------------------------------------------------------------")
        self.sentenceGrade=dic[self.grade]
        self.jobGrade=dic[JobSentence]
        
        if(self.sentenceGrade<self.jobGrade):
            return 0
        else:
            return (self.sentenceGrade+10)*(10/14)
    
    def ResumeRank(self,resume_file_name,job_description_name,sentence,JobSentence):
        rank1=self.resume_rank(resume_file_name,job_description_name)
        rank2=self. GradeCalc(sentence,JobSentence)
        indexed_string = ["courses","education","faculty","grade","project","techskills","personalskills","language","experience"]
        print( "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$" )
        print(rank1[1])
        rr= np.array(rank1[1])
        print(np.sum(rr))
        print(rank1[0])
        for idx, val in enumerate(rank1[1]):
            print("Score of category : ", indexed_string[idx], "with score :" , rank1[2][idx] , "with max : " , rank1[3][idx])
        print(rank1[4])
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
#        return round((rank1[0]+rank2)/2)
        return round(rank1[0])
        
        

