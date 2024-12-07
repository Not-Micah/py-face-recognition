import tkinter as tk
import cv2
from PIL import Image, ImageTk
import util
import os
import subprocess
from datetime import datetime

class App():    
    def __init__(self):
        # Initialize the Window
        self.main_window  = tk.Tk()
        self.main_window.geometry("1280x520+350+100")

        # Defining Buttons
        self.login_button_main_window = util.get_button(window=self.main_window, text="Login", color="green", command=self.login)
        self.login_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(window=self.main_window, text="Register New User", color="gray", command=self.register_new_user, fg="black")
        self.register_new_user_button_main_window.place(x=750, y=400)

        # Getting Webcam
        self.webcam_label = util.get_img_label(window=self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(label=self.webcam_label)

        # Database Directory
        self.db_dir = "./db"
        self.log_path = './log.txt'
        
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:                                              # Checking whether 'cap' is a class variable
            self.cap = cv2.VideoCapture(0)                                          # Reading a frame from the web cam

        self._label = label  
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame

        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)        # Convert the frame into the needed format
        self.most_recent_capture_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)                  
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        
        self._label.after(20, self.process_webcam)                                  # Repeating same process after 20ms

    def login(self):
        unknown_img_path = './tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        name = output.split(',')[1][:-5]
        
        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box(title="Oops",  description="Unknown user, please register new user or try again!")
        else:
            util.msg_box(title="Welcome back!", description=f"Hello there {name}")
            with open(self.log_path, 'a') as f:
                f.write(f"{name} logged in at {datetime.now()}")

        os.remove(unknown_img_path)

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1280x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(window=self.register_new_user_window, text="Accept", color="green", command=self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(window=self.register_new_user_window, text="Try Again", color="red", command=self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.caputre_label = util.get_img_label(window=self.register_new_user_window)
        self.caputre_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(label=self.caputre_label)

        self.entry_text_register_new_user = util.get_entry_text(window=self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(window=self.register_new_user_window, text="Enter User Name : ")
        self.text_label_register_new_user.place(x=750, y=70)

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)                  
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)
        util.msg_box(title="Success", description="User was registered successfully")
        self.register_new_user_window.destroy()

    def start(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    App().start()