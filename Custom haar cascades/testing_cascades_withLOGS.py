import cv2
import time
import glob


''' not working.. not sorted
path = glob.glob('Cascades/*.xml') 
videos_name_list = []
for name in path: 
    videos_name_list.append(name)
print(videos_name_list)
cv2.waitKey(20000)
'''


Video_list = ['v1.mp4', 'v2.mp4', 'v3.mp4', 'v4.mp4', 'v5.mp4', 'v6.mp4', 'v7.mp4'
    , 'VIP_sample1.mp4', 'VIP_sample2.mp4', 'sample11.mp4']

OLD_Cascade_list = ['haarcascade_eliav.xml', 'haarcascade_eliav2.xml', 'haarcascade_eliav3.xml', 'haarcascade_eliav4.xml'
    , 'haarcascade_eliav5 24x44 15it.xml', 'haarcascade_eliav6 24x24 15it.xml', 'haarcascade_eliav7 24x24 20it.xml'
    , 'haarcascade_eliav8 20x20 20it.xml', 'haarcascade_eliav9 20x20 15it.xml']

Cascade_list = ['haarcascade_eliav1_44x24_15it.xml', 'haarcascade_eliav2_44x24_20it.xml'
    , 'haarcascade_eliav3_43x24_15it.xml', 'haarcascade_eliav4_43x24_20it.xml'
    , 'haarcascade_eliav5_37x20_15it.xml', 'haarcascade_eliav6_37x20_20it.xml'
    , 'haarcascade_eliav7_36x20_15it.xml', 'haarcascade_eliav8_36x20_20it.xml'
    , 'haarcascade_eliav9_28x15_15it.xml', 'haarcascade_eliav10_28x15_20it.xml'
    , 'haarcascade_eliav11_27x15_15it.xml', 'haarcascade_eliav12_27x15_20it.xml'
    , 'haarcascade_eliav13_24x24_15it.xml', 'haarcascade_eliav14_24x24_20it.xml'
    , 'haarcascade_eliav15_20x20_15it.xml', 'haarcascade_eliav16_20x20_20it.xml']


# test all videos with all cascades
def runLoop(video_list, cascade_list):

    start_time = time.time()

    log_num = 1
    for v in video_list:
        log = open("logs/log_file" + str(log_num) + ".txt", "w")  # will overwrite any existing file
        log.write("Logs from running all cascades an " + v + "\n====================================================\n")
        run_all_cascade(v, cascade_list, log)
        print(v + "  Finished\n")
        log.close()
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
        c = "Cascades/" + c  # grabbing the cascades from a folder
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

    cv2.imshow('feed', frame1)
    cv2.waitKey(300)

    start_time = time.time()

    while True:
        ret, img = cap.read()
        if img is None:
            return

        if rotate:
            img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # print(gray.shape)
        casc = Cascade.detectMultiScale(gray, 1.3, 2, minSize=(100, 100))  # minSize=(W, H) TODO

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


# work(Video_list[3], Cascade_list[1])  # working
# work(Video_list[4], Cascade_list[4])

runLoop(Video_list, Cascade_list)
