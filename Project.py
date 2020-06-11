import cv2
import numpy as np
import glob
import person_center
import background_thread
# import importlib
# from PIL import Image
# from resizeimage import resizeimage
from threading import Thread
from matplotlib import pyplot as plt

import warnings
warnings.filterwarnings("ignore")
# import breath_dilation
import queue


# IMPORT A CLASS OF IMPORTS.. LOOKS BETTER


if __name__ == "__main__":
    # 2 threads for to 2 infinity loops
    t = Thread(target=background_thread.call_background_thread)
    m = Thread(target=background_thread.main_func)

    m.start()
    t.start()
    #background_thread.call_background_thread()
    # print("Main Process got to main_func")
    #background_thread.main_func() # if no PERSON detected - return - handle it below

    ''' # FROM PERSON_DETECTION_ML.PY #
    
    image_path = 'WhatsApp Image 2020-04-25 at 09.29.42.jpeg'

    cv2.imshow("cropped", Person_detection_ML.Center_coordinates(image_path))
    cv2.waitKey(0)
    '''

    # when the program ends kill thread
    t.join()
    m.join()


