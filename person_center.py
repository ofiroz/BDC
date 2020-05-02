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
    return center_coordinates


def circle_center(image_path, center_coordinates):
    imgage = cv2.imread(image_path)
    orginal_image_with_circle = cv2.circle(imgage, center_coordinates, 150, (255, 0, 0), 10)
    orginal_image_with_circle

    return orginal_image_with_circle


# NO NEED FOR A MAIN
if __name__ == "__main__":

    image_path = 'WhatsApp Image 2020-04-25 at 09.29.42.jpeg'
    img = circle_center(image_path, Center_coordinates(image_path))
    plt.imshow(img, cmap='gray')
    plt.xticks([]), plt.yticks([])
    plt.show()


# can import Project.py
# Project.main_func()

