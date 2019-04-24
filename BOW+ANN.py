import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#import functions as fn
#import DocxReader as reader
import json
import re
dataset_train=pd.read_csv('AnotherDataset.csv')
training_set = dataset_train.iloc[:,1:2]
y = dataset_train.iloc[:,2:3]

counts = dataset_train['Label'].value_counts()
print(counts)

sentences_train =[]
for i in range(len(training_set)):
    sentences_train.append(training_set[i:i+1].values[0,0])



from sklearn.preprocessing import LabelBinarizer
encoder = LabelBinarizer()
transfomed_label = encoder.fit_transform(y)
print(transfomed_label)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(training_set, transfomed_label, test_size=0.25, random_state=100,shuffle=True)

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
classifier.add(Dense(units = 2100, kernel_initializer = 'uniform', activation = 'relu', input_dim = 4273))
classifier.add(Dropout(0.5))

# Adding the second hidden layer
#classifier.add(Dense(units = 1150, kernel_initializer = 'uniform', activation = 'relu'))
#classifier.add(Dropout(0.2))

# Adding the output layer
classifier.add(Dense(units = 10, kernel_initializer = 'uniform', activation = 'softmax'))

# Compiling the ANN
classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

# Fitting the ANN to the Training set
classifier.fit(X_train, y_train, batch_size =100, epochs = 20,validation_data=(X_test, y_test))
filename = 'finalized_model.sav'
joblib.dump(classifier, filename)
loss, accuracy = classifier.evaluate(X_test, y_test, verbose=False)
print("Testing Accuracy:  {:.4f}".format(accuracy))
y_pred = classifier.predict(X_test)
y_pred=(y_pred == y_pred.max(axis=1)[:,None]).astype(int)

print("sklearn accuracy:",accuracy_score(y_test,y_pred))


courses,others,education,faculty,grade,project,techskills,personalskills,language,experience = ([] for i in range(10))
labels={0:courses,1:education,2:experience,3:faculty,4:grade,5:language,6:others,7:personalskills
        ,8:project,9:techskills}
#for i in range(0,75):
#    key=y_pred[i].argmax(axis=0)
#    labels[key].append(X_test_vec[i])




import json

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



with open('data.txt', 'w') as outfile:  
    json.dump(data, outfile)














###############################################################################################################################

def ClassifySentenceList(sentence_list,filename):
   
    courses,others,education,faculty,grade,project,techskills,personalskills,language,experience = ([] for i in range(10))
    labels={0:courses,1:education,2:experience,3:faculty,4:grade,5:language,6:others,7:personalskills
        ,8:project,9:techskills}
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
    with open('InterStorage\\'+filename+'.txt', 'w') as outfile:  
        json.dump(data, outfile)
        #print(y_pred_2)
        
