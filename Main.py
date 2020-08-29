from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
from Process_vid import FrameHelper
from threading import Thread
import get_pulse
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


class GUI:
    def __init__(self):
        self.proc = FrameHelper()  # FrameHelper obj
        self.App = get_pulse.getPulseApp()  # getPulseApp obj
        self.root = Tk()  # Tk obj
        self.root.bind('<Control-e>', lambda e: self.end_program())  # closes the program
        self.root.protocol("WM_DELETE_WINDOW", self.end_program)  # ask when closing


        self.menubutton = Menubutton(self.root, text="Menu")

        self.menubutton.menu = Menu(self.menubutton)
        self.menubutton["menu"] = self.menubutton.menu

        self.motivation = Menu(self.menubutton)  # sub-menu
        self.menubutton.menu.add_cascade(menu=self.motivation, label="Motivation")
        self.motivation.add_command(label="Pictures", command=self.proc.motivation_pics)
        self.motivation.add_command(label="VIdeo", command=self.proc.motivation_vid_t)  # needs a new thread

        self.menubutton.menu.add_separator()

        self.menubutton.menu.add_command(label="Open Cascade Folder", command=lambda: self.open_folder(self.casc_path))
        self.menubutton.menu.add_command(label="Open Logs Folder", command=lambda: self.open_folder(self.logs_path))
        self.menubutton.menu.add_command(label="Open Videos Folder", command=lambda: self.open_folder(self.vid_path))
        self.menubutton.menu.add_command(label="Open Pictures Folder", command=lambda: self.open_folder(self.pics_path))
        self.menubutton.grid(row=0)

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

    # opens a new window with 2 choices:
    # 1. detect from pictures
    # 2. detect from video
    def baby_detection(self):
        self.disable(self.btn1)

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
        self.proc.state = 'baby detection'  # TODO: reuse of the video processing method (show_feed) and its vars!
        t2 = Thread(target=self.proc.show_vid)
        t2.start()

    def pulse_monitor(self):
        self.disable(self.btn3)
        t3 = Thread(target=self.App.MY_main_loop)
        t3.start()

    # clicking Ctrl+e OR [x] will end the program
    def end_program(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            print("Program was terminated. Both flags updated - closing program")
            self.proc.flag_end = True  # will kill all running threads in Process_vid
            self.App.flag_end = True  # will kill all running threads in get_pulse
            plt.close('all')
            self.root.destroy()


if __name__ == "__main__":
    run = GUI().root
    # allows changes after the GUI was lunched
    # while True:
    #    run.update_idletasks()
    #    run.update()
    run.mainloop()
