import cv2
import numpy as np
import glob
import threading
import re  # sort videos_name_list
from time import *  # for sleep


class FrameHelper(object):

    def __init__(self):
        self.prev_frame = np.zeros((10, 10))  # TODO for motion extraction
        self.curr_frame = np.zeros((10, 10))
        self.frame_output = np.zeros((10, 10))

        self.rotate = False

        self.videos_are_done = False
        self.vid_capture = []  # correct type?

        self.fps = 0  # needed?
        """
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        """
        # TODO: using the state option aloows only 1 btn at a time! not ideal..
        self.state = ''  # can be either pulse monitor/ breath monitor/ baby detection

        # self.buffer_size = 250  # needed?
        # self.window = np.hamming(self.buffer_size)
        # self.data_buffer = []  # needed?
        # self.freqs = []  # needed?
        # self.fft = []  # needed?

        self.cascade = 'haar_cascade_upperbody_24x24_20it_90pos_5m46sec.xml'
        # self.upper_body = cv2.CascadeClassifier('haarcascade_upperbody.xml')
        # self.full_body = cv2.CascadeClassifier('haarcascade_fullbody.xml')

        # self.rect = [1, 1, 2, 2]

        self.last_center = np.array([0, 0])  # usage in shift

        # TODO: for upper body cascade ill need to use the lower center of the ROI
        # TODO: ill monitor a ROI smaller then the original one
        self.new_xywh = 0, 0, 0, 0  # will pass to it the ROI every iteration - usage in shift

        self.idx = 1
        self.find_faces = True

    def two_sec_count(self):
        if self.videos_are_done:
            return
        print('Two seconds has passed')
        timer = threading.Timer(2, self.two_sec_count)  # Call `two_sec_count` in 2 seconds.
        timer.start()

    def call_frame_processor(self):
        # self.two_sec_count()  #TODO
        self.frame_processor()

    # calls check_for_person every 5 seconds
    def frame_processor(self):  # TODO not needed if using self. 
        print("frame_processor")
        '''
        while True:
            if self.videos_are_done:
                return
            # print('line 75')
            # print("========== Checking for person. will be back in 7-9 seconds ============")

            self.check_for_person()
        '''

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

            # TODO: using the state option aloows only 1 btn at a time! not ideal..
            '''
            if self.state == "baby detection":
                casc = self.get_ROI()  # get the ROI info using the cascades
                for (a, b, c, d) in casc:
                    self.draw_rect(a, b, c, d)  # draws the rect on the frame_output
            '''
            casc = self.get_ROI()  # get the ROI info using the cascades
            for (a, b, c, d) in casc:
                self.draw_rect(a, b, c, d)  # draws the rect on the frame_output

            cv2.imshow("tempered feed", self.frame_output)

            self.prev_frame = self.curr_frame

            # play the waitkey to reach real live movement rate
            if cv2.waitKey(20) == 27:
                break

        cv2.destroyAllWindows()
        self.vid_capture.release()

    # returns the ROI found with the cascade TODO: returns casc with potentially many ROIs
    def get_ROI(self):
        gray = cv2.cvtColor(self.curr_frame, cv2.COLOR_BGR2GRAY)
        Cascade = cv2.CascadeClassifier(self.cascade)  # TODO

        casc = Cascade.detectMultiScale(gray, 1.05, 5, minSize=(130, 130))  # minSize=(W, H) TODO
        '''
            scaleFactor 1.05 is a good possible value for this, which means you use a small step for resizing, 
            i.e. reduce size by 5%, you increase the chance of a matching size with the model for detection is found. 
            This also means that the algorithm works slower since it is more thorough. 
            You may increase it to as much as 1.4 for faster detection, with the risk of missing some faces altogether.
        '''
        # for (a, b, c, d) in casc:
        #    self.draw_rect(a, b, c, d)
        #    cv2.rectangle(img, (a, b), (a + c, b + d), (0, 255, 210), 4)
        return casc

    def draw_rect(self, x, y, w, h, color=(0, 255, 210), width=4):
        cv2.rectangle(self.frame_output, (x, y), (x + w, y + h), color, width)

    # fix the rectangle the the face location
    def shift(self):  # TODO: needed - find what detected is!
        x, y, w, h = self.new_xywh
        center = np.array([x + 0.5 * w, y + 0.5 * h])
        shift = np.linalg.norm(center - self.last_center)

        self.last_center = center
        return shift


# =========================================== TODO

"""
# checks for person in the frame every n seconds - uses person_center_new
def check_for_person():
    image_path = frame_sample[0]

    center, circle_radius = person_center_new.Center_coordinates(image_path)
    circle_radius = int(circle_radius)
    img = person_center_new.circle_center(image_path, center, circle_radius)

    # TODO: fixed plt colors issue
    # OpenCV represents RGB images as multi - dimensional NumPy arrays… but in reverse order!
    # need to do is convert the image from BGR to RGB
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.imshow(img, cmap='gray')
    plt.xticks([]), plt.yticks([])
    plt.show()

    # print("thread finished 'check_for_person'")


# test for timing - DELETE
def two_sec_count():
    # if all videos are done
    if done_all_videos[0] is 1:
        return
    print('Two seconds has passed')
    timer = threading.Timer(2, two_sec_count)  # Call `two_sec_count` in 2 seconds.
    timer.start()


def readVideo(video_name):
    capture = cv2.VideoCapture(video_name)  # 0 for camera OR video_name
    if capture is None:
        print("Failed to read the image")
        exit
    # resized_capture = resizeimage.resize_thumbnail(capture, [640, 360])

    return capture


# get one video -> deliver motion detection
def show_and_sample_frame(vid_name):
    cap = readVideo(vid_name)

    #    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    _, frame1 = cap.read()
    _, frame2 = cap.read()
    # print(frame1.shape)

    while cap.isOpened():
        # Major issue - SOLVED
        # returns an error while trying to read frames when video is over.
        if frame1 is None or frame2 is None:
            # print("success")
            return

        # ==================== Center Movement Detection ================================
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
        # ============================================================
        cv2.imshow("feed", frame1)

        # sample every 15th frame for person detection
        if flag_to_ten[0] == 1:
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)

            frame_sample[0] = frame1
            # print("15 frame has passed")

            flag_to_ten[0] = 15
        else:
            flag_to_ten[0] = flag_to_ten[0] - 1

        # cv2.imshow("feed", diff)
        # cv2.imshow("feed", dilated)

        frame1 = frame2
        _, frame2 = cap.read()

        # TODO: play the waitkey to reach real live movement rate
        if cv2.waitKey(40) == 27:
            break

    cv2.destroyAllWindows()
    cap.release()

'''
NOT IN USE
'''

# calls check_for_person every 5 seconds
def frame_processor():
    while True:
        # if all videos are done
        if done_all_videos[0] is 1:
            print("All Video Are Done - Thank You")
            return
        print("========== Checking for person. will be back in 7-9 seconds ============")
        check_for_person()

        # sleep(1)


def call_frame_processor():
    two_sec_count()
    frame_processor()


# get ALL videos
def show_vid():
    videos_name_list = []
    path = glob.glob('Video Samples/*.mp4')  # choose right format and location

    for f in path:  # check if gets names OR the videos (MP4)
        # print(tmp)
        videos_name_list.append(f)

    # show_and_sample_frame('Video Samples\sample9.mp4')
    for vid in videos_name_list:
        print('Video Path:', vid)  # video name
        show_and_sample_frame(vid)

    done_all_videos[0] = 1


"""
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

# ========= TODO: temp main for testing ===================

#App = FrameHelper()
#App.frame_input =


# ========= TODO: temp main for testing ===================
