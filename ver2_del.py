import cv2

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

def diffImage(t0, t1):
  diff = cv2.absdiff(t0, t1)
  return diff


cam = cv2.VideoCapture(0)

winName = "Video"
cv2.namedWindow(winName)

# flipHorizontal = cv2.flip(originalImage, 1)
# flipVertical = cv2.flip(img, 1)

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

while True:
  # cv2.imshow(winName, diffImg(t_minus, t, t_plus))
  cv2.imshow(winName, diffImage(t, t_plus))

  # Read next image
  t_minus = t
  t = t_plus
  t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

  key = cv2.waitKey(20)
  if key == 27:
    cv2.destroyWindow(winName)
    break
