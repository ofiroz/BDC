import cv2
from detecto import core, utils, visualize
from matplotlib import pyplot as plt
# import Project


# this function detect a person (uses ML model)
# finds the person's location and it's center
# returns the center's coordinates
def Center_coordinates(image_path):
    image = utils.read_image(image_path)
    model = core.Model()

    labels, boxes, scores = model.predict_top(image)

    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0

    for lbl, box in zip(labels, boxes): # zip stops when the shorter list is finished
        if lbl is "person":
            # print(type(box)) # finding the person's box
            a, b, c, d = box # a,b,c,d are "torch.Tensor" objects
            min_x = int(a)
            min_y = int(b)
            max_x = int(c)
            max_y = int(d)
            # print(min_x, min_y, max_x, max_y)
            break

    center_X = int((max_x + min_x)/2)
    center_y = int((max_y + min_y)/2)
    # print(center_X, center_y)
    center_coordinates = (center_X, center_y)

    # visualize.show_labeled_image(image, boxes, labels)

    # CAN RETURN A CROPPED PERSON
    # img = cv2.imread(image_path)
    # crop_img = img[min_y:max_y, min_x:max_x]
    # cv2.imshow("cropped", crop_img)
    # cv2.waitKey(0)
    # return crop_img, center_coordinates
    return center_coordinates


# NO NEED FOR A MAIN
if __name__ == "__main__":

    image_path = 'WhatsApp Image 2020-05-01 at 15.09.02.jpeg'
    img = cv2.imread(image_path)
    # cv2.imshow("cropped", cropped_person(image_path))
    center = Center_coordinates(image_path)

    img = cv2.circle(img, center, 120, (255, 0, 0), 10)

    plt.imshow(img, cmap='gray')
    plt.xticks([]), plt.yticks([])
    plt.show()
    #cv2.imshow("cropped", img)
   # cv2.waitKey(0)


# can import Project.py
# Project.main_func()
