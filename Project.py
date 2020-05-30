import cv2
import numpy as np
import glob
import person_center
import background_thread
# import importlib
# from PIL import Image
# from resizeimage import resizeimage
from threading import Thread
# import breath_dilation
import queue


# IMPORT A CLASS OF IMPORTS.. LOOKS BETTER


if __name__ == "__main__":

    # print(background_thread.flag_to_ten)
    #print(background_thread.frame_sample.__len__())


    t = Thread(target=background_thread.call_background_thread)
    keep_going = True
    t.start()

    background_thread.main_func()


    ''' # FROM PERSON_DETECTION_ML.PY #
    
    image_path = 'WhatsApp Image 2020-04-25 at 09.29.42.jpeg'

    cv2.imshow("cropped", Person_detection_ML.Center_coordinates(image_path))
    cv2.waitKey(0)
    '''

    # when the program ends kill thread
    keep_going = False
    t.join()


