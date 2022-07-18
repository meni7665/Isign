from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import cv2
from showVideoOnGui import StartVideo
import time
import showVideoOnGui
import threading

class DevGUI(Frame):

    def __init__(self, parent, controller, dev_login):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        dev_login.destroy()
        self.controller.title("Isign - Developer")
        self.capture = None
        self.stop = False
        self.canvas = Canvas(parent, bg="#FFFFFF", height=600, width=1024, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(8.0, 78.0, 654.0, 564.0, fill="#FFFFFF", outline="#000000")
        self.video_canvas = Canvas(self.parent, width=640, height=480)
        self.video_canvas.place(x=10, y=80)
        self.camera = StartVideo(self, "dev")
        self.controller = controller
        self.canvas.create_rectangle(670.0, 9.0, 670.0, 590.0, fill="#3D7892", outline="")
        self.canvas.create_text(780.0, 190.0, anchor="nw", text="word:", fill="#000000",
                                font=("Roboto", 18 * -1))
        self.canvas.create_text(750.0, 40.0, anchor="nw", text="Isign", fill="#000000", font=("Roboto", 64 * -1))
        #### textarea   later : textarea.insert(tk.END, *variable*)
        self.canvas.create_text(780.0, 250.0, anchor="nw", text="number of videos:", fill="#000000",
                                font=("Roboto", 18 * -1))
        self.text_word = StringVar()
        self.wordEntry = Entry(self.parent, textvariable=self.text_word)
        self.wordEntry.place(x=780, y=220, width=100, height=20)
        self.text_numOfVideo = StringVar()
        self.numOfVideoEntry = Entry(self.parent, textvariable=self.text_numOfVideo)
        self.numOfVideoEntry.place(x=780, y=280, width=100, height=20)

        # Drop down
        self.clicked = StringVar()
        self.options = []
        self.numOfCams = 0
        self.check_cameras()
        # clicked.set(options[0])
        self.chooseCamera = ttk.OptionMenu(parent, self.clicked, self.options[0], *self.options)
        self.chooseCamera.place(x=780, y=150, width=100, height=30)
        # create start/stop Btn - and texts
        self.startBtn_image = PhotoImage(file='assets/start_btn.png')
        self.stopBtn_image = PhotoImage(file='assets/stop_btn.png')
        self.goBack_image = PhotoImage(file='assets/goBack.png')
        self.startBtn = Button(parent, image=self.startBtn_image, borderwidth=0, highlightthickness=0,
                               command=lambda: [self.startvideo()], relief="flat")
        self.stopBtn = Button(parent, image=self.stopBtn_image, borderwidth=0, highlightthickness=0,
                              command=lambda: self.stopvideo(),
                              relief="flat")
        self.goBackBtn = Button(parent, image=self.goBack_image, borderwidth=0, highlightthickness=0,
                                command=lambda: [self.stopvideo(True), self.controller.show_frame("main")],
                                relief="flat")  # controller.show_frame()
        self.startBtn.place(x=762, y=320, width=77, height=30)
        self.stopBtn.place(x=850, y=320, width=77, height=30)
        self.goBackBtn.place(x=26, y=32, width=25, height=25)

    def check_cameras(self):
        self.numOfCams = self.camerasConnected()  # can do status bar progress
        if self.numOfCams == 0:
            # messagebox.showerror("Error", "Please connect camera!")
            self.clicked.set("no camera")
            self.options.append("no camera")
        else:
            for i in range(self.numOfCams):
                self.options.append(i + 1)

    def startvideo(self):
        self.camera.set_stop(False)  # = False
        # self.check_cameras()
        if self.numOfCams == 0:
            messagebox.showerror("Error", "Please connect camera!")
        else:
            self.capture = cv2.VideoCapture(int(self.clicked.get()) - 1)
            self.camera = StartVideo(self, "dev")
            self.startBtn.config(state="disabled")
            threading.Thread(target=self.camera.recordVideo()).start()
            # threading.Thread(target=camera.showVideo()).start()

    def stopvideo(self, back=None):
        self.camera.set_stop(True)  # = True
        self.startBtn.config(state="normal")
        self.textarea_word.delete("1.0", "end")
        self.textarea_numOfVideo.delete("1.0","end")
        if back:
            time.sleep(1)

    def clearCapture(self, capture):
        capture.release()
        cv2.destroyAllWindows()

    def camerasConnected(self):
        n = 0
        for i in range(3):
            try:
                cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
                if cap:
                    ret, frame = cap.read()
                    if ret:
                        # cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        self.clearCapture(cap)
                        n += 1
            except:
                self.clearCapture(cap)
                break
        return n
