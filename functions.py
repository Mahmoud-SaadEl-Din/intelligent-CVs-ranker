import sys
import DocxReader as reader
import tkinter
import json
from tkinter import *
from os import listdir
from os.path import join,isfile
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk,Image
from sklearn.externals import joblib
import PythonApplication2 as pa2
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from keras.preprocessing.text import Tokenizer
import math






def cosine_similarity_measure(vectorization1,vectorization2):
    sum_x_squared, sum_x_y, sum_y_squared = 0, 0, 0
    for i in range(len(vectorization1)): # both have the same length
        x = vectorization1[i]; y = vectorization2[i]
        sum_x_squared += x*x
        sum_y_squared += y*y
        sum_x_y += x*y
    return sum_x_y/math.sqrt(sum_x_squared*sum_y_squared)
    

def create_embedding_matrix(filepath, word_index, embedding_dim):
    vocab_size = len(word_index) + 1  # Adding again 1 because of reserved 0 index
    embedding_matrix = np.zeros((vocab_size, embedding_dim))

    f = open(filepath, encoding="utf8")
    for line in f:
        word, *vector = line.split()
        if word in word_index:
            idx = word_index[word] 
            embedding_matrix[idx] = np.array(vector, dtype=np.float32)[:embedding_dim]

    return embedding_matrix

def sentence2vec(sentence):
    tokenizer = Tokenizer(num_words=30)
    tokenizer.fit_on_texts(sentence.split())
    embedding_dim = 300
    embedding_matrix2 = create_embedding_matrix('A:\College\Graduation Project\Project\glove.42B.300d.txt',tokenizer.word_index, embedding_dim)
    vector=embedding_matrix2.sum(axis=0)
    rms = np.sqrt(np.mean(vector**2))
    sentence_vector = vector/rms
    return sentence_vector

def ClassifySentenceList(sentence_list,filename):
    Tokenizer=joblib.load("Tokenizer.sav")
    classifier=joblib.load("finalized_model.sav")
    courses,others,education,faculty,grade,project,techskills,personalskills,language,experience = ([] for i in range(10))
    courses_vec,others_vec,education_vec,faculty_vec,grade_vec,project_vec,techskills_vec,personalskills_vec,language_vec,experience_vec = ([] for i in range(10))
    labels={0:courses,1:education,2:experience,3:faculty,4:grade,5:language,6:others,7:personalskills
        ,8:project,9:techskills}
    labels_vec={0:courses_vec,1:education_vec,2:experience_vec,3:faculty_vec,4:grade_vec,5:language_vec,6:others_vec,7:personalskills_vec
        ,8:project_vec,9:techskills_vec}
    for sentence in sentence_list:
        print(sentence)
        sx=[]
        sx.append(sentence)
        x=Tokenizer.texts_to_sequences(sx)
        x = pad_sequences(x, padding='post', maxlen=100)
        y_pred = classifier.predict(x)
        y_pred=(y_pred == y_pred.max(axis=1)[:,None]).astype(int)
        key=y_pred[0].argmax(axis=0)
        print(key)
        sentence_vec=sentence2vec(sentence)
        labels[key].append(sentence)
        labels_vec[key].append(sentence_vec.tolist())
        
    data={}
    data_vec={}
        
    data={
          'courses':courses,
          'education':education,
          'others':others,
          'faculty':faculty,
          'grade':grade,
          'project':project,
          'techskills':techskills,
          'personalskills':personalskills,
          'language':language,
          'experience':experience,
          }
    data_vec={
          'courses':courses_vec,
          'education':education_vec,
          'others':others_vec,
          'faculty':faculty_vec,
          'grade':grade_vec,
          'project':project_vec,
          'techskills':techskills_vec,
          'personalskills':personalskills_vec,
          'language':language_vec,
          'experience':experience_vec,
          }
    with open('InterStorage\\'+filename+'.txt', 'w') as outfile:
        json.dump(data, outfile)
    with open('InterStorage_vec\\'+filename+'.txt', 'w') as outfile:
        json.dump(data_vec, outfile)
        #print(y_pred_2)

def start_scanning(files,directory,bt3,job_specs):
    
    ClassifySentenceList(job_specs,"JobDescription")
    for file in files:
        if file.endswith(".docx"):
            reader.scan_docx(join(directory,file))
            #print(reader.get_sentence_list())
            ClassifySentenceList(reader.get_sentence_list(),file)
        elif file.endswith(".pdf"):
            pages = pa2.scan_pdf(join(directory,file))
            ClassifySentenceList(pages,file)
        print("\n")
    bt3.config(state="normal")

def pdf_reader(file):
    pdfFileObj = open(file, 'rb')
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
    print(pages)



