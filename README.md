# BDC
Breathing_Detection_Camera

Three key features:
1. baby (only) detection
2. baby respiratory monitoring
3. baby pulse monitoring

All three works in real time!



person_detection uses Machine Learning - getting 2 warnings - cant get rid of them - solution: downgrade to pytorch 1.14.0 (not working)

Continue...

https://recordit.co/5dPlSKdROx

http://g.recordit.co/5dPlSKdROx.gif

Resourses used
================

https://pdfs.semanticscholar.org/b611/2977b9a18fd80f1a8eb855f3ab04be8572c1.pdf - SIFT & haar features 

https://www.mathworks.com/help/vision/ug/train-a-cascade-object-detector.html - cascade training 

https://github.com/thearn/webcam-pulse-detector - pulse detection

https://academic.oup.com/cardiovascres/article/70/1/12/408540 - Mayer waves and nerves frequencies 

https://arxiv.org/pdf/1909.03503.pdf - monitoring breathing rate from face alone -> future todo

https://docs.opencv.org/2.4/modules/objdetect/doc/cascade_classification.html - Haar Feature based Cascade Classifier

https://sites.google.com/site/5kk73gpu2012/assignment/viola-jones-face-detection#TOC-Image-Pyramid - Haar Feature and Image Pyramid

https://www.hindawi.com/journals/mse/2015/948960/ - Haar and LBP study

http://people.csail.mit.edu/mrub/evm/#code - Eulerian Magnification

https://www.microsoft.com/en-us/research/wp-content/uploads/2013/01/bill-freeman_visualmotion.pdf - Eulerian Magnification Microsoft study

https://github.com/brycedrennan/eulerian-magnification - implementation

https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_pyramids/py_pyramids.html - Image Pyramids

https://docs.opencv.org/2.4/modules/video/doc/motion_analysis_and_object_tracking.html - calculating an optical flow (Lucas-Kanade) for breath monitoring

https://nanonets.com/blog/optical-flow/ - optical-flow

https://www.geeksforgeeks.org/opencv-the-gunnar-farneback-optical-flow/ - preview to the Gunnar Farneback algorithm (optical flow)

https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf - Gunnar Farneback algorithm (optical flow)

