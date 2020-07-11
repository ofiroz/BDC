import background_thread
from threading import Thread
import warnings
warnings.filterwarnings("ignore")
# import breath_dilation

# ========= GUI ============
from tkinter import * # now can use the name of stuff without the "tkinter."
from tkinter import ttk


def GUI():
    root = Tk()  # parent window

    label = ttk.Label(root, text='Some Welcome Label', font=('Ariel', 18, 'bold'))
    label.grid(row=0, column=0, columnspan=3)

    btn1 = ttk.Button(root, text="Center Pic")
    btn1.grid(row=1, column=0)
    btn1.config(command=find_center__pic_option)

    btn2 = ttk.Button(root, text='Center Vid')
    btn2.grid(row=1, column=1)
    btn2.config(command=threadTo_center_motion_option)

    btn3 = ttk.Button(root, text='Pulse')
    btn3.grid(row=1, column=2)
    btn3.config(command=pulse_monitor_option)

    return root
#===========================


def threadTo_center_motion_option():
    t = Thread(target=center_motion_option)
    t.start()
    # t.join()


def center_motion_option():
    # 2 threads for to 2 infinity loops
    t1 = Thread(target=background_thread.call_background_thread)
    t2 = Thread(target=background_thread.main_func)

    t2.start()
    t1.start()

    # when the program ends kill threads
    t1.join()
    t2.join()


def find_center__pic_option():
    print("find_center__pic_option WAS NOT YET WRITEN")


def pulse_monitor_option():
    print("pulse_monitor_option WAS NOT YET WRITEN")


if __name__ == "__main__":

    # TODO add tkinter GUI - 2 btns in root - breathing & pulse

    #center_motion_option()
    root = GUI()
    root.mainloop()
    # showing_in_delay = Thread(target=background_thread.delay_video)
    # showing_in_delay.start()
