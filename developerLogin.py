from tkinter import *
from PIL import Image, ImageTk
import main
import devGUI
import json
import devGUI

class dev_login(Frame):

    def __init__(self, parent, controller, main):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        main.destroy()
        self.controller.title("Isign - Developer LogIn")
        self.canvas = Canvas(self.parent, bg="#FFFFFF", height=600, width=1024, bd=0, highlightthickness=0,
                             relief="ridge")
        self.canvas.place(x=0, y=0)
        # create blue rectangle and on top of it our Isign LOGO
        self.canvas.create_rectangle(0.0, 0.0, 500.0, 600.0, fill="#78BFDD", outline="")
        self.logo_img = Image.open('assets/Logo.png')
        self.logo_resize = self.logo_img.resize((450, 450), Image.ANTIALIAS)
        self.logo_img = ImageTk.PhotoImage(self.logo_resize)
        self.canvas.create_image(240.0, 300.0, image=self.logo_img)
        self.canvas.create_text(702.0, 40.0, anchor="nw", text="Isign", fill="#000000", font=("Roboto", 64 * -1))
        self.canvas.create_text(840, 80.0, anchor="nw", text="dev", fill="#000000", font=("Roboto", 18 * -1))
        # username text entry
        self.canvas.create_text(680.0, 170.0, anchor="nw", text="UserName", fill="#000000", font=("Roboto", 20 * -1))
        self.username = StringVar()
        self.usernameEntry = Entry(self.parent, textvariable=self.username)
        self.usernameEntry.place(x=680, y=200, width=200, height=40)

        # password text entry
        self.canvas.create_text(680.0, 300.0, anchor="nw", text="Password", fill="#000000", font=("Roboto", 20 * -1))
        self.password = StringVar()
        self.passwordEntry = Entry(self.parent, textvariable=self.password, show='*')
        self.passwordEntry.place(x=680, y=330, width=200, height=40)

        self.goBack_image = PhotoImage(file='assets/goBack_blue.png')
        self.logInBtn_image = PhotoImage(file='assets/Button.png')
        self.goBackBtn = Button(self.parent, image=self.goBack_image, borderwidth=0, highlightthickness=0,
                                command=lambda: self.controller.show_frame("main"),
                                relief="flat")
        self.logInBtn = Button(self.parent, image=self.logInBtn_image, borderwidth=0, highlightthickness=0,
                               command=lambda: self.validUsers(self.username, self.password),
                               relief="flat")
        self.logInBtn.place(x=705, y=426, width=158, height=52)
        self.goBackBtn.place(x=26, y=32, width=22, height=20)

    def validUsers(self, check_details, password):
        data = open('LogIn\\users.json')
        users = json.load(data)
        for user in users:
            if user["username"].lower() == check_details.get().lower() and user["password"].lower() == password.get():
                self.controller.show_frame(devGUI.DevGUI(self.parent, self.controller, self))
                break
        else:
            self.canvas.create_text(715.0, 400.0, anchor="nw", text="invalid username or password", fill="red",
                                    font=("Roboto", 10 * -1))
        #if user.get().lower() == 'liran' and password.get() == 'pass':
        #    devGUI.changeToDevWin(logInGui)
        #else:
        #    print("bye!")
