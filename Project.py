import cv2
import numpy as np
import glob


def readVideo(video_name):
    capture = cv2.VideoCapture(video_name)  # 0 for camera OR "WhatsApp Video 2020-01-23 at 16.21.02.mp4"
    if capture is None:
        print("Failed to read the image")
        exit
    return capture


# get one video -> deliver motion detection
def video_processing(vid_name):

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
        diff = cv2.absdiff(frame1, frame2)
        # print(frame1.shape)
        # print(frame2.shape)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 18, 255,
                                  cv2.THRESH_BINARY)  # thresh of 5 reconize breathing. 2 will reconize pulse!!

        dilated = cv2.dilate(thresh, None, iterations=3)

        # cv2.imshow("feed", dilated)

        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

            if cv2.contourArea(contour) < 1000:
                continue
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 150, 255), 2)
        # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

        cv2.imshow("feed", frame1)
        # cv2.imshow("feed", diff)
        # cv2.imshow("feed", dilated)

        frame1 = frame2
        _, frame2 = cap.read()

        if cv2.waitKey(40) == 27:
            break

    cv2.destroyAllWindows()
    cap.release()


# get ALL videos -> deliver motion detection
def main_func():
    videos_name_list = []
    path = glob.glob('videoSamples/*.mp4')  # choose right format and location

    for tmp in path:  # check if gets names OR the videos (MP4)
        # print(tmp)
        videos_name_list.append(tmp)

    for vid in videos_name_list:
        print(vid)
        video_processing(vid)


# ============== MAIN =============== #
# Breath recognition options
# 1. remove all big motions - dilate only breathing (only if tempo is correct)
# 2. focus on torso - dilate only torso

main_func()
