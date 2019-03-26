import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import functions as fn
import DocxReader as reader
import json
import re
dataset_train=pd.read_csv('Final-Dataset.csv').dropna()
training_set = dataset_train.iloc[:,0:1]
y = dataset_train.iloc[:,1:2]

sentences_train =[]
for i in range(len(training_set)):
    sentences_train.append(training_set[i:i+1].values[0,0])



from sklearn.preprocessing import LabelBinarizer
encoder = LabelBinarizer()
transfomed_label = encoder.fit_transform(y)
print(transfomed_label)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(training_set, transfomed_label, test_size=0.25, random_state=1000)

X_train_vec =[]
for i in range(len(X_train)):
    X_train_vec.append(X_train[i:i+1].values[0,0])
X_test_vec =[]
for i in range(len(X_test)):
    X_test_vec.append(X_test[i:i+1].values[0,0])
    
vectorizer = CountVectorizer()
vectorizer.fit(sentences_train)
X_train=vectorizer.transform(X_train_vec)
X_test=vectorizer.transform(X_test_vec)

import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
# Initialising the ANN
classifier = Sequential()

# Adding the input layer and the first hidden layer
classifier.add(Dense(units = 50, kernel_initializer = 'uniform', activation = 'relu', input_dim = 4865))
classifier.add(Dropout(0.2))

# Adding the second hidden layer
classifier.add(Dense(units = 50, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add(Dropout(0.2))

# Adding the output layer
classifier.add(Dense(units = 14, kernel_initializer = 'uniform', activation = 'softmax'))

# Compiling the ANN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Fitting the ANN to the Training set
classifier.fit(X_train, y_train, batch_size = 10, epochs = 10)
filename = 'finalized_model.sav'
joblib.dump(classifier, filename)
loss, accuracy = classifier.evaluate(X_test, y_test, verbose=False)
print("Testing Accuracy:  {:.4f}".format(accuracy))
y_pred = classifier.predict(X_test)
y_pred=(y_pred == y_pred.max(axis=1)[:,None]).astype(int)

print("sklearn accuracy:",accuracy_score(y_test,y_pred))

courses,volunteering,others,PHD,faculty,grade,project,techskills,personalskills,language,experience,masters,graduate,undergraduate = ([] for i in range(14))
labels={0:courses,1:volunteering,2:others,3:PHD,4:faculty,5:grade,6:project,7:techskills
        ,8:personalskills,9:language,10:experience,11:masters,12:graduate,13:undergraduate}
for i in range(0,1441):
    key=y_pred[i].argmax(axis=0)
    labels[key].append(X_test_vec[i])




import json

data={
      'courses':courses,
      'volunteering':volunteering,
      'others':others,
      'PHD':PHD,
      'faculty':faculty,
      'grade':grade,
      'project':project,
      'techskills':techskills,
      'personalskills':personalskills,
      'language':language,
      'experience':experience,
      'masters':masters,
      'graduate':graduate,
      'udergraduate':undergraduate
      }



with open('data.txt', 'w') as outfile:  
    json.dump(data, outfile)














###############################################################################################################################

def ClassifySentenceList(sentence_list,filename):
    courses,volunteering,others,PHD,faculty,grade,project,techskills,personalskills,language,experience,masters,graduate,undergraduate = ([] for i in range(14))
    labels={0:courses,1:volunteering,2:others,3:PHD,4:faculty,5:grade,6:project,7:techskills
            ,8:personalskills,9:language,10:experience,11:masters,12:graduate,13:undergraduate}
    for sentence in sentence_list:
        print(sentence)
        x=vectorizer.transform([sentence])
        y_pred = classifier.predict(x)
        y_pred=(y_pred == y_pred.max(axis=1)[:,None]).astype(int)
        key=y_pred[0].argmax(axis=0)
        labels[key].append(sentence)
        
    data={}
    data={
          'courses':courses,
          'volunteering':volunteering,
          'others':others,
          'PHD':PHD,
          'faculty':faculty,
          'grade':grade,
          'project':project,
          'techskills':techskills,
          'personalskills':personalskills,
          'language':language,
          'experience':experience,
          'masters':masters,
          'graduate':graduate,
          'udergraduate':undergraduate
          }
    with open('InterStorage\\'+filename+'.txt', 'w') as outfile:  
        json.dump(data, outfile)
        #print(y_pred_2)
        