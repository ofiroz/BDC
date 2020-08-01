import cv2
import numpy as np
import glob
import threading
import person_center
from matplotlib import pyplot as plt
import queue
from time import * # for sleep

# sample_frame = cv2.imread(path) 'WhatsApp Image 2020-04-27 at 11.53.36.jpeg'

# flag to when all videos finished
done_all_videos = [0]

# flag to every 10 frames - use only flag_to_ten[0]
flag_to_ten = [15] #15 frames

# do I need a img in for the first cell?
tmp = cv2.imread('WhatsApp Image 2020-04-27 at 11.53.36.jpeg') # TODO: change to a logo image "starting program"
tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2RGB)
frame_sample = [tmp]

#global samp

# current frame queue
# Q = queue.Queue(maxsize=1)
# Q = queue.Queue()
# Q.put(tmp)  # end of queue flag - check if qsize > 1
# Q.put(tmp)

'''
# Q.get()
if Q.empty():
    print("empty")
if Q.full():
    print("full")
# Q.put(5)
print("f")
# Q.put(54)
# Q.put(53)
# print(Q.get())
print(Q.get())

if Q.empty() is True:
    print("empty")

if Q.full is True:
    print("full")
'''


# checks for person in the frame every n seconds - uses person_center
def check_for_person():
    # cv2.waitKey(2000)
    # print(sample)
    # image_path = 'WhatsApp Image 2020-04-25 at 09.29.42.jpeg'

    #image_path = frame_sample[0]
    '''
    if Q.empty():
        print("-----line 56 ------")
        return
        cv2.waitKey(2000)
    # image_path = Q.get()
    '''
    # print("---line62 - access to frame_sample[0]----")
    # image_path = frame_sample[0]
    '''
    try: # TODO: USELESS
        image_path = frame_sample[0]
    except:
        print("----samp is None----")
        image_path = cv2.imread('WhatsApp Image 2020-04-27 at 11.53.36.jpeg')
    '''
    image_path = frame_sample[0]

    center, circle_radius = person_center.Center_coordinates(image_path)
    circle_radius = int(circle_radius)
    img = person_center.circle_center(image_path, center, circle_radius)

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
    timer = threading.Timer(2, two_sec_count) # Call `two_sec_count` in 2 seconds.
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


def movement_detection(frame1, diff, min_x, max_x, min_y, max_y): # TODO OR (frame1, diff, radius, (centerX, centerY))
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
        print('Video Path:', vid) # video name
        show_and_sample_frame(vid)

    done_all_videos[0] = 1


# TODO
# ==============================================================================================
# showing a video in 8 seconds delay
'''
def delay_video():
    print("$$ will show in 20 seconds $$")
    sleep(20)
    print("$$ showing $$")
    show_and_sample_frame2('Video Samples/sample1.mp4')

def show_and_sample_frame2(vid_name):
    cap = readVideo(vid_name)
    _, frame1 = cap.read()
    _, frame2 = cap.read()
    while cap.isOpened():
        if frame1 is None or frame2 is None:
            # print("success")
            return
        cv2.imshow("feed in delay", frame1)
        frame1 = frame2
        _, frame2 = cap.read()

        if cv2.waitKey(40) == 27:
            break
    cv2.destroyAllWindows()
    cap.release()
'''
