import cv2

face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
eye_cascade = 'haarcascade/haarcascade_eye.xml'

cap = cv2.VideoCapture(0)
if cap is None:
    print("Failed to read the image")
    exit

while True:

    _, img = cap.read()
    if img is None:
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces configured in the XML
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('img', img)

    k = cv2.waitKey(40) & 0xff
    if k == 27:
        break
cap.release()

