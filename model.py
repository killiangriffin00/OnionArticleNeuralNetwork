from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.models import Sequential, Model
from keras import layers
import dataPreparation as dp
import numpy as np
from sklearn.model_selection import train_test_split

data = dp.getCleanData()

MAXLEN = 100
X = []
y = []

for (t, l) in data:
    X.append(t)
    y.append(l)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

vocab_size = len(tokenizer.word_index) + 1

X_train = pad_sequences(X_train, padding='post', maxlen=MAXLEN)
X_test = pad_sequences(X_test, padding='post', maxlen=MAXLEN)

model = Sequential()
model.add(layers.Embedding(vocab_size, 200, input_length=MAXLEN))
model.add(layers.Conv1D(128, 5, activation='relu'))
model.add(layers.GlobalMaxPooling1D())
model.add(layers.Dense(10, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# prints the structure of the model
model.summary()

# this is needed for fitting
X_train = np.array(X_train)
X_test = np.array(X_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

model.fit(
    X_train, 
    y_train, 
    epochs=10, 
    verbose=1, 
    validation_data=(X_test, y_test), 
    batch_size=10
)

loss, accuracy = model.evaluate(X_train, y_train, verbose=1)
print(f"Training Accuracy: {accuracy}")

loss, accuracy = model.evaluate(X_test, y_test, verbose=1)
print(f"Testing Accuracy: {accuracy}")
