from webcam_pulse_detector.lib.device import Camera
from webcam_pulse_detector.lib.processors_noopenmdao import findFaceGetPulse
from webcam_pulse_detector.lib.interface import plotXY, imshow, waitKey, destroyWindow
from cv2 import moveWindow
import cv2
import argparse
import numpy as np
import datetime
# import socket #TODO disabled it
import sys

#import warnings
#warnings.filterwarnings("ignore")

class getPulseApp(object):
    def __init__(self):
        self.cameras = []
        self.selected_cam = 0
        for i in range(3):
            camera = Camera(camera=i)  # first camera by default
            if camera.valid or not len(self.cameras):
                self.cameras.append(camera)
            else:
                break
        self.w, self.h = 0, 0
        self.pressed = 0
        self.processor = findFaceGetPulse(bpm_limits=[50, 160],
                                          data_spike_limit=2500.,
                                          face_detector_smoothness=10.)

        # Init parameters for the cardiac data plot
        self.bpm_plot = False
        self.plot_title = "Data display - raw signal (top) and PSD (bottom)"

        # Maps keystrokes to specified methods
        # (A GUI window must have focus for these to work)
        self.key_controls = {"s": self.toggle_search,
                             "d": self.toggle_display_plot,
                             # "f": self.write_csv,   # TODO: I disabled it - needed for anything else? maybe closing?
                             "c": self.toggle_cam}

    def toggle_cam(self):
        if len(self.cameras) > 1:
            self.processor.find_faces = True
            self.bpm_plot = False
            destroyWindow(self.plot_title)
            self.selected_cam += 1
            self.selected_cam = self.selected_cam % len(self.cameras)

    def toggle_search(self):
        # state = self.processor.find_faces.toggle()
        state = self.processor.find_faces_toggle()  # change self.find_faces state - False/ True
        print("face detection lock =", not state)

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
            print("Exiting")
            for cam in self.cameras:
                cam.cam.release()
            # if self.send_serial:
            #   self.serial.close()
            sys.exit()

        for key in self.key_controls.keys():
            if chr(self.pressed) == key:
                self.key_controls[key]()

    def main_loop(self):
        # Get current image frame from the camera
        frame = self.cameras[self.selected_cam].get_frame()
        self.h, self.w, _c = frame.shape

        # display unaltered frame
        # imshow("Original",frame)

        # set current image frame to the processor's input
        self.processor.frame_in = frame
        # process the image frame to perform all needed analysis
        self.processor.run(self.selected_cam)
        # collect the output frame for display
        output_frame = self.processor.frame_out

        # show the processed/annotated output frame
        imshow("Processed", output_frame)

        # create and/or update the raw data display if needed
        if self.bpm_plot:
            self.make_bpm_plot()
        # handle any key presses
        self.key_handler()

    # TODO: my change
    def MY_main_loop(self):
        cap = cv2.VideoCapture("pulseVid.mp4")

        while True:
            # Capture frame-by-frame
            _, frame = cap.read()

            if frame is None:
                exit(0)

            frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)

            # frame = self.cameras[self.selected_cam].get_frame()
            self.h, self.w, _c = frame.shape

            # display unaltered frame
            # imshow("Original",frame)

            # self.selected_cam = 0  # TODO - if unnotted it work fine! look at the TODO below

            # set current image frame to the processor's input
            self.processor.frame_in = frame
            # process the image frame to perform all needed analysis
            self.processor.run(self.selected_cam)  # TODO: if camera changed to '0' -> might be useful
            # collect the output frame for display
            output_frame = self.processor.frame_out

            # show the processed/annotated output frame
            imshow("Processed", output_frame)

            # create and/or update the raw data display if needed
            if self.bpm_plot:
                self.make_bpm_plot()

            # handle any key presses
            self.key_handler()

            # Display the resulting frame
            # cv2.imshow('frame', frame)

            # TODO: play the waitkey to reach real live movement rate
            if cv2.waitKey(40) == 27:
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
