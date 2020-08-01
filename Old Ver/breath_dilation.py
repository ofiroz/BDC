# ********************************************************************************************
# TODO
# solve the colors issue
# get frame and work with it
# from the cropped squer make a circle
# find a way to dilate the movment (amplify_spatial_lpyr_temporal_iir.m)
# ********************************************************************************************
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import PIL


# TODO: GET THE ORIGINAL IMAGE, MONITORING AREA CENTER, RADIUS AND RETURNS THE FINAL IMAGE
# image_path, center, radius
def monitored_area():
    # A PIL crop box is defined as a 4-tuple of pixel coordinates:
    # (left, upper, right, lower)

    # im is type <class 'PIL.Image.Image'>
    # in order to work with it a convertion to type <class 'numpy.ndarray'> is needed
    im = PIL.Image.open("dddd.png").convert('CMYK')  # for grey .convert("L") # convert('CMYK') is useful#
    # print(type(im))

    region = im.crop((100, 50, 250, 200))

    im.paste(region, (50, 50, 200, 200))

    conv_im = np.array(im)  # type <class 'numpy.ndarray'>
    # print(type(conv_im))

    return conv_im


temp_im = monitored_area()
#plt.imshow(temp_im, cmap='gray')
#plt.show()


# tempering
# ===================


# Taking a matrix of size 5 as the kernel
kernel = np.ones((5, 5), np.uint8)


img_erosion = cv2.erode(temp_im, kernel, iterations=3)
img_dilation = cv2.dilate(temp_im, kernel, iterations=3)

cv2.imshow('Input', temp_im)
cv2.imshow('Erosion', img_erosion)
# cv2.imshow('Dilation', img_dilation)

cv2.waitKey(0)




