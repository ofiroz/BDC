'''
must detect 1 or 2

if found 2 eyes:
1. calc ave x,y
2. move N pixels from the ave point according the "Eyes : Stomach" ratio

else if 1 eye found (side view):
TODO

'''

import cv2

eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')
cap = cv2.VideoCapture("videoSamples/WhatsApp Video 2020-04-23 at 13.45.40.mp4")
if cap is None:
    print("Failed to read the image")
    exit

while True:
    _, img = cap.read()
    if img is None:
        break
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(20, 20), maxSize=(35, 35))
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

    cv2.imshow("Eye Detected", img)

    k = cv2.waitKey(40) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()

