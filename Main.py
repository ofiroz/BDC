from tkinter import *  # now can use the name of stuff without the "tkinter."
from tkinter import ttk
# import Process_vid
from Process_vid import FrameHelper
from threading import Thread

# from webcam_pulse_detector.lib.device import Camera
# from webcam_pulse_detector.lib.processors_noopenmdao import findFaceGetPulse
# from webcam_pulse_detector.lib.interface import plotXY, imshow, waitKey, destroyWindow
# from webcam_pulse_detector.get_pulse import getPulseApp
# import webcam_pulse_detector.get_pulse
# from get_pulse import *
import get_pulse

import cv2  # delete

import warnings
warnings.filterwarnings("ignore")


class GUI:
    def __init__(self, master):
        self.proc = FrameHelper()  # FrameHelper obj

        # self.buttons_state = [0, 0, 0]  # if pressed = 1
        self.label = ttk.Label(master, text="Some Welcome Label")
        self.label.grid(row=0, column=0, columnspan=3)
        self.label.config(font=('Ariel', 18, 'bold')) # font_name, size, extra (bold, underline..)

        # label = ttk.Label(root, text='Some Welcome Label', font=('Ariel', 18, 'bold'))
        # label.grid(row=0, column=0, columnspan=3)

        self.btn1 = ttk.Button(master, text="Center Pic")
        self.btn1.grid(row=1, column=0)
        self.btn1.config(command=self.find_center_pic_option)

        self.btn2 = ttk.Button(master, text='Center Vid')
        self.btn2.grid(row=1, column=1)
        self.btn2.config(command=self.center_motion_option)

        self.btn3 = ttk.Button(master, text='Pulse')
        self.btn3.grid(row=1, column=2)
        self.btn3.config(command=self.pulse_monitor_option)

    # this function disables the input button - there is no need to press it a second time
    def disable(self, btn):
        btn.config(state="disabled")
        print("Disabled the", btn['text'], "button.", sep=" ")
        '''
        for b in self.buttons_state:
            if b is 1:
                b.config(state="disabled")  # TODO: maybe self.b??
        # self.btn2.config(state="disabled")
        '''

    '''
    # the GUI need to run on the main process - a new thread is needed
    def threadTo_center_motion_option(self):
        self.disable(self.btn2)
        print("*** btn2 disabled ***")

        t = Thread(target=self.center_motion_option)
        t.start()
        # t.join()
    '''

    # runs samples videos and returns person with a circled center
    def center_motion_option(self):  # TODO no need for this func - delete line 51 and paste 58-64
        self.disable(self.btn2)
        print("*** btn2 disabled ***")

        # 2 threads for to 2 infinity loops
        t1 = Thread(target=self.proc.call_frame_processor)  # process the sample frame
        t2 = Thread(target=self.proc.show_vid)  # Shows the video
        #t1 = Thread(target=Process_vid.call_frame_processor)  # process the sample frame
        #t2 = Thread(target=Process_vid.show_vid)  # Shows the video

        t2.start()
        #cv2.waitKey(500)
        t1.start()

        # when the program ends kill threads
        # t1.join()
        # t2.join()

    # runs samples pictures and returns person with a circled center
    def find_center_pic_option(self):
        print("find_center__pic_option WAS NOT YET WRITEN")

    # NOT STATIC(?) do I need 'self' for connecting the precise time of the video?
    def pulse_monitor_option(self):
        # TODO: either disable btn3 or add a "close pulse option"
        App = get_pulse.getPulseApp()  # TODO: couses [ WARN:0] global C:\projects\opencv-python\opencv\modules\videoio\src\cap_msmf.cpp (436) `anonymous-namespace'::SourceReaderCB::~SourceReaderCB terminating async callback

        t3 = Thread(target=App.MY_main_loop)
        t3.start()


if __name__ == "__main__":

    root = Tk()  # Tk obj
    #proc = FrameHelper()  # FrameHelper obj
    run = GUI(root)  # GUI obj

    root.mainloop()

