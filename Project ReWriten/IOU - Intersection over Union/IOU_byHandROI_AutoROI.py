import cv2
import glob

'''
This class go through all the picture test samples (was NOT used to train the cascade) and:
1. allow the user to select the ROI by hand and save the coordinates, height and width of it to "byHand_info.txt"
2. using my frontal face cascade, select the ROI by save the coordinates, height and width of it to "auto_info.txt"
'''


def generate_both():
    lis = []
    path = glob.glob('./Testing_samples/*.jpg')

    for name in path:
        lis.append(name)
    # print(lis)
    byHand = open("./Files/byHand_info.txt", "x")
    auto = open("./Files/auto_info.txt", "x")

    for pic in lis:
        x1, y1, w1, h1, x2, y2, w2, h2 = work(pic)
        byHand.write("%s %s %s %s\n" % (x1, y1, w1, h1))
        auto.write("%s %s %s %s\n" % (x2, y2, w2, h2))

    byHand.close()
    auto.close()
    print("Done!")


def work(pic):
    face_casc = cv2.CascadeClassifier("./Files/haar_cascade_frontal_face_24x24_15it_85pos_39m15sec.xml")
    picture = cv2.imread(pic)
    # gray_pic = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)

    (x1, y1, w1, h1) = cv2.selectROI(picture)
    # print(x, y, w, h)

    gray = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
    casc = face_casc.detectMultiScale(gray, 1.05, 5, minSize=(100, 100))

    try:
        x2, y2, w2, h2 = casc[0]
    except:
        x2, y2, w2, h2 = 0, 0, 0, 0
        print("didnt find in: " + pic)

    return x1, y1, w1, h1, x2, y2, w2, h2


if __name__ == "__main__":

    generate_both()
