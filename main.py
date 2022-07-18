from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
import userGUI
import developerLogin


class MainApp(Tk):

    def __init__(self):
        super().__init__()
        self.geometry("1024x600")
        self.title("Isign")
        self.icon = PhotoImage(file='assets/Logo.png')
        self.iconphoto(True, self.icon)
        self.configure(bg="#FFFFFF")
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.show_frame(Start(self.container, self))

    def show_frame(self, main):
        if main == "main":
            Start(self.container, self).tkraise()
        else:
            main.tkraise()


class Start(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("Isign")
        self.canvas = Canvas(parent, bg="#FFFFFF", height=600, width=1024, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        # create blue rectangle and on top of it our Isign LOGO
        self.canvas.create_rectangle(0.0, 0.0, 500.0, 600.0, fill="#78BFDD", outline="")
        self.logo_img = Image.open('assets/Logo.png')
        self.logo_resize = self.logo_img.resize((450, 450), Image.ANTIALIAS)
        self.logo_img = ImageTk.PhotoImage(self.logo_resize)
        self.canvas.create_image(240.0, 300.0, image=self.logo_img)
        # end
        # create Developer/User Btn - and texts
        self.userBtn_image = PhotoImage(file='assets/user.png')
        self.developerBtn_image = PhotoImage(file='assets/developer.png')
        self.userBtn = Button(parent, image=self.userBtn_image, borderwidth=0, highlightthickness=0,
                              command=lambda: controller.show_frame(userGUI.UserGUI(parent, controller, self)), relief="flat")
        self.developerBtn = Button(parent, image=self.developerBtn_image, borderwidth=0, highlightthickness=0,
                                   command=lambda: controller.show_frame(developerLogin.dev_login(parent, controller, self)), relief="flat")
        self.userBtn.place(x=660, y=390, width=208, height=60)
        self.developerBtn.place(x=660, y=250, width=208, height=60)
        self.canvas.create_text(721, 191, anchor="nw", text="You are", fill="#000000", font=("Roboto", 24 * -1))
        self.canvas.create_text(746, 340, anchor="nw", text="Or", fill="#000000", font=("Roboto", 24 * -1))
        self.canvas.create_text(698, 56, anchor="nw", text="Isign", fill="#000000", font=("Roboto", 64 * -1))


if __name__ == '__main__':
    gui = MainApp()
    gui.resizable(False, False)
    gui.update()
    gui.mainloop()
