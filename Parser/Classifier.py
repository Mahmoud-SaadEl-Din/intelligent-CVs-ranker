from sklearn.externals import joblib
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import gensim
import json
import re
import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords,wordnet
from keras.preprocessing.text import Tokenizer
import pickle
import math

class Classifier:
    def __init__(self):
        self.tokenizer=joblib.load("Parser\\Tokenizer.sav")
        self.model=joblib.load("Parser\\W2V_ANN.sav")
#        self.glove = pickle.load( open( "glove.840B.300d.pkl", "rb" ) )  
        self.w2v_model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)  
        
#    def create_embedding_matrixV2(self, word_index, embedding_dim):
#        vocab_size = len(word_index) + 1  # Adding again 1 because of reserved 0 index
#        embedding_matrix = np.zeros((vocab_size, embedding_dim))
#        for word in word_index:
#            if word in self.glove:
#                vector=self.glove.get(word,'none')
#                idx = word_index[word] 
#                embedding_matrix[idx] = np.array(vector, dtype=np.float32)[:embedding_dim]
#        return embedding_matrix
#        
#        
#    def create_embedding_matrix(self,filepath, word_index, embedding_dim):
#        vocab_size = len(word_index) + 1  # Adding again 1 because of reserved 0 index
#        embedding_matrix = np.zeros((vocab_size, embedding_dim))
#    
#        f = open(filepath, encoding="utf8")
#        for line in f:
#            word, *vector = line.split()
#            if word in word_index:
#                idx = word_index[word] 
#                embedding_matrix[idx] = np.array(vector, dtype=np.float32)[:embedding_dim]
#        return embedding_matrix       
    
#    def sentence2vec(self,sentence):
#        sentence = self.TextPreprocessing(sentence)
#        tokenizer = Tokenizer(num_words=30)
#        tokenizer.fit_on_texts(sentence.split())
#        embedding_dim = 300
#        #embedding_matrix2 = self.create_embedding_matrix('glove.42B.300d.txt',tokenizer.word_index, embedding_dim)
#        embedding_matrix2 = self.create_embedding_matrixV2(tokenizer.word_index, embedding_dim)
#        vector=embedding_matrix2.sum(axis=0)
#        rms = np.sqrt(np.mean(vector**2))
#        sentence_vector = vector/rms
#        return sentence_vector
    def sentence2vec(self,sent):
        vector_dim=300
        sent=sent.split()
        sent_vec = np.zeros(vector_dim)
        numw = 0
        for w in sent:
            try:
                vc=self.w2v_model[w]
                vc=vc[0:vector_dim]
                
                sent_vec = np.add(sent_vec, vc) 
                numw+=1
            except:
                pass
        return sent_vec / np.sqrt(sent_vec.dot(sent_vec))



    def ClassifySentenceList(self,sentence_list,filename,type=0):
        courses,others,education,faculty,grade,project,techskills,personalskills,language,experience = ([] for i in range(10))
        courses_vec,others_vec,education_vec,faculty_vec,grade_vec,project_vec,techskills_vec,personalskills_vec,language_vec,experience_vec = ([] for i in range(10))
        labels={0:courses,1:education,2:experience,3:faculty,4:grade,5:language,6:others,7:personalskills
            ,8:project,9:techskills}
        labels_vec={0:courses_vec,1:education_vec,2:experience_vec,3:faculty_vec,4:grade_vec,5:language_vec,6:others_vec,7:personalskills_vec
            ,8:project_vec,9:techskills_vec}
        for sentence in sentence_list:
            sentence2classify = self.TextPreprocessing(sentence)
            print(sentence)
            sx=[]
            sx.append(sentence2classify)
            x=self.tokenizer.texts_to_sequences(sx)
            x = pad_sequences(x, padding='post', maxlen=100)
            y_pred = self.model.predict(x)
            y_pred=(y_pred == y_pred.max(axis=1)[:,None]).astype(int)
            key=y_pred[0].argmax(axis=0)
            print(key)
            sentence_vec=self.sentence2vec(sentence2classify)
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
                
        if type==0:
            with open('InterStorage\\'+filename+'.txt', 'w') as outfile:
                json.dump(data, outfile)
            with open('InterStorage_vec\\'+filename+'.txt', 'w') as outfile:
                json.dump(data_vec, outfile)
                #print(y_pred_2)
        else:
            with open('JobDescription\\'+filename+'.txt', 'w') as outfile:
                json.dump(data, outfile)
            with open('JobDescription\\'+filename+'_vec.txt', 'w') as outfile:
                json.dump(data_vec, outfile)
                #print(y_pred_2)
                #print(y_pred_2)
            

    def TextPreprocessing(self,text):
        REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
        BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
        STOPWORDS = set(stopwords.words('english'))
        text = text.lower() # lowercase text
        text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text. substitute the matched string in REPLACE_BY_SPACE_RE with space.
        text = BAD_SYMBOLS_RE.sub('', text) # remove symbols which are in BAD_SYMBOLS_RE from text. substitute the matched string in BAD_SYMBOLS_RE with nothing. 
        text = ' '.join(word for word in text.split() if word not in STOPWORDS) # remove stopwors from text
        lemmatizer = WordNetLemmatizer()
        text=' '.join([lemmatizer.lemmatize(w, self.get_wordnet_pos(w)) for w in nltk.word_tokenize(text)])
        return text
    
    def get_wordnet_pos(self,word):
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        
        return tag_dict.get(tag, wordnet.NOUN)
        