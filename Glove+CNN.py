import numpy as np
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


from nltk.tokenize import RegexpTokenizer
import pandas as pd
dataset_train=pd.read_csv('AnotherDataset.csv').dropna()
tokenizer = RegexpTokenizer(r'\w+')

dataset_train["tokens"] = dataset_train["Sentence"].apply(tokenizer.tokenize)
dataset_train.head()



from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical

all_words = [word for tokens in dataset_train["tokens"] for word in tokens]
sentence_lengths = [len(tokens) for tokens in dataset_train["tokens"]]
VOCAB = sorted(list(set(all_words)))
print("%s words total, with a vocabulary size of %s" % (len(all_words), len(VOCAB)))
print("Max sentence length is %s" % max(sentence_lengths))






sentences=np.asarray(dataset_train["Sentence"].tolist())
NamedLabel=np.asarray(dataset_train["Label"].tolist())


from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical

EMBEDDING_DIM = 300
MAX_SEQUENCE_LENGTH = 35
VOCAB_SIZE = len(VOCAB)

VALIDATION_SPLIT=.2
tokenizer = Tokenizer(num_words=VOCAB_SIZE)
tokenizer.fit_on_texts(dataset_train["Sentence"].tolist())
sequences = tokenizer.texts_to_sequences(dataset_train["Sentence"].tolist())

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

cnn_data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
from sklearn.preprocessing import LabelEncoder
transform_labels = LabelEncoder()
dataset_train["category"] =transform_labels.fit_transform(dataset_train["Label"])
labels = to_categorical(np.asarray(dataset_train["category"]))

indices = np.arange(cnn_data.shape[0])
np.random.shuffle(indices)
cnn_data = cnn_data[indices]
labels = labels[indices]
NamedLabel= NamedLabel[indices]
sentences=sentences[indices]
num_validation_samples = int(VALIDATION_SPLIT * cnn_data.shape[0])





embedding_matrix = create_embedding_matrix('A:\College\Graduation Project\Project\glove.42B.300d.txt',tokenizer.word_index, EMBEDDING_DIM)



from keras.layers import Dense, Input, Flatten, Dropout, Concatenate 
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.layers import LSTM, Bidirectional
from keras.models import Model

def ConvNet(embeddings, max_sequence_length, num_words, embedding_dim, labels_index, trainable=False, extra_conv=True):
    
    embedding_layer = Embedding(num_words,
                            embedding_dim,
                            weights=[embeddings],
                            input_length=max_sequence_length,
                            trainable=trainable)

    sequence_input = Input(shape=(max_sequence_length,), dtype='int32')
    embedded_sequences = embedding_layer(sequence_input)

    # Yoon Kim model (https://arxiv.org/abs/1408.5882)
    convs = []
    filter_sizes = [3,4,5]

    for filter_size in filter_sizes:
        l_conv = Conv1D(filters=128, kernel_size=filter_size, activation='relu')(embedded_sequences)
        l_pool = MaxPooling1D(pool_size=3)(l_conv)
        convs.append(l_pool)

    l_merge = Concatenate(axis=1)(convs)

    # add a 1D convnet with global maxpooling, instead of Yoon Kim model
    conv = Conv1D(filters=128, kernel_size=3, activation='relu')(embedded_sequences)
    pool = MaxPooling1D(pool_size=3)(conv)

    if extra_conv==True:
         x = Dropout(0.5)(l_merge)  
    else:
        # Original Yoon Kim model
        x = Dropout(0.5)(pool)
    x = Flatten()(x)
    x = Dense(20, activation='relu')(x)
    x = Dropout(0.5)(x)
    preds = Dense(labels_index, activation='softmax')(x)

    model = Model(sequence_input, preds)
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['acc'])

    return model


x_train = cnn_data[:-num_validation_samples]
y_train = labels[:-num_validation_samples]
x_val = cnn_data[-num_validation_samples:]

y_val = labels[-num_validation_samples:]

model = ConvNet(embedding_matrix, MAX_SEQUENCE_LENGTH, len(word_index)+1, EMBEDDING_DIM, 
                len(list(dataset_train["Label"].unique())), True)
model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=30, batch_size=10)
loss, accuracy = model.evaluate(x_train, y_train, verbose=False)
print("Training Accuracy: {:.4f}".format(accuracy))
loss, accuracy = model.evaluate(x_val, y_val, verbose=False)
print("Testing Accuracy:  {:.4f}".format(accuracy))
y_pred = model.predict(x_val)
from sklearn.externals import joblib
filename = 'finalized_model.sav'
joblib.dump(model, filename)



testing=[]
testing.append("bsc")
X_test1 = tokenizer.texts_to_sequences(testing)
X_test1 = pad_sequences(X_test1, padding='post', maxlen=35)
prediction=model.predict(X_test1)
print(prediction)

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
        