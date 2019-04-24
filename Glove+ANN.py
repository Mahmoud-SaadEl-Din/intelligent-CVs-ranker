import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from functions import create_embedding_matrix
dataset_train=pd.read_csv('AnotherDataset.csv')
training_set = dataset_train.iloc[:,1:2]
y = dataset_train.iloc[:,2:3]
sentences_train =[]
for i in range(len(training_set)):
    sentences_train.append(training_set[i:i+1].values[0,0])


from sklearn.preprocessing import LabelBinarizer
encoder = LabelBinarizer()
transfomed_label = encoder.fit_transform(y)


from sklearn.model_selection import train_test_split
Xsentence_train, Xsentence_test, y_train, y_test = train_test_split(sentences_train, transfomed_label, test_size=0.15, shuffle=True,random_state=10)

from keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(Xsentence_train)
from sklearn.externals import joblib
filename = 'Tokenizer.sav'
joblib.dump(tokenizer, filename)
X_train = tokenizer.texts_to_sequences(Xsentence_train)
X_test = tokenizer.texts_to_sequences(Xsentence_test)
vocab_size = len(tokenizer.word_index) + 1 


    
from keras.preprocessing.sequence import pad_sequences
maxlen = 100
X_train = pad_sequences(X_train, padding='post', maxlen=maxlen)
X_test = pad_sequences(X_test, padding='post', maxlen=maxlen)


embedding_dim = 300
embedding_matrix = create_embedding_matrix('A:\College\Graduation Project\Project\glove.42B.300d.txt',tokenizer.word_index, embedding_dim)

nonzero_elements = np.count_nonzero(np.count_nonzero(embedding_matrix, axis=1))
nonzero_elements / vocab_size




from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Flatten, LSTM, Conv1D, MaxPooling1D, Dropout, Activation
from keras.layers.embeddings import Embedding



from keras.models import Sequential
from keras import layers
from keras.optimizers import SGD


#model = Sequential()
#model.add(layers.Embedding(vocab_size, embedding_dim, input_length=maxlen))
#model.add(layers.Conv1D(128, 5, activation='relu'))
#model.add(layers.GlobalMaxPooling1D())
#model.add(layers.Dense(10, activation='relu'))
#model.add(layers.Dense(10, activation='softmax'))
#model.compile(optimizer='adam',
 #             loss='categorical_crossentropy',
  #            metrics=['accuracy'])
#model.summary()
model = Sequential()
model.add(layers.Embedding(vocab_size, embedding_dim, 
                           weights=[embedding_matrix], 
                           input_length=maxlen, 
                           trainable=True))
model.add(layers.GlobalMaxPool1D())
model.add(layers.Dense(149, activation='relu'))
#model.add(layers.Dense(149, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))
sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=['accuracy'])

model.summary()
  #sotek mesh bayn 5als
model.fit(X_train, y_train,
                    epochs=30,
                    verbose=True,
                    validation_data=(X_test, y_test),
                    batch_size=100)
loss, accuracy = model.evaluate(X_train, y_train, verbose=False)
print("Training Accuracy: {:.4f}".format(accuracy))
loss, accuracy = model.evaluate(X_test, y_test, verbose=False)
print("Testing Accuracy:  {:.4f}".format(accuracy))
from sklearn.metrics import accuracy_score
y_pred = model.predict(X_test)
y_pred=(y_pred == y_pred.max(axis=1)[:,None]).astype(int)

print("sklearn accuracy:",accuracy_score(y_test,y_pred))

filename = 'finalized_model.sav'
joblib.dump(model, filename)
testing=[]
testing.append("BSC")
X_test1 = tokenizer.texts_to_sequences(testing)
X_test1 = pad_sequences(X_test1, padding='post', maxlen=maxlen)
prediction=model.predict(X_test1)
print(prediction)