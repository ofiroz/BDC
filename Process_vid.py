import cv2
import numpy as np
import glob
import threading  # TODO: delete after deleting two_seconds
from threading import Thread
import re  # sort videos_name_list
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

# from time import *  # for sleep


class FrameHelper(object):
    def __init__(self):
        self.prev_frame = np.zeros((10, 10))  # for motion extraction
        self.curr_frame = np.zeros((10, 10))
        self.frame_output = np.zeros((10, 10))

        self.flag_end = False  # if "Ctrl + e" is pressed on the GUI it will be True --> end program

        self.rotate = False

        self.videos_are_done = False
        self.vid_capture = []

        self.fps = 0  # needed?
        """
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        """
        # using the state option allows only 1 btn at a time! not ideal..
        self.state = ''  # can be either pulse monitor/ breath monitor/ baby detection

        self.motivation_flag = False  # when True - compare me cascade to the official opencv one

        # self.upperB_or_face =
        self.cascade_upper_body = 'Data/Cascades/haar_cascade_upperbody_24x24_20it_90pos_5m46sec.xml'
        self.cascade_face = 'Data/Cascades/haar_cascade_frontal_face_24x24_15it_85pos_39m15sec.xml'
        self.official_haarcascade_upperbody = 'Data/Cascades/haarcascade_upperbody.xml'
        self.official_haarcascade_frontalface = 'Data/Cascades/haarcascade_frontalface_alt.xml'

        self.new_xywh = 0, 0, 0, 0  # will pass to it the ROI every iteration - usage in shift
        # self.center = np.array([0, 0])  # usage in shift ?
        self.center = 0, 0

        self.idx = 1

        # this flag will grow by 1 for every frame with no baby detected - after 90 frames (3sec) the ALERT will go off
        self.detected_counter = 0
        self.not_detected_pic = cv2.imread("Data/Error_pics/baby_not_found.jpg")

        # this flag will grow by 1 for every frame with a detected baby who doesnt breath - ALERT after 120 frames (4sec)
        self.breathing_counter = 0
        self.breathing_gone_pic = cv2.imread("Data/Error_pics/breathing_gone.jpg")

    # if the "motivation_flag" is True --> compare my cascade to the official opencv one
    def detect_from_pics(self, selected_casc):
        Cascade = cv2.CascadeClassifier(selected_casc)
        detected = []
        not_detected = []

        officialHAAR_motivation = []  # for motivation

        pic_set = []  # TODO: make a method to do this..
        path = glob.glob('Data/Samples/Pictures_Set/*.jpg')  # choose right format and location

        for name in path:
            pic_set.append(name)

        # TODO: output - two cv2 table: one with detected and one without
        for p in pic_set:
            flag = False  # is True if rect is found
            img = cv2.imread(p)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            casc = Cascade.detectMultiScale(gray, 1.05, 5, minSize=(130, 130))  # minSize=(W, H)

            for (a, b, c, d) in casc:
                cv2.rectangle(img, (a, b), (a + c, b + d), (0, 255, 210), 4)
                flag = True
            if flag is True:
                detected.append(img)
                continue
            not_detected.append(img)

            # ======= motivation ====================================
            if self.motivation_flag is True:
                mot_Cascade = cv2.CascadeClassifier(self.official_haarcascade_upperbody)
                mot_casc = mot_Cascade.detectMultiScale(gray, 1.05, 5, minSize=(100, 100))  # minSize=(W, H)

                for (a, b, c, d) in mot_casc:
                    cv2.rectangle(img, (a, b), (a + c, b + d), (0, 255, 210), 4)
                    officialHAAR_motivation.append(img)

        if self.motivation_flag is True:
            plt.figure('Motivation: using the original haarcascade_upperbody.xml')
            plot_mot = 331
            for n in officialHAAR_motivation:
                n = cv2.cvtColor(n, cv2.COLOR_BGR2RGB)  # convert from cv2(BGR) to plt(RGB)
                plt.subplot(plot_mot)
                plt.imshow(np.abs(n), cmap='gray')
                plt.xticks([]), plt.yticks([])
                plot_mot += 1
                # ======= motivation ====================================

        # plot_d = 221
        plot_d = 331
        plot_nd = 331
        plt.figure('Positive Detection')
        for n in detected:
            n = cv2.cvtColor(n, cv2.COLOR_BGR2RGB)  # convert from cv2(BGR) to plt(RGB)
            plt.subplot(plot_d)
            plt.imshow(np.abs(n), cmap='gray')
            plt.xticks([]), plt.yticks([])
            plot_d += 1

        plt.figure('Negative Detection')
        for n in not_detected:
            n = cv2.cvtColor(n, cv2.COLOR_BGR2RGB)  # convert from cv2(BGR) to plt(RGB)
            plt.subplot(plot_nd)
            plt.imshow(np.abs(n), cmap='gray')
            plt.xticks([]), plt.yticks([])
            plot_nd += 1

        self.motivation_flag = False
        try:
            plt.show()  # will close after end_program. added plt.close() in Main.py
            print("Done processing all {} pictures".format(len(pic_set)))
        except:
            print("please close all plots")
            return

    # shows the bad results with the opencv official frontal face Haar casc
    def motivation_pics(self):
        self.motivation_flag = True
        self.detect_from_pics(self.cascade_upper_body)
        self.motivation_flag = False

    # new thread to motivation_vid
    def motivation_vid_t(self):
        t = Thread(target=self.motivation_vid)
        t.start()

    # compare the results with my casc and the opencv casc
    def motivation_vid(self):
        my_casc = cv2.CascadeClassifier(self.cascade_face)
        official_face_cascade = cv2.CascadeClassifier(self.official_haarcascade_frontalface)
        video_src = "VIP_1.mp4"
        video_src2 = "v4.mp4"

        rotate = False
        rotate2 = False

        cap = cv2.VideoCapture(video_src)
        cap2 = cv2.VideoCapture(video_src2)
        _, frame1 = cap.read()
        hi, wi, _ = frame1.shape
        if hi < 400:
            rotate = True

        _, frame1 = cap2.read()
        hi, wi, _ = frame1.shape
        if hi < 400:
            rotate2 = True

        while True:
            if self.flag_end is True:  # [x] OR Ctrl+e pressed in the GUI
                exit(0)

            ret, img = cap.read()
            ret2, img3 = cap2.read()
            if img is None or img3 is None:
                break

            if rotate:
                img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
            if rotate2:
                img3 = cv2.rotate(img3, cv2.cv2.ROTATE_90_CLOCKWISE)

            img2 = img.copy()
            img4 = img3.copy()

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

            gray3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
            gray4 = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY)

            casc = my_casc.detectMultiScale(gray, 1.05, 5, minSize=(100, 100))
            casc2 = my_casc.detectMultiScale(gray3, 1.05, 5, minSize=(100, 100))
            official_casc = official_face_cascade.detectMultiScale(gray2, 1.05, 5, minSize=(100, 100))
            official_casc2 = official_face_cascade.detectMultiScale(gray4, 1.05, 5, minSize=(100, 100))

            for (a, b, c, d) in casc:
                cv2.rectangle(img, (a, b), (a + c, b + d), (0, 255, 210), 4)

            for (a, b, c, d) in casc2:
                cv2.rectangle(img3, (a, b), (a + c, b + d), (0, 255, 210), 4)

            for (x, y, z, w) in official_casc:
                cv2.rectangle(img2, (x, y), (x + z, y + w), (0, 255, 210), 4)

            for (x, y, z, w) in official_casc2:
                cv2.rectangle(img4, (x, y), (x + z, y + w), (0, 255, 210), 4)

            # cv2.imshow('feed', img)
            # cv2.imshow('feed_official', img2)

            cv2.imshow("1: My Cascade                                          VS                                          OpenCV Build-in Cascade (Face)", np.hstack([img, img2]))
            cv2.imshow("2: My Cascade                                          VS                                          OpenCV Build-in Cascade (Face)", np.hstack([img3, img4]))

            if cv2.waitKey(1) == 27:
                break
        # print("Done showing the deference in results between my custom cascade and the build-in cascade")
        cv2.destroyAllWindows()

    def two_sec_count(self):  # TODO
        if self.videos_are_done:
            return
        print('Two seconds has passed')
        timer = threading.Timer(2, self.two_sec_count)  # Call `two_sec_count` in 2 seconds.
        timer.start()

    # sort by the num in string
    def atoi(self, text):
        return int(text) if text.isdigit() else text

    # sort by the num in string
    def natural_keys(self, text):
        return [self.atoi(c) for c in re.split(r'(\d+)', text)]

    # initialize the frames every video
    def init(self):
        self.curr_frame = np.zeros((10, 10))
        self.prev_frame = np.zeros((10, 10))
        self.frame_output = np.zeros((10, 10))

    def rotate_frames(self):
        self.curr_frame = cv2.rotate(self.curr_frame, cv2.cv2.ROTATE_90_CLOCKWISE)
        self.prev_frame = cv2.rotate(self.prev_frame, cv2.cv2.ROTATE_90_CLOCKWISE)
        self.frame_output = cv2.rotate(self.frame_output, cv2.cv2.ROTATE_90_CLOCKWISE)

    # active the process on every video by order
    def show_vid(self, selected_casc):
        videos_name_list = []
        path = glob.glob(r'Data\Samples\Baby_Detection_Videos\*.mp4')

        for name in path:  # check if gets names OR the videos (MP4)
            videos_name_list.append(name)
        # print(videos_name_list)
        # videos_name_list = sorted(videos_name_list)  # sorted OR sort(a12, a11, a2, a10) = (a10, a11, a12, a2)
        videos_name_list.sort(key=self.natural_keys)  # sort by the num in string
        # print(videos_name_list)

        for vid in videos_name_list:
            # print('Video Path:', vid)  # video name
            if self.state == 'breathing detection':
                if vid == r"Data\Samples\Baby_Detection_Videos\v1.mp4":  # not the best results for respiratory detection TODO more vid
                    continue
            # print(vid)
            self.show_feed(vid, selected_casc)

        self.videos_are_done = True
        print("All Video Are Done - Thank You")

    # get one video -> deliver motion detection
    def show_feed(self, vid_name, selected_casc):
        self.vid_capture = cv2.VideoCapture(vid_name)  # 0 for camera OR video_name
        if self.vid_capture is None:
            print("Failed to read the video")
            exit

        _, self.prev_frame = self.vid_capture.read()
        hi, wi, _ = self.prev_frame.shape
        if hi == 352:
            self.rotate = True

        # resized_capture = resizeimage.resize_thumbnail(capture, [640, 360])
        # frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # breathing detection
        feature_params = dict(maxCorners=300, qualityLevel=0.2, minDistance=5, blockSize=7)
        lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        color = (0, 255, 0)
        f = self.prev_frame
        f = cv2.rotate(f, cv2.cv2.ROTATE_90_CLOCKWISE)
        prev_gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        my_mask = np.zeros_like(prev_gray)
        my_mask[150:200, 100:200] = 255  # ROI coordinates
        prev = cv2.goodFeaturesToTrack(prev_gray, mask=my_mask, **feature_params)
        mask = np.zeros_like(f)
        # breathing detection

        while self.vid_capture.isOpened():
            if self.flag_end is True:  # [x] OR Ctrl+e pressed in the GUI
                exit(0)
            # Major issue - SOLVED
            # returns an error while trying to read frames when video is over.
            _, self.curr_frame = self.vid_capture.read()
            if self.curr_frame is None or self.prev_frame is None:
                # print("ERROR ~ line 220")
                self.init()
                return

            self.frame_output = self.curr_frame  # only for rotate_frame
            if self.rotate:
                self.rotate_frames()

            cv2.imshow("original feed", self.curr_frame)

            casc = self.get_ROI(selected_casc)  # get the ROI info using the cascades

            # breathing detection
            if self.state == 'breathing detection':
                f = self.curr_frame
                gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
                frame_num = self.vid_capture.get(cv2.CAP_PROP_POS_FRAMES)

                # if int(frame_num) % 250 == 0:  # calc goodFeaturesToTrack every 5-6 seconds
                if int(frame_num) % 200 == 0:  # calc goodFeaturesToTrack every 5-6 seconds
                    prev = cv2.goodFeaturesToTrack(prev_gray, mask=my_mask, **feature_params)
                nxt, status, error = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev, None, **lk_params)

                good_old = prev[status == 1]
                good_new = nxt[status == 1]

                if np.array_equal(good_old, good_new):
                    self.breathing_counter = self.breathing_counter + 1
                    if self.breathing_counter == 120:  # of no breathing found for more than 4 seconds
                        self.breathing_alert()
                else:
                    self.breathing_counter = 0
                    cv2.destroyWindow("error")

                for i, (new, old) in enumerate(zip(good_new, good_old)):
                    a, b = new.ravel()
                    f = cv2.circle(f, (a, b), 3, color, -1)
                self.frame_output = cv2.add(f, mask)
                prev_gray = gray.copy()
                prev = good_new.reshape(-1, 1, 2)

                for (a, b, c, d) in casc:
                    # self.draw_rect(a, b, c, d)
                    my_mask[b+150:b+d-30, a:a+c] = 255  # ROI coordinates
                    self.detected_counter = 0
                    cv2.destroyWindow("error")

                cv2.imshow("original feed", self.frame_output)
            # breathing detection

            # baby detection
            if self.state == 'baby detection':
                # casc = self.get_ROI(selected_casc)  # get the ROI info using the cascades
                for (a, b, c, d) in casc:
                    self.draw_rect(a, b, c, d)  # draws the rect on the frame_output
                    self.center = a+c/2, b  # (x+w/2,y) update the lower center of the detected ROI
                    self.new_xywh = a, b, c, d
                    self.detected_counter = 0
                    cv2.destroyWindow("error")
                    # cv2.imshow("tempered feed", self.frame_output)
                cv2.imshow("original feed", self.frame_output)  # shows only the tempered frame
            # baby detection
            self.prev_frame = self.curr_frame

            if len(casc) == 0:  # for every empty casc == no detection add 1 to the counter until 90
                self.detected_counter = self.detected_counter + 1
                if self.detected_counter == 90:
                    self.detection_alert()  # baby was not detected for more than 3 seconds! ALERT

            # play the wait key to reach real live movement rate
            if cv2.waitKey(20) == 27:
                break

        cv2.destroyAllWindows()
        self.vid_capture.release()

    # returns the ROI found with the cascade
    # returns casc with potentially many ROIs
    def get_ROI(self, selected_casc):
        gray = cv2.cvtColor(self.curr_frame, cv2.COLOR_BGR2GRAY)
        Cascade = cv2.CascadeClassifier(selected_casc)
        '''
        scaleFactor 1.05 is a good possible value for this, which means you use a small step for resizing, 
        i.e. reduce size by 5%, you increase the chance of a matching size with the model for detection is found. 
        This also means that the algorithm works slower since it is more thorough. 
        You may increase it to as much as 1.4 for faster detection, with the risk of missing some faces altogether.
        '''
        casc = Cascade.detectMultiScale(gray, 1.05, 5, minSize=(100, 100))  # minSize=(W, H)
        return casc

    def draw_rect(self, x, y, w, h, color=(0, 255, 210), width=4):
        cv2.rectangle(self.frame_output, (x, y), (x + w, y + h), color, width)

    # the flag will grow by 1 for every frame with no baby detected - after 90 frames (3sec) the ALERT will go off
    def detection_alert(self):
        print("baby was not found")
        cv2.imshow("error", self.not_detected_pic)

    # the flag will grow by 1 for every frame with a detected baby who doesnt breath - ALERT after 120 frames (4sec)
    def breathing_alert(self):
        print("breathing was not found")
        cv2.imshow("error", self.breathing_gone_pic)
