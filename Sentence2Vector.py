from functions import create_embedding_matrix
import numpy as np


Example="Cairo University Faculty of Engineering"
sentence_size= len(Example.split())
Example[1]
from keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer(num_words=30)
tokenizer.fit_on_texts(Example.split())
X_train = tokenizer.texts_to_sequences(Example.split())
embedding_dim = 300
embedding_matrix = create_embedding_matrix('A:\College\Graduation Project\Project\glove.42B.300d.txt',tokenizer.word_index, embedding_dim)
vector=embedding_matrix.sum(axis=0)
rms = np.sqrt(np.mean(vector**2))
sentence_vector = vector/rms

Example2= "Cairo University of Engineering"


Example[1]
from keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer(num_words=30)
tokenizer.fit_on_texts(Example2.split())
embedding_dim = 300
embedding_matrix2 = create_embedding_matrix('A:\College\Graduation Project\Project\glove.42B.300d.txt',tokenizer.word_index, embedding_dim)
vector=embedding_matrix2.sum(axis=0)
rms = np.sqrt(np.mean(vector**2))
sentence_vector2 = vector/rms





print(cosine_similarity_measure([2,3,4],[2,3,4])) # equal 1.0

print(10*cosine_similarity_measure(sentence_vector,sentence_vector2))






