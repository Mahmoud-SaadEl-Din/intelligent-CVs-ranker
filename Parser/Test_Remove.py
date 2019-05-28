from sklearn.externals import joblib
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import json
from keras.preprocessing.text import Tokenizer
import pickle
import math
glove = pickle.load( open( "glove.840B.300d.pkl", "rb" ) )  

def create_embedding_matrix(self,filepath, word_index, embedding_dim):
        vocab_size = len(word_index) + 1  # Adding again 1 because of reserved 0 index
        embedding_matrix = np.zeros((vocab_size, embedding_dim))
    
        f = open(filepath, encoding="utf8")
        for line in f:
            word, *vector = line.split()
            if word in word_index:
                idx = word_index[word] 
                embedding_matrix[idx] = np.array(vector, dtype=np.float32)[:embedding_dim]
        return embedding_matrix       

def create_embedding_matrixV2(self, word_index, embedding_dim):
        vocab_size = len(word_index) + 1  # Adding again 1 because of reserved 0 index
        embedding_matrix = np.zeros((vocab_size, embedding_dim))
        for word in word_index:
            if word in glove:
                vector=glove.get(word,'none')
                idx = word_index[word] 
                embedding_matrix[idx] = np.array(vector, dtype=np.float32)[:embedding_dim]
        return embedding_matrix
                
        
 def sentence2vec(self,sentence):
        tokenizer = Tokenizer(num_words=30)
        tokenizer.fit_on_texts(sentence.split())
        embedding_dim = 300
        embedding_matrix2 = self.create_embedding_matrixV2(tokenizer.word_index, embedding_dim)
        vector=embedding_matrix2.sum(axis=0)
        rms = np.sqrt(np.mean(vector**2))
        sentence_vector = vector/rms
        return sentence_vector
    
tokenizer = Tokenizer(num_words=30)
tokenizer.fit_on_texts("The dog ate the cat".split())
word_index= tokenizer.word_index
vocab_size = len(word_index) + 1  # Adding again 1 because of reserved 0 index
embedding_matrix = np.zeros((vocab_size, 200))
for word in word_index:
    if word in glove:
        vector=glove.get(word,'none')
        idx = word_index[word] 
        embedding_matrix[idx] = np.array(vector, dtype=np.float32)[:200]
