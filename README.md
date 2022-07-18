# Isign
Israeli Sign Language Translator
![image](https://user-images.githubusercontent.com/62890495/179477055-fde60ce9-ad0b-479c-a3b1-933c6271fcaa.png)
# Abstract
The deaf-mute community has always suffered from communication problems in their daily life. 
In recent years technological developments in the field of machine learning have succeeded to break these communication barriers,But still due to lack of large dataset that each language has its own sign language, 
the developments do not reach to all the deaf community. 
In this project we deal with the challenges of developing software to translate the Israeli Sign Language (ISL) into text. 
We do that by using Mediapipe, a key points identification tool, and machine learning algorithms. The input is a live video of a human that speaks in the Israeli sign language, translating it to text. We use the Long Short-Term memory (LSTM) machine learning algorithm, to learn the hands movements and translate the Israeli Sign Language into text.
![image](https://user-images.githubusercontent.com/62890495/179477519-005e7cbc-9ba2-4e27-80d2-2655f4d1a972.png)
# installation
User guide:
1.	First, install Python 3.6 – 3.9 on your computer. Version that supports the installation: https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe
2.	After the Python installation, install the file Isign.exe. [Isign.zip](https://github.com/meni7665/Isign/files/9130687/Isign.zip)
3.	install the following libraries with the specific versions listed below. You can also use this command: pip install tensorflow==2.5.0 tensorflow-gpu==2.5.0 OpenCV-python==4.5.5.64 mediapipe==0.8.9.1 sklearn matplotlib protobuf~=3.19.0). To make the process easier, go to the location of the installed folder and run the file “"install dependencies”
4.	now run the file “lunch Isign”
5.	enjoy using Isign
# How it works:
This project target is creating a software to translate the Israeli Sign Language into Hebrew text, this software can help to the deaf – mute community with their communication problem, they will be able to operate this software with any smart device that have camera. The system includes 2 main modes: User mode – in this mode the deaf will speak in front of the camera and the software will analyzed has signs and translated it to Hebrew text and display it on the screen.
Developer mode – to this only to the developer there is access, they can add more videos to an exciting word that the model knows to translate or to create a new file for a new word that we want to add to our model, they can shoot as many videos they want. The length of the video is fixed and be 30 frames for each video.
# Developer Mode:
![image](https://user-images.githubusercontent.com/62890495/179478233-10d9c415-b4cc-4b6f-9815-213bb60fa2d7.png)
# User Mode:
![image](https://user-images.githubusercontent.com/62890495/179478335-32001454-0a3d-4124-9b15-054cd17f64eb.png)




