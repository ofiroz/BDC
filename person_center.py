import cv2
from detecto import core, utils, visualize
from matplotlib import pyplot as plt
# import Project


# this function detect a person (uses ML model)
# finds the person's location and it's center
# returns the center's coordinates
def Center_coordinates(image_path):

    # TODO: DELETE
    #plt.imshow(image_path, cmap='gray')
    #plt.xticks([]), plt.yticks([])
    #plt.show()

    # image = utils.read_image(image_path) # image_path
    image = image_path
    model = core.Model()

    # print(model.predict_top(image))
    # person_is_found = 0

    try:
        labels, boxes, scores = model.predict_top(image)
        # print("Test 1")
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0

        for lbl, box in zip(labels, boxes):  # zip stops when the shorter list is finished
            # print("Test 2")
            if lbl is "person":
                # print(type(box)) # finding the person's box
                a, b, c, d = box  # a,b,c,d are "torch.Tensor" objects
                min_x = int(a)
                min_y = int(b)
                max_x = int(c)
                max_y = int(d)
                # print(min_x, min_y, max_x, max_y)
                person_is_found = 1
                print("person HAS BEEN found")
                break
    except:
        # if no person has been found
        print("no person found")
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
        print("**** failed in circle_center - no person was found")
    return cv2.imread('dddd.PNG') # TODO: add FAILED img


'''
# NO NEED FOR A MAIN
if __name__ == "__main__":

    image_path = 'pasted2.png'
    center, circle_radius = Center_coordinates(image_path)
    circle_radius = int(circle_radius)
    img = circle_center(image_path, center, circle_radius)

    plt.imshow(img, cmap='gray')
    plt.xticks([]), plt.yticks([])
    plt.show()
'''

# can import Project.py
# Project.main_func()

