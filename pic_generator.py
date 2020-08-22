import cv2
import glob
import math
import time

# TODO: there must be a "test_images" folder with the .py file

'''
# this func gets a set of videos and extract a frame every second from each video.
# with is I have created my cascade learning pictures set (positive & negative)
def generator():
    videos_name_list = []
    path = glob.glob('*.mp4')  # choose right format and location

    for name in path:  # check if gets names OR the videos (MP4)
        videos_name_list.append(name)

    print(videos_name_list)

    a = 1  # added to the image name to uniq it
    for vid in videos_name_list:
        print('Video Path:', vid)  # video name
        write_pic_every_second(vid, a)
        a += 1
    print("Done!")


def write_pic_every_second(vid, a):
    videoFile = vid
    rotate = False
    cap = cv2.VideoCapture(videoFile)
    frameRate = cap.get(5)  # frame rate
    x = 1

    ret1, frame1 = cap.read()
    hi, wi, _ = frame1.shape
    if hi == 352:
        rotate = True
    # print(frame1.shape)

    while cap.isOpened():
        frameId = cap.get(1)  # current frame number
        ret, frame = cap.read()
        if ret != True:
            break

        if rotate:
            frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)

        if frameId % math.floor(frameRate) == 0:
            filename = './test_images/image' + str(a) + str(int(x)) + ".jpg"
            x += 1
            cv2.imwrite(filename, frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(40) == 27:
            break

    cap.release()
'''
# TODO: second part - convert to gray pics and fix name ================================================================

'''
# picked pictures from many sources.. need to convert to gray pics & fix to naming convention
def generator_gray():
    pictures_name_list = []
    path = glob.glob('*.jpg')  # choose right format and location

    for name in path:
        pictures_name_list.append(name)

    # print(pictures_name_list)

    a = 1  # added to the image name to uniq it
    for pic in pictures_name_list:
        a = fix(pic, a)

    print("Done!")


def fix(pic, a):
    picture = cv2.imread(pic)
    gray_pic = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
    gray_pic = picture  # TODO: fix names ONLY
    filename = './test_images/' + str(int(a)) + ".jpg"
    cv2.imwrite(filename, gray_pic)
    a += 1
    return a
'''


# TODO: third part - Extract from vid + convert to gray and fix name + generates 2 pics - reg and mirror ===============
def generator_all_together():
    start_time = time.time()

    videos_name_list = []
    path = glob.glob('*.mp4')  # choose right format and location

    for name in path:  # check if gets names OR the videos (MP4)
        videos_name_list.append(name)

    print(videos_name_list)

    a = 1  # TODO added to the image name to uniq it
    for vid in videos_name_list:
        print('Video Path:', vid)  # video name
        a = write_gray_pic_every_second(vid, a)

    t_pass = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
    print("\nDone after " + t_pass)


# generates 2 gray pics - reg and mirror
def write_gray_pic_every_second(vid, a):
    videoFile = vid
    rotate = False
    cap = cv2.VideoCapture(videoFile)
    frameRate = cap.get(5)  # frames per second = 29.9332

    # fps = cap.get(cv2.CAP_PROP_FPS)
    # print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))  # ==print(cap.get(5))
    # print(cap.get(5))
    # print(cap.get(0))  # returns the time in video in milliseconds

    ret1, frame1 = cap.read()
    hi, wi, _ = frame1.shape
    if hi == 352:
        rotate = True
    # print(frame1.shape)

    while cap.isOpened():
        frameId = cap.get(1)  # current frame number
        ret, frame = cap.read()
        if ret is None:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if rotate:
            frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)

        # if frameId % math.floor(frameRate) == 0:  # every ~29 frames
        if frameId % math.floor(frameRate) == 0 or frameId % math.floor(frameRate) == 15:  # every ~15 frame - 2 per sec
            filename = './test_images/image' + str(a) + ".jpg"
            # filename = './n_nums_no_mirror/' + str(a) + ".jpg"   # TODO mirror
            # filename = './n_mirror_nums/' + str(c) + ".jpg"  # TODO delete
            # filename = './n_mirror_nums/' + str(a) + ".jpg"  # TODO delete

            cv2.imwrite(filename, frame)
            # cv2.imwrite(filename1, frame)  # TODO delete

            # b = a + 1   # TODO mirror
            # mirror_filename = './test_images/image' + str(b) + ".jpg"   # TODO mirror
            # mirror_filename = './n_mirror_nums/' + str(b) + ".jpg"
            # mirror_frame = cv2.flip(frame, 1)  # will be saved as a mirror (horizontal flip) pic of frame
            # cv2.imwrite(mirror_filename, mirror_frame)   # TODO mirror
            # a += 2   # TODO mirror
            a += 1
        cv2.imshow('frame', frame)
        if cv2.waitKey(40) == 27:
            break
    cap.release()
    return a


if __name__ == "__main__":
    # generator()
    # generator_gray()
    generator_all_together()

