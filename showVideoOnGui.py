import tkinter as tk
from tkinter import Frame
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import numpy as np
import PIL
import cv2
import numpy as np
import os
import time
import mediapipe as mp
from words import Words


class StartVideo:

    def __init__(self, toupdate, dev=None):
        self.to_update = toupdate
        self.cap = self.to_update.capture
        self.stop = self.to_update.stop
        self.mp_holistic = mp.solutions.holistic  # MediaPipe Holistic model
        self.mp_show = mp.solutions.drawing_utils  # Drawing utilities
        self.video_canvas = self.to_update.video_canvas
        self.dev = dev
        if self.dev is None:
            self.base_word = 'עומד'
            wordClass = Words()
            self.words = wordClass.get()
            self.model = self.lstm_model()
            self.sequence = []
            self.sentence = []
            self.predictions = []
            self.threshold = 0.8
        else:
            pass

    def mediapipe_detection(self, image, model):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Color Convert from BGR(cv2) to RBG
        image.flags.writeable = False  # Image is not longer writeable
        results = model.process(image)  # Make prediction
        image.flags.writeable = True  # Image is now writeable
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Color Convert from RBG to BGR(cv2)
        return image, results

    # Draw face, pose and hands connections
    def show_landmarks(self, image, results):
        #self.mp_show.draw_landmarks(image, results.face_landmarks, self.mp_holistic.FACEMESH_CONTOURS,
                                    #self.mp_show.DrawingSpec(color=(80, 80, 80), thickness=1, circle_radius=1))
        #self.mp_show.draw_landmarks(image, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS,
                                    #self.mp_show.DrawingSpec(color=(80, 80, 80), thickness=1, circle_radius=1))
        self.mp_show.draw_landmarks(image, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                    self.mp_show.DrawingSpec(color=(180, 100, 100), thickness=2, circle_radius=2))
        self.mp_show.draw_landmarks(image, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                    self.mp_show.DrawingSpec(color=(180, 100, 100), thickness=2, circle_radius=2))

    def extract_keypoints(self, results):
        #pose = np.array([[res.x, res.y, res.z] for res in results.pose_landmarks.landmark]).flatten() \
        #    if results.pose_landmarks else np.zeros(33 * 4)
        left_hand = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() \
            if results.left_hand_landmarks else np.zeros(21 * 3)
        right_hand = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() \
            if results.right_hand_landmarks else np.zeros(21 * 3)
        #face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() \
        #    if results.face_landmarks else np.zeros(468 * 3)
        return np.concatenate([left_hand, right_hand]) # (126,)    # (1662,) [pose, face, left_hand, right_hand]

    def lstm_model(self):
        model = Sequential()
        model.add(LSTM(128, return_sequences=True, activation='relu', input_shape=(30, 126)))
        model.add(Dropout(0.2))
        model.add(LSTM(128, return_sequences=True, activation='relu'))
        model.add(Dropout(0.2))
        model.add(LSTM(64, return_sequences=False, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(self.words.shape[0], activation='softmax'))
        model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
        model.load_weights('model\\israeli_sing_language_model.h5')
        return model

    def results_from_model(self, results):
        keyPoints = self.extract_keypoints(results)  # extract key point from image(camera)
        self.sequence.append(keyPoints)
        sequence = self.sequence[-30:]
        if len(sequence) == 30:
            res = self.model.predict(np.expand_dims(sequence, axis=0))[0]
            # print(self.words[np.argmax(res)], res)
            self.predictions.append(np.argmax(res))
            checkRes = self.words[np.argmax(res)]
            if np.unique(self.predictions[-15:])[0] == np.argmax(res):
                if res[np.argmax(res)] > self.threshold and checkRes != self.base_word:
                    if len(self.sentence) > 0:
                        if checkRes != self.sentence[-1]:
                            self.sentence.append(checkRes)
                            return checkRes
                            # self.sentence.append(checkRes)
                            # print(self.sentence)
                    else:
                        self.sentence.append(checkRes)
                        return checkRes
                        # self.sentence.append(checkRes)
                        # print(self.sentence)
        if len(self.sentence) > 8:
            self.sentence = self.sentence[-8:]
        if len(self.predictions) > 40:
            self.predictions = self.predictions[-40:]

        return self.base_word

    def set_stop(self, stop):
        self.stop = stop

    def showVideo(self):
        with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic_model:
            while not self.stop:
                ret, frame = self.cap.read()                                            # Read frame from webcam
                if ret:
                    frame, results = self.mediapipe_detection(frame, holistic_model)    # Make detections
                    #self.show_landmarks(frame, results)                                # Draw the landmarks
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                    self.video_canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                    sentence = self.results_from_model(results)
                    if sentence != self.base_word:
                        self.to_update.textarea.insert(tk.END, sentence)
                        self.to_update.textarea.insert(tk.END, " ")
                    self.to_update.update()

            else:
                self.cap.release()

    def recordVideo(self):
        with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic_model:
            while not self.stop:
                ret, frame = self.cap.read()  # Read frame from webcam
                if ret:
                    frame, results = self.mediapipe_detection(frame, holistic_model)  # Make detections
                    self.show_landmarks(frame, results)                                # Draw the landmarks
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                    self.video_canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                    self.to_update.update()
            else:
                self.cap.release()
        # take from create video per word
