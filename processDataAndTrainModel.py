import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import TensorBoard
import numpy as np


#ACTIONS = np.array(['השעה','אתה - ימין','לא','מה','איפה','שמח'])
ACTIONS = np.array(['אתה','מה','שמח','עומד','השעה'])

numbers_of_videos = 20  # Number of videos to each word
video_length = 30       # Frames we take to analyze
label_map = {label: num for num, label in enumerate(ACTIONS)}
DATA_PATH = os.path.join('C:\\Sign_Language_Data')

sequences, labels = [], []
for sing in ACTIONS:
    for video in range(numbers_of_videos):
        window = []
        for frame_number in range(video_length):
            res = np.load(os.path.join(DATA_PATH, sing, str(video), "{}.npy".format(frame_number)))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[sing])

X = np.array(sequences)
y = to_categorical(labels).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
print(X_train.shape)
print(X_train[0].shape)
# Build and train LSTM neural Network
log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)

model = Sequential()
model.add(LSTM(128, return_sequences=True, activation='relu', input_shape=X_train[0].shape))
model.add(Dropout(0.2))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(Dropout(0.2))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(32, activation='relu'))
model.add(Dense(ACTIONS.shape[0], activation='softmax'))

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
#model.load_weights('C:\\Sign_Language_Data\\israeli_sing_language_model.h5')
model.fit(X_train, y_train, epochs=500, callbacks=[tb_callback])

model.summary()

# Predict
#res = model.predict(X_test)
# Checking and print the numbers not fit
#for i in range(len(ACTIONS)):
 #   pre = ACTIONS[np.argmax(res[i])]
  #  actual = ACTIONS[np.argmax(y_test[i])]
   # if pre != actual:
    #    print(i)

model.save('C:\\Sign_Language_Data\\israeli_sing_language_model.h5')
# if we want to load the model
# !!!!! first !!!!! run the model LSTM and Dense
# !!!!! second !!!! compile the model
# and then run this command --> model.load_weights('israeli_sing_language_model.h5')          model = keras.models.load_model('bottleneck_fc_model.h5')

# To evaluate and confusion matrix :
# from sklearn.metrix import multilabal_confusion_matrix, accuracy_score
# res = model.predict(X_test)
# ytrue = np.argmax(y_test, axis=1).tolist()
# yhat = np.argmax(res, axis=1).tolist()
# multilabel_confusion_matrix(ytrue, yhat)