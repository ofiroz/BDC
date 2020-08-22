import cv2
import time
import glob


def get_cascade_list():
    cascade_list = []
    path = glob.glob('Cascades/*.xml')  # choose right format and location
    for name in path:  # check if gets names OR the videos (MP4)
        cascade_list.append(name)
    return cascade_list


def get_vid_list():
    vid_list = []
    path = glob.glob('Videos/*.mp4')  # choose right format and location
    for name in path:  # check if gets names OR the videos (MP4)
        vid_list.append(name)
    return vid_list


# test all videos with all cascades
def runLoop():
    cascade_list = get_cascade_list()
    video_list = get_vid_list()
    start_time = time.time()

    log_num = 1
    for v in video_list:
        log = open("logs/log_file" + str(log_num) + ".txt", "w")  # will overwrite any existing file
        log.write("Logs from running all cascades an " + v + "\n====================================================\n")
        run_all_cascade(v, cascade_list, log)
        print(v + "  Finished\n")
        log.close()
        print("logs file for " + v + "  was generated successfully\n")
        log_num += 1
        # log.write("\n" + v + "  Finished")
    t_pass = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
    print("\nDone running all videos after " + t_pass + " seconds")
    # log.write("\nDone running all videos")
    # log.close()


# run all cascades on 1 video
def run_all_cascade(vid, cascade_list, log):
    for c in cascade_list:
        log.write("\n Start testing cascade: " + c)
        # print(c)
        # c = "Cascades/" + c  # grabbing the cascades from a folder
        # print(c)
        work(vid, c, log)
        # print("\nDone cascade " + c + "\n")
        log.write("\n   Done testing cascade: " + c + "\n")

    print("\nDone running all cascade on " + vid)
    log.write("\nDone running all cascade on " + vid)


# run a video with a cascade
def work(video_src, cascade, log):

    Cascade = cv2.CascadeClassifier(cascade)

    rotate = False

    cap = cv2.VideoCapture(video_src)
    ret1, frame1 = cap.read()
    hi, wi, _ = frame1.shape
    # print(frame1.shape)
    if hi == 352:
        rotate = True

    cv2.imshow('feed', frame1)  # show the video original shape
    cv2.waitKey(200)

    start_time = time.time()

    while True:
        ret, img = cap.read()
        if img is None:
            return

        if rotate:
            img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # print(gray.shape)
        #casc = Cascade.detectMultiScale(gray, 1.3, 2, minSize=(100, 100))  # minSize=(W, H) TODO
        casc = Cascade.detectMultiScale(gray, 1.05, 5, minSize=(130, 130))  # minSize=(W, H) TODO

        '''
        scaleFactor 1.05 is a good possible value for this, which means you use a small step for resizing, i.e. reduce size by 5%, you increase the chance of a matching size with the model for detection is found. This also means that the algorithm works slower since it is more thorough. You may increase it to as much as 1.4 for faster detection, with the risk of missing some faces altogether.
        '''

        for (a, b, c, d) in casc:
            cv2.rectangle(img, (a, b), (a + c, b + d), (0, 255, 210), 4)

            t_pass = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))  # the time passes from start
            print("GOT ONE in " + video_src + " with " + cascade + " at " + t_pass
                  + "!!! Height: " + str(d) + "  Width: " + str(c))
            log.write("\nGOT ONE in " + video_src + " with " + cascade + " at " + t_pass
                  + "!!! Height: " + str(d) + "  Width: " + str(c))
            # print("GOT ONE!!! a: " + str(a) + "  b: " + str(b) + "  c: " + str(c) + "  d: " + str(d))
            # print("GOT ONE!!! (a, b): (" + str(a) + ", " + str(b) + ")||  (a + c, b + d): ("
            #      + str(a+c) + ", " + str(b+d) + ")")

        cv2.imshow('feed', img)

        if cv2.waitKey(33) == 27:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    # work(Video_list[3], Cascade_list[1])  # working
    # work(Video_list[4], Cascade_list[4])

    # runLoop(Video_list, OLD_Cascade_list)

    runLoop()
