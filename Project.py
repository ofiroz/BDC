import numpy as np
import cv2
import time

cv2.namedWindow("video")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
# x = frame
while rval:
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # for process
    # frame = cv2.GaussianBlur(frame, (27, 5), 0) # (frame, ( change this , 5), 0)

    # cv2.imshow("video", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
# ------------
    a = frame
    # a = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("video", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    x = a - frame
    x = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)

    #פתרון פלורוסנט
    # המרה מRGB לHSV- לעבוד. YIQ ואז לHSV
    # הבעיה היא בפלורוסנט!! צריך להגדיר ממוצע אפור לתמונה של 128 ואולי גם סטיית תקן
    # התמרת פורייה - נבודד את השקופית עם הרעש
    '''
    kernel = np.ones((5, 5), np.uint8)
    y = cv2.dilate(x, kernel, iterations=3)
    '''
    '''
    filter1 = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])

    filter2 = np.array([[1, 2, 1],
                        [0, 0, 0],
                        [-1, -2, -1]])

    left = cv2.filter2D(x, -1, filter1)
    right = cv2.filter2D(x, -1, -1 * filter1)
    top = cv2.filter2D(x, -1, filter2)
    bottom = cv2.filter2D(x, -1, -1 * filter2)
    filtered_x = left + right + top + bottom
    '''
    # filtered_square = cv2.GaussianBlur(x, (27, 5), 0) # (frame, ( change this , 5), 0)
    cv2.imshow("video", x)
    # ------------
    # frameDiff = cv2.absdiff(x, frame)
    # cv2.imshow("preview", frameDiff)
    # cv2.waitKey(20000)

cv2.destroyWindow("video")

