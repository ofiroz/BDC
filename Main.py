from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
# import Process_vid
from Process_vid import FrameHelper
from threading import Thread
import get_pulse
import warnings
warnings.filterwarnings("ignore")


class GUI:
    def __init__(self):
        self.proc = FrameHelper()  # FrameHelper obj

        self.root = Tk()  # Tk obj
        self.root.bind('<Control-e>', lambda e: self.end_program())  # closes the program
        self.root.protocol("WM_DELETE_WINDOW", self.end_program)  # ask when closing
        self.flag_end = True  # if "Ctrl + e" is pressed it will be False

        self.menubutton = Menubutton(self.root, text="Menu")
        self.menubutton.menu = Menu(self.menubutton)
        self.menubutton["menu"] = self.menubutton.menu

        # shows the bad results with the opencv official frontal face Haar casc
        self.menubutton.menu.add_command(label="Motivation", command=self.proc.motivation)

        self.menubutton.menu.add_command(label="Open Cascade Folder", command=lambda: self.open_folder(self.casc_path))
        self.menubutton.menu.add_command(label="Open Logs Folder", command=lambda: self.open_folder(self.logs_path))
        self.menubutton.menu.add_command(label="Open Videos Folder", command=lambda: self.open_folder(self.vid_path))
        self.menubutton.menu.add_command(label="Open Pictures Folder", command=lambda: self.open_folder(self.pics_path))
        self.menubutton.grid(row=0)

        # self.buttons_state = [0, 0, 0]  # if pressed = 1
        self.label = ttk.Label(self.root, text="Some Welcome Label")
        self.label.grid(row=1, column=0, columnspan=3)
        self.label.config(font=('Ariel', 18, 'bold'))  # font_name, size, extra (bold, underline..)

        # label = ttk.Label(root, text='Some Welcome Label', font=('Ariel', 18, 'bold'))
        # label.grid(row=0, column=0, columnspan=3)

        self.btn1 = ttk.Button(self.root, text="Baby Detection")
        self.btn1.grid(row=2, column=0)
        self.btn1.config(command=self.baby_detection)

        self.btn2 = ttk.Button(self.root, text='Respiratory Monitor')
        self.btn2.grid(row=2, column=1)
        self.btn2.config(command=self.breath_detection)

        self.btn3 = ttk.Button(self.root, text='Pulse Monitor')
        self.btn3.grid(row=2, column=2)
        self.btn3.config(command=self.pulse_monitor)

        # the 'r' is a conversion to raw string (unicode error)
        self.casc_path = r"C:\Users\ofirozer\PycharmProjects\untitled\1PROJECT\custom haar cascade\Cascades"
        self.logs_path = r"C:\Users\ofirozer\PycharmProjects\untitled\1PROJECT\custom haar cascade\Logs Research"
        self.vid_path = r"C:\Users\ofirozer\PycharmProjects\untitled\1PROJECT\custom haar cascade\Videos"
        self.pics_path = r"C:\Users\ofirozer\PycharmProjects\untitled\1PROJECT\Project ReWriten\Pictures_Set"

    @staticmethod
    def open_folder(path):
        p = os.path.realpath(path)
        os.startfile(p)

    # This function disables the input button - there is no need to press it a second time
    @staticmethod
    def disable(btn):
        btn.config(state="disabled")
        print("Disabled the", btn['text'], "button.", sep=" ")

    @staticmethod
    def enable(btn):
        btn.config(state="enable")
        print("Enabled the", btn['text'], "button.", sep=" ")

    # runs samples videos and returns person with a circled center
    def breath_detection(self):
        self.disable(self.btn2)
        # self.proc.state = 'baby detection'
        print('self.proc.state',self.proc.state)

        # 2 threads for to 2 infinity loops
        t1 = Thread(target=self.proc.call_frame_processor)  # process the sample frame TODO: useless
        t2 = Thread(target=self.proc.show_vid)  # Shows the video
        t2.start()
        t1.start()
        # when the program ends kill threads
        # t1.join()
        # t2.join()

    # opens a new window with 2 choices:
    # 1. detect from pictures
    # 2. detect from video
    def baby_detection(self):
        self.disable(self.btn1)
        # self.proc.state = 'baby detection'
        # print('self.proc.state', self.proc.state)
        newWindow = Toplevel(self.root)
        newWindow.title("tk2")
        Label(newWindow, text="Please choose the detection platform:").grid(row=1, column=0, columnspan=2)

        #  the only good looking method to pass an arg AND commence two action at the same time
        newWindow.protocol("WM_DELETE_WINDOW", lambda e=self.btn1: [newWindow.destroy(), self.enable(e)])
        newWindow.bind('<Control-e>', lambda e: self.end_program())  # closes the program - needed here as well

        b1 = ttk.Button(newWindow, text="PictureDS")
        b1.grid(row=2, column=0)
        b1.config(command=self.baby_detection_pics)

        b2 = ttk.Button(newWindow, text="Video")
        b2.grid(row=2, column=1)
        b2.config(command=self.baby_detection_vid)

    # Run the cascade on pictures dataset
    def baby_detection_pics(self):
        print("Commencing baby detection on the Pictures DataSet")
        t1 = Thread(target=self.proc.detect_from_pics)
        t1.start()

    # Run the cascade on a video
    def baby_detection_vid(self):
        print("Commencing baby detection on a Video")
        self.proc.state = 'baby detection'  # TODO: reuse of the video processing method (show_feed)
        t2 = Thread(target=self.proc.show_vid)
        t2.start()

    def pulse_monitor(self):
        self.disable(self.btn3)
        # TODO: solve the [ WARN:0]
        # TODO: cancel the camera 0 activation
        App = get_pulse.getPulseApp()

        t3 = Thread(target=App.MY_main_loop)
        t3.start()

    # Ctrl+e OR clicking [x] will end the program
    def end_program(self):
        print("FLAG updated to FALSE - closing program")
        self.flag_end = False  # will kill all running threads
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()


if __name__ == "__main__":
    run = GUI().root
    run.mainloop()

# TODO: make a combo box in the GUI for file name selection
# https://www.linkedin.com/learning/python-gui-development-with-tkinter-2/making-selections-with-the-combobox-and-spinbox?u=2101329

'''
file_name = StringVar()
combobox = ttk.Combobox(root, textVariable = file_name)
combobox.pack()
combobox.config(values = [list of names]
'''
