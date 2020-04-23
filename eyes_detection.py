import cv2

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture(0)
if cap is None:
    print("Failed to read the image")
    exit

while True:
    _, img = cap.read()
    if img is None:
        break
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

    cv2.imshow("Eye Detected", img)

    k = cv2.waitKey(40) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
