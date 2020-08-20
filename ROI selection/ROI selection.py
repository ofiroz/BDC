import cv2
import glob

'''
This class go through all the frames after ROI selection (manual) generate two samples
1. pos with ROI
2. neg with background with black rect on the ROI 

GOALS:
1. sample 100 samples and save every ROI coordinates
2. average the rect size and get the min, max coordinates 
3. try to find the best ROI coordinates to automate the samples dataset
'''


def pos_n_neg_generator():
    orig_list = []
    path = glob.glob('./samp_folder/*.jpg')  # choose right format and location

    for name in path:
        orig_list.append(name)
    a = 1  # added to the image name to uniq it
    for pic in orig_list:
        a = work(pic, a)
    print("Done!")


def work(pic, a):
    picture = cv2.imread(pic)
    gray_pic = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)

    # Select ROI
    (x, y, w, h) = cv2.selectROI(gray_pic)
    # print(x, y, w, h)
    # print(gray_pic.shape)

    # crop and save as a positive image
    pos = gray_pic[y:y + h, x:x + w]
    pos_filename = './ROI_folder/' + str(int(a)) + ".jpg"
    cv2.imwrite(pos_filename, pos)

    start_point = (x, y)  # upper left corner
    end_point = (x+w, y+h)  # lower right corner

    color = (0, 0, 0)  # Black color in BGR
    thickness = -1  # Thickness of -1 will fill the entire shape

    # negative picture is the original background without the ROI
    neg = cv2.rectangle(gray_pic, start_point, end_point, color, thickness)

    neg_filename = './NEG_folder/' + str(int(a+1)) + ".jpg"
    cv2.imwrite(neg_filename, neg)
    a += 2
    return a


if __name__ == "__main__":
    pos_n_neg_generator()

