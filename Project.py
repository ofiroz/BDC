import background_thread
from threading import Thread
import warnings
warnings.filterwarnings("ignore")
# import breath_dilation
from tkinter import * # now can use the name of stuff without the "tkinter."
from tkinter import ttk

buttons = [] # all the root buttons - for the disable func


class GUI:
    def __init__(self, master):

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
        self.btn2.config(command=self.threadTo_center_motion_option)

        self.btn3 = ttk.Button(master, text='Pulse')
        self.btn3.grid(row=1, column=2)
        self.btn3.config(command=self.pulse_monitor_option)

    # the GUI need to run on the main process - a new thread is needed
    def threadTo_center_motion_option(self):
        self.disable()
        print("*** btn2 disabled ***")

        t = Thread(target=self.center_motion_option)
        t.start()
        # t.join()

    # runs samples videos and returns person with a circled center
    def center_motion_option(self):
        # 2 threads for to 2 infinity loops
        t1 = Thread(target=background_thread.call_background_thread)
        t2 = Thread(target=background_thread.main_func)

        t2.start()
        t1.start()

        # when the program ends kill threads
        t1.join()
        t2.join()

    # this function disables button btn2 - there is no need to press it a second time
    # TODO: use the "buttons" list above to disable any btn - just pass the func the btn number
    def disable(self):
        self.btn2.config(state="disabled")

    # runs samples pictures and returns person with a circled center
    def find_center_pic_option(self):
        print("find_center__pic_option WAS NOT YET WRITEN")

    def pulse_monitor_option(self):
        print("pulse_monitor_option WAS NOT YET WRITEN")


if __name__ == "__main__":

    #root = init_GUI()
    root = Tk()
    run = GUI(root)
    root.mainloop()

    # showing_in_delay = Thread(target=background_thread.delay_video)
    # showing_in_delay.start()
