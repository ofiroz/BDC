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
        self.vid_capture = []  # correct type?

        self.fps = 0  # needed?
        """
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        """
        # using the state option allows only 1 btn at a time! not ideal..
        self.state = ''  # can be either pulse monitor/ breath monitor/ baby detection

        self.motivation_flag = False  # when True - compare me cascade to the official opencv one

        self.cascade_upper_body = 'haar_cascade_upperbody_24x24_20it_90pos_5m46sec.xml'
        self.cascade_face = 'haar_cascade_frontal_face_24x24_15it_85pos_39m15sec.xml'
        self.official_haarcascade_upperbody = 'haarcascade_upperbody.xml'
        self.official_haarcascade_frontalface = 'haarcascade_frontalface_alt.xml'

        # TODO: for upper body cascade ill need to use the lower center of the ROI (x+w/2,y)
        # TODO: ill monitor a ROI smaller then the original one
        self.new_xywh = 0, 0, 0, 0  # will pass to it the ROI every iteration - usage in shift
        # self.center = np.array([0, 0])  # usage in shift ?
        self.center = 0, 0

        self.idx = 1
        self.find_faces = True

    # the first option in the GUI
    # if the "motivation_flag" is True --> compare my cascade to the official opencv one
    def detect_from_pics(self):
        Cascade = cv2.CascadeClassifier(self.cascade_upper_body)
        detected = []
        not_detected = []

        officialHAAR_motivation = []  # for motivation

        pic_set = []  # TODO: make a method to do this..
        path = glob.glob('Pictures_Set/*.jpg')  # choose right format and location

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
            plt.figure('Motivation: using haarcascade_upperbody.xml')
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
        plt.figure('Positive')
        for n in detected:
            n = cv2.cvtColor(n, cv2.COLOR_BGR2RGB)  # convert from cv2(BGR) to plt(RGB)
            plt.subplot(plot_d)
            plt.imshow(np.abs(n), cmap='gray')
            plt.xticks([]), plt.yticks([])
            plot_d += 1

        plt.figure('Negative')
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
        self.detect_from_pics()
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
        # video_src2 = "VIP_sample2.mp4"
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

            cv2.imshow("1: My Cascade VS OpenCV Build-in Cascade (Face)", np.hstack([img, img2]))
            cv2.imshow("2: My Cascade VS OpenCV Build-in Cascade (Face)", np.hstack([img3, img4]))

            if cv2.waitKey(1) == 27:
                break
        # print("Done showing the deference in results between my custom cascade and the build-in cascade")
        cv2.destroyAllWindows()

    def two_sec_count(self):
        if self.videos_are_done:
            return
        print('Two seconds has passed')
        timer = threading.Timer(2, self.two_sec_count)  # Call `two_sec_count` in 2 seconds.
        timer.start()

    def call_frame_processor(self):  # useless
        # self.two_sec_count()  #TODO
        self.frame_processor()

    # calls check_for_person every 5 seconds
    def frame_processor(self):  # TODO not needed if using self.
        print("frame_processor is useless")


    '''
    def check_for_person(self):
        # center, circle_radius = person_center_new.Center_coordinates(self.curr_frame)
        # center, circle_radius =
        self.center_coordinates()
        # circle_radius = int(circle_radius)
        # print("center: ",center,"circle_radius: ",circle_radius, sep=" ")

        # self.frame_output = person_center_new.circle_center(self.curr_frame, center, circle_radius)
        # self.circle_center(center, circle_radius)

        # TODO: fixed plt colors issue
        # OpenCV represents RGB images as multi - dimensional NumPy arrays… but in reverse order!
        # need to do is convert the image from BGR to RGB
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        try:
            plt.imshow(self.frame_output, cmap='gray')
            plt.xticks([]), plt.yticks([])
            plt.show()
        except:
            print("ERROR in line 99")
        # print("thread finished 'check_for_person'")

    # this function detect a person (uses ML model)
    # finds the person's location and it's center
    # returns the center's coordinates
    def center_coordinates(self):
        model = core.Model()
        # print(model.predict_top(image))
        # person_is_found = 0
        try:
            labels, boxes, scores = model.predict_top(self.curr_frame)
            min_x = 0
            min_y = 0
            max_x = 0
            max_y = 0

            for lbl, box in zip(labels, boxes):  # zip stops when the shorter list is finished
                if lbl is "person":
                    # print(type(box)) # finding the person's box
                    a, b, c, d = box  # a,b,c,d are "torch.Tensor" objects
                    min_x = int(a)
                    min_y = int(b)
                    max_x = int(c)
                    max_y = int(d)
                    # print(min_x, min_y, max_x, max_y)
                    # print("person HAS BEEN found")
                    break
        except:
            # if no person has been found
            print("&&&&&&&&&&&& NO person found &&&&&&&&&&&&")
            return (0, 0), 0

        # calculate main vector length, radius = (main vector length) * 0.2
        radius = (((max_x - min_x) ** 2 + (max_y - min_y) ** 2) ** 0.5) * 0.2
        radius = int(radius)
        # print(radius)

        center_x = int((max_x + min_x) / 2)
        center_y = int((max_y + min_y) / 2)
        # print(center_X, center_y)
        center_coordinates = (center_x, center_y)

        # visualize.show_labeled_image(image, boxes, labels)

        # CAN RETURN A CROPPED PERSON
        # img = cv2.imread(image_path)
        # crop_img = img[min_y:max_y, min_x:max_x]
        # cv2.imshow("cropped", crop_img)
        # cv2.waitKey(0)
        # return crop_img, center_coordinates


        cv2.circle(self.frame_output, center_coordinates, radius, (0, 0, 255), 10)
        return  # center_coordinates, radius
    '''

    # TODO circle_center
    '''
    def circle_center(self, center_coordinates, radius):
        # image = cv2.imread(image_path)
        try:
            cv2.circle(self.frame_output, center_coordinates, radius, (0, 0, 255), 10)
            return
        except:
            print("**** failed in circle_center - no person was found**************")  # TODO: DELETE
            # cv2.waitKey(900000000)
        return # cv2.imread('ttt.JPG')  # TODO: add FAILED img
    '''
    # TODO circle_center
    # ======================================================================================================================

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
    def show_vid(self):
        videos_name_list = []
        path = glob.glob('Video Samples/*.mp4')  # choose right format and location

        for name in path:  # check if gets names OR the videos (MP4)
            videos_name_list.append(name)
        # print(videos_name_list)
        # videos_name_list = sorted(videos_name_list)  # sorted OR sort(a12, a11, a2, a10) = (a10, a11, a12, a2)
        videos_name_list.sort(key=self.natural_keys)  # sort by the num in string
        # print(videos_name_list)

        for vid in videos_name_list:
            print('Video Path:', vid)  # video name
            self.show_feed(vid)

        self.videos_are_done = True
        print("All Video Are Done - Thank You")

    # get one video -> deliver motion detection
    def show_feed(self, vid_name):
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

            # =========== Center Movement Detection ================================
            '''
            diff = cv2.absdiff(frame1, frame2)
            # print(frame1.shape)
            # print(frame2.shape)

            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            # TODO the Threshhold says- every pixel of the diff higher than 18 - become 255 (white)
            _, thresh = cv2.threshold(blur, 18, 255,
                                      cv2.THRESH_BINARY)  # thresh of 5 reconize breathing. 2 will reconize pulse!!

            dilated = cv2.dilate(thresh, None, iterations=3)

            # cv2.imshow("feed", dilated)

            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)

                if cv2.contourArea(contour) < 1000:
                    continue
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 150, 255), 2) # enlarge the image in the rectangle
                #cv2.circle(frame1, (w/2, h/2), 30, (0, 150, 255), 2)
                # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
            '''
            # =========== Center Movement Detection ================================

            cv2.imshow("original feed", self.curr_frame)

            if self.state == 'baby detection':
                casc = self.get_ROI()  # get the ROI info using the cascades
                for (a, b, c, d) in casc:
                    self.draw_rect(a, b, c, d)  # draws the rect on the frame_output
                    self.center = a+c/2, b  # (x+w/2,y) update the lower center of the detected ROI
                    self.new_xywh = a, b, c, d
                cv2.imshow("tempered feed", self.frame_output)

            self.prev_frame = self.curr_frame

            # play the wait key to reach real live movement rate
            if cv2.waitKey(20) == 27:
                break

        cv2.destroyAllWindows()
        self.vid_capture.release()

    # returns the ROI found with the cascade
    # returns casc with potentially many ROIs
    def get_ROI(self):
        gray = cv2.cvtColor(self.curr_frame, cv2.COLOR_BGR2GRAY)
        Cascade = cv2.CascadeClassifier(self.cascade_upper_body)
        '''
        scaleFactor 1.05 is a good possible value for this, which means you use a small step for resizing, 
        i.e. reduce size by 5%, you increase the chance of a matching size with the model for detection is found. 
        This also means that the algorithm works slower since it is more thorough. 
        You may increase it to as much as 1.4 for faster detection, with the risk of missing some faces altogether.
        '''
        casc = Cascade.detectMultiScale(gray, 1.05, 5, minSize=(130, 130))  # minSize=(W, H)
        return casc

    def draw_rect(self, x, y, w, h, color=(0, 255, 210), width=4):
        cv2.rectangle(self.frame_output, (x, y), (x + w, y + h), color, width)

    '''
    # fix the rectangle the the face location
    def shift(self):  # TODO: needed?
        x, y, w, h = self.new_xywh
        new_center = np.array([x + 0.5 * w, y + 0.5 * h])
        shift = np.linalg.norm(new_center - self.center)

        self.center = new_center
        return shift
    '''

'''
def movement_detection(frame1, diff, min_x, max_x, min_y, max_y):  # TODO OR (frame1, diff, radius, (centerX, centerY))
    # ==================== Center Movement Detection ================================
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # TODO the Threshhold says- every pixel of the diff higher than 18 - become 255 (white)
    _, thresh = cv2.threshold(blur, 18, 255,
                              cv2.THRESH_BINARY)  # thresh of 5 reconize breathing. 2 will reconize pulse!!

    dilated = cv2.dilate(thresh, None, iterations=3)

    # cv2.imshow("feed", dilated)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 1000:
            continue
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 150, 255), 2)  # enlarge the image in the rectangle
        # cv2.circle(frame1, (w/2, h/2), 30, (0, 150, 255), 2)
        # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    # ============================================================
'''


