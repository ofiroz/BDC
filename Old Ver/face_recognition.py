import cv2
# import background_thread

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
    faces = list(face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4, minSize=(50, 50),flags=cv2.CASCADE_SCALE_IMAGE))
    if len(faces) > 0:
        faces.sort(key=lambda a: a[-1] * a[-2])

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('img', img)

    k = cv2.waitKey(40) & 0xff
    if k == 27:
        break
cap.release()

