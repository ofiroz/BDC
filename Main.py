from tkinter import *  # now can use the name of stuff without the "tkinter."
from tkinter import ttk
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
        self.flag_end = True  # if "Ctrl + e" is pressed it will be False

        self.menubutton = Menubutton(self.root, text="Menu")
        self.menubutton.menu = Menu(self.menubutton)
        self.menubutton["menu"] = self.menubutton.menu
        # TODO: write a regular menu without the checks + find what is IntVar() + add each menu option to a folder
        self.var1 = IntVar()
        self.var2 = IntVar()
        self.var3 = IntVar()

        self.menubutton.menu.add_checkbutton(label="open video folder", variable=self.var1)
        self.menubutton.menu.add_checkbutton(label="open logs folder", variable=self.var2)
        self.menubutton.menu.add_checkbutton(label="open cascades folder", variable=self.var3)
        self.menubutton.grid(row=0)

        # self.buttons_state = [0, 0, 0]  # if pressed = 1
        self.label = ttk.Label(self.root, text="Some Welcome Label")
        self.label.grid(row=1, column=0, columnspan=3)
        self.label.config(font=('Ariel', 18, 'bold')) # font_name, size, extra (bold, underline..)

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

    # This function disables the input button - there is no need to press it a second time
    def disable(self, btn):
        btn.config(state="disabled")
        print("Disabled the", btn['text'], "button.", sep=" ")

    # runs samples videos and returns person with a circled center
    def breath_detection(self):
        self.disable(self.btn2)
        # print("*** btn2 disabled ***")

        # 2 threads for to 2 infinity loops
        t1 = Thread(target=self.proc.call_frame_processor)  # process the sample frame
        t2 = Thread(target=self.proc.show_vid)  # Shows the video
        # t1 = Thread(target=Process_vid.call_frame_processor)  # process the sample frame
        # t2 = Thread(target=Process_vid.show_vid)  # Shows the video

        t2.start()
        # cv2.waitKey(500)
        t1.start()

        # when the program ends kill threads
        # t1.join()
        # t2.join()

    # runs samples pictures and returns person with a circled center
    def baby_detection(self):
        print("baby_detection WAS NOT YET WRITEN")

    def pulse_monitor(self):
        self.disable(self.btn3)
        # print("*** btn3 disabled ***")
        # TODO: solve the [ WARN:0]
        # TODO: cancel the camera 0 activation
        App = get_pulse.getPulseApp()

        t3 = Thread(target=App.MY_main_loop)
        t3.start()

    # Ctrl+e will end the program
    def end_program(self):
        print("FLAG updated to FALSE - closing program")
        self.flag_end = False


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
