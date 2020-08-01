import cv2
from detecto import core
"""
# ==========================================
import time
upper_body = cv2.CascadeClassifier('haarcascade_upperbody.xml')
full_body = cv2.CascadeClassifier('haarcascade_fullbody.xml')

cap = cv2.VideoCapture("sample1.mp4")
if cap is None:
    print("Failed to read the image")
    exit

while True:
    r, frame = cap.read()
    if r:
        start_time = time.time()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # Haar-cascade classifier needs a grayscale image
        rects = full_body.detectMultiScale(gray_frame)

        end_time = time.time()
        print("Elapsed Time:", end_time - start_time)

        for (x, y, w, h) in rects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("preview", frame)
    k = cv2.waitKey(1)
    if k & 0xFF == ord("q"):  # Exit condition
        break

while not True:

    _, img = cap.read()
    if img is None:
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces configured in the XML
    faces = full_body.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('img', img)

    k = cv2.waitKey(40) & 0xff
    if k == 27:
        break
cap.release()

# ==========================================
"""



# this function detect a person (uses ML model)
# finds the person's location and it's center
# returns the center's coordinates
def Center_coordinates(image_path):
    image = image_path
    model = core.Model()

    # print(model.predict_top(image))
    # person_is_found = 0
    try:
        labels, boxes, scores = model.predict_top(image)
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0

        for lbl, box in zip(labels, boxes):  # zip stops when the shorter list is finished
            if lbl is "person":
                # print(type(box)) # finding the person's box
                a, b, c, d = box  # a,b,c,d are "torch.Tensor" objects
                min_x = int(a)
                min_y = int(b)
                max_x = int(c)
                max_y = int(d)
                # print(min_x, min_y, max_x, max_y)
                # print("person HAS BEEN found")
                break
    except:
        # if no person has been found
        print("&&&&&&&&&&&&&& NO person found &&&&&&&&&&&&") # TODO: DELETE
        return (0, 0), 0

    # calculate main vector length, radius = (main vector length) * 0.2
    radius = (((max_x-min_x)**2 + (max_y-min_y)**2)**0.5) * 0.2
    # print(radius)

    center_x = int((max_x + min_x)/2)
    center_y = int((max_y + min_y)/2)
    # print(center_X, center_y)
    center_coordinates = (center_x, center_y)

    # visualize.show_labeled_image(image, boxes, labels)

    # CAN RETURN A CROPPED PERSON
    # img = cv2.imread(image_path)
    # crop_img = img[min_y:max_y, min_x:max_x]
    # cv2.imshow("cropped", crop_img)
    # cv2.waitKey(0)
    # return crop_img, center_coordinates
    return center_coordinates, radius


def circle_center(image_path, center_coordinates, radius):
    # image = cv2.imread(image_path)
    image = image_path
    try:
        orginal_image_with_circle = cv2.circle(image, center_coordinates, radius, (255, 0, 0), 10)
        return orginal_image_with_circle
    except:
        print("**** failed in circle_center - no person was found**************") # TODO: DELETE
        # cv2.waitKey(900000000)

    return cv2.imread('ttt.JPG') # TODO: add FAILED img

