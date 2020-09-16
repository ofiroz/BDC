from lib.processors_noopenmdao import findFaceGetPulse
from lib.interface import plotXY, imshow, waitKey, destroyWindow
from cv2 import moveWindow
import cv2
import sys


class getPulseApp(object):
    def __init__(self):
        self.w, self.h = 0, 0
        self.pressed = 0
        self.processor = findFaceGetPulse(bpm_limits=[50, 160],
                                          data_spike_limit=2500.,
                                          face_detector_smoothness=10.)
        # print(self.processor.dpath)

        self.flag_end = False  # if "Ctrl + e" is pressed on the GUI it will be True --> end program

        # Init parameters for the cardiac data plot
        self.bpm_plot = False
        self.plot_title = "Data display - raw signal (top) and PSD (bottom)"

        # Maps keystrokes to specified methods
        # (A GUI window must have focus for these to work)
        self.key_controls = {"s": self.toggle_search,
                             "d": self.toggle_display_plot}

    def toggle_search(self):
        state = self.processor.find_faces_toggle()  # change self.find_faces state - False/ True
        # print("face detection lock =", not state)

    def toggle_display_plot(self):
        if self.bpm_plot:
            print("bpm plot disabled")
            self.bpm_plot = False
            destroyWindow(self.plot_title)
        else:
            print("bpm plot enabled")
            if self.processor.find_faces:
                self.toggle_search()
            self.bpm_plot = True
            self.make_bpm_plot()
            moveWindow(self.plot_title, self.w, 0)

    def make_bpm_plot(self):
        """
        Creates and/or updates the data display
        """
        plotXY([[self.processor.times,
                 self.processor.samples],
                [self.processor.freqs,
                 self.processor.fft]],
               labels=[False, True],
               showmax=[False, "bpm"],
               label_ndigits=[0, 0],
               showmax_digits=[0, 1],
               skip=[3, 3],
               name=self.plot_title,
               bg=self.processor.slices[0])

    def key_handler(self):
        """
        Handle keystrokes, as set at the bottom of __init__()

        A plotting or camera frame window must have focus for keypresses to be
        detected.
        """
        self.pressed = waitKey(10) & 255  # wait for keypress for 10 ms
        if self.pressed == 27:  # exit program on 'esc'
            # TODO enable btn2/3 after Esc
            print("Exiting")
            sys.exit()

        for key in self.key_controls.keys():
            if chr(self.pressed) == key:
                self.key_controls[key]()

    def MY_main_loop(self):
        vid = r"Samples\Videos_Pulse\v6.mp4"  # can also use '/' without the raw flag...

        cap = cv2.VideoCapture(vid)

        while True:
            if self.flag_end is True:  # [x] OR Ctrl+e pressed in the GUI
                exit(0)

            _, frame = cap.read()

            if frame is None:
                print("Done running " + vid)
                exit(0)

            frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)

            self.h, self.w, _c = frame.shape
            # set current image frame to the processor's input
            self.processor.frame_in = frame
            # process the image frame to perform all needed analysis
            self.processor.run()
            # collect the output frame for display
            output_frame = self.processor.frame_out

            # show the processed/annotated output frame
            imshow("Processed", output_frame)

            # create and/or update the raw data display if needed
            if self.bpm_plot:
                self.make_bpm_plot()

            # handle any key presses
            self.key_handler()

            if cv2.waitKey(40) == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
