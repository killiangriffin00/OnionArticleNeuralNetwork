from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.models import Sequential, Model
from keras import layers
import dataPreparation as dp
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

data = dp.importData()
clean_data = dp.cleanData(data)

MAXLEN = 100
X = []
y = []

#build data sets for features, target
data_map = {}
for count, (t, l) in enumerate(clean_data):
    X.append(t)
    y.append(l)
    data_map[t] = data[count][0]


X_train, X_test_text, y_train, y_test = train_test_split(X, y, test_size=0.1)

tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test_text)

vocab_size = len(tokenizer.word_index) + 1
print("Vocabulary size: {}".format(vocab_size))

X_train = pad_sequences(X_train, padding='post', maxlen=MAXLEN)
X_test = pad_sequences(X_test, padding='post', maxlen=MAXLEN)

#build model
#MODEL STRUCTURE
#=================================
# Layer 1: Embedding layer, dimensionality reduction to 200 inputs
# Layer 2: Convolution, relu activation
# Layer 3: Max Pooling
# Layer 4: Dense layer, 12 nodes, with a 20% dropout
# Layer 5: Single sigmoid activation for output.
# =================================
model = Sequential()
model.add(layers.Embedding(vocab_size, 200, input_length=MAXLEN))
model.add(layers.Conv1D(128, 15, activation='relu'))
model.add(layers.GlobalMaxPooling1D())
model.add(layers.Dense(12, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# prints the structure of the model
model.summary()

# this is needed for fitting
X_train = np.array(X_train)
X_test = np.array(X_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

#Train the model. 20 epochs with a batch size of 1024
#CUDA HIGHLY RECOMMENDED.
#If you don't have CUDA support, you'll want to run 5 epochs tops!
fit = model.fit(
    X_train, 
    y_train, 
    epochs=20, 
    verbose=1, 
    validation_data=(X_test, y_test), 
    batch_size=1024
)

output = model.predict(X_test)

#generate confusion matrix
conf_matrix = confusion_matrix(y_test, np.rint(output))
print("Confusion matrix:")
print(conf_matrix)

#Write output to test results to file for the frontend.
# False positives and false negatives are sampled for process documentation reasons.
file = open("archive/AlgorithmOutput.csv", 'w', encoding="UTF-8")
fpfile = open("archive/FalsePositives.csv", 'w', encoding="UTF-8")
fnfile = open("archive/FalseNegatives.csv", 'w', encoding="UTF-8")
for count, value in enumerate(X_test_text):
    if output[count] > .5:
        file.write(data_map[value] + ",1" + "," + str(y_test[count]) + "\n")
        if(y_test[count] == 0): # False positive
            fpfile.write(data_map[value] + ",1," + str(y_test[count]) + "\n")
    else:
        file.write(data_map[value] + ",0" + "," + str(y_test[count]) + "\n")
        if(y_test[count] == 1): # False negative
            fnfile.write(data_map[value] + ",0," + str(y_test[count]) + "\n")

loss, accuracy = model.evaluate(X_train, y_train, verbose=1)
print(f"Training Accuracy: {accuracy}")

loss, accuracy = model.evaluate(X_test, y_test, verbose=1)
print(f"Testing Accuracy: {accuracy}")


#Generate accuracy and loss graphs.
accuracy = fit.history['accuracy']
validation_accuracy = fit.history['val_accuracy']
loss = fit.history['loss']
validation_loss = fit.history['val_loss']
epochs = range(len(accuracy))

plt.plot(epochs, accuracy, label='Training Accuracy')
plt.plot(epochs, validation_accuracy, label='Test accuracy')
plt.title('Training and Testing accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.figure()

plt.plot(epochs, loss, label='Training Loss')
plt.plot(epochs, validation_loss, label ='Test Loss')
plt.title('Training and Testing loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()