from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import IOU_Intersection_over_Union.IOU_calculator as iou
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
        self.motivation.add_command(label="Pictures, Upper Body", command=self.proc.motivation_pics)
        self.motivation.add_command(label="VIdeo, Face", command=self.proc.motivation_vid_t)  # needs a new thread

        self.menubutton.menu.add_separator()

        self.menubutton.menu.add_command(label="IOU", command=self.calc_IOU)

        self.menubutton.menu.add_separator()

        self.menubutton.menu.add_command(label="Open Samples Folder", command=lambda: self.proc.open_folder(self.Data_path))
        self.menubutton.menu.add_command(label="Open Samples Folder", command=lambda: self.proc.open_folder(self.SMP_path))
        self.menubutton.menu.add_command(label="Open Cascade Folder", command=lambda: self.proc.open_folder(self.casc_path))
        self.menubutton.menu.add_command(label="Open Logs Folder", command=lambda: self.proc.open_folder(self.logs_path))
        self.menubutton.menu.add_command(label="Open Videos Folder", command=lambda: self.proc.open_folder(self.vid_path))
        self.menubutton.menu.add_command(label="Open Pictures Folder", command=lambda: self.proc.open_folder(self.pics_path))
        self.menubutton.grid(row=0)

        self.label = ttk.Label(self.root, text="Welcome To BDC")
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
        self.Data_path = r"C:\Users\ofirozer\PycharmProjects\untitled\1PROJECT\Project ReWriten\Data"
        self.SMP_path = r"C:\Users\ofirozer\PycharmProjects\untitled\1PROJECT\Project ReWriten\Data\Samples"
        self.casc_path = r"C:\Users\ofirozer\PycharmProjects\untitled\1PROJECT\Project ReWriten\Data\Cascades"
        self.logs_path = r"C:\Users\ofirozer\PycharmProjects\untitled\1PROJECT\custom haar cascade\Logs Research"
        self.vid_path = r"C:\Users\ofirozer\PycharmProjects\untitled\1PROJECT\custom haar cascade\Videos"
        self.pics_path = r"C:\Users\ofirozer\PycharmProjects\untitled\1PROJECT\Project ReWriten\Samples\Pictures_Set"
    '''
    @staticmethod
    def open_folder(path):
        p = os.path.realpath(path)
        os.startfile(p)
    '''
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
        #self.disable(self.btn2)
        self.proc.state = 'breathing detection'
        # print('self.proc.state',self.proc.state)
        t = Thread(target=lambda: self.proc.show_vid(self.proc.cascade_upper_body))  # Dummy is a 'must' arg used in baby_detection option
        t.start()

    # opens a new window with 2 choices:
    # 1. detect from pictures
    # 2. detect from video
    def baby_detection(self):
        self.disable(self.btn1)

        newWindow = Toplevel(self.root)
        newWindow.title("Detection Options")
        Label(newWindow, text="Please choose the detection mode (testData/cascade): ").grid(row=1, column=0, columnspan=4)

        # the only good looking method to pass an arg AND commence two action at the same time
        newWindow.protocol("WM_DELETE_WINDOW", lambda e=self.btn1: [newWindow.destroy(), self.enable(e)])
        newWindow.bind('<Control-e>', lambda e: self.end_program())  # closes the program - needed here as well

        #self.menubutton.menu.add_command(label="Open Samples Folder", command=lambda: self.open_folder(self.SMP_path))
        b1 = ttk.Button(newWindow, text="PicDS-UB")
        b1.grid(row=2, column=0)
        b1.config(command=lambda: self.baby_detection_pics(self.proc.cascade_upper_body))

        b2 = ttk.Button(newWindow, text="PicDS-F")
        b2.grid(row=2, column=1)
        b2.config(command=lambda: self.baby_detection_pics(self.proc.cascade_face))

        b3 = ttk.Button(newWindow, text="Video-UB")
        b3.grid(row=2, column=2)
        b3.config(command=lambda: self.baby_detection_vid(self.proc.cascade_upper_body))

        b4 = ttk.Button(newWindow, text="Video-F")
        b4.grid(row=2, column=3)
        b4.config(command=lambda: self.baby_detection_vid(self.proc.cascade_face))

    # Run the selected cascade (UB/F) on pictures dataset
    def baby_detection_pics(self, cascade):
        print("Commencing baby detection on the Pictures DataSet - was not in use in the training process")
        # plt.close('all')
        t1 = Thread(target=lambda: self.proc.detect_from_pics(cascade))
        t1.start()

    # Run the cascade on a video
    def baby_detection_vid(self, selected_casc):
        print("Commencing baby detection on the Videos DataSet - was not in use in the training process")
        self.proc.state = 'baby detection'
        t2 = Thread(target=lambda: self.proc.show_vid(selected_casc))
        t2.start()

    def pulse_monitor(self):
        self.disable(self.btn3)
        t3 = Thread(target=self.App.MY_main_loop)
        t3.start()


    def calc_IOU(self):
        iou.calc()

    # clicking Ctrl+e OR [x] will end the program
    def end_program(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            print("Program terminated. Both flags updated - closing program")
            self.proc.flag_end = True  # will kill all running threads in Process_vid TODO check all options
            self.App.flag_end = True  # will kill all running threads in get_pulse TODO check all options
            plt.close('all')
            self.root.destroy()


if __name__ == "__main__":
    run = GUI().root
    # allows changes after the GUI was lunched
    # while True:
    #    run.update_idletasks()
    #    run.update()
    run.mainloop()
