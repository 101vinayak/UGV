#!/usr/bin/env python2.7
"""
import cv2
import numpy as np

img = cv2.imread('/home/vinayak/input_image.png',1)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_white = np.array([0,0,0], dtype=np.uint8)
upper_white = np.array([0,0,255], dtype=np.uint8)

mask = cv2.inRange(hsv, lower_white, upper_white)

res = cv2.bitwise_and(img,img, mask= mask)


kernel = np.ones((7,7),np.uint8)

erosion = cv2.erode(res,kernel,iterations = 1)
dilation = cv2.dilate(res,kernel,iterations = 1)
opening = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(res, cv2.MORPH_CLOSE, kernel)
dst = cv2.filter2D(img,-1,kernel)

cv2.imshow('image1',img)

cv2.imshow('image2',erosion)
cv2.imshow('image3',dilation)

cv2.imshow('image4',opening)
cv2.imshow('image5',closing)
cv2.imshow('image6',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
"""
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_white = np.array([0,0,0])
    upper_white = np.array([0,0,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    
    kernel = np.ones((6,6),np.uint8)
    erosion = cv2.erode(res,kernel,iterations = 1)
    dilation = cv2.dilate(res,kernel,iterations = 1)
    opening = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(res, cv2.MORPH_CLOSE, kernel)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('erosion',erosion)
    cv2.imshow('dilation',dilation)
    cv2.imshow('opening',opening)
    cv2.imshow('closing',closing)
    k = cv2.waitKey(5) & 0xFF
    if k == 0:
        break

cv2.destroyAllWindows()


"""

import cv2 as cv
import numpy as np

# optional argument for trackbars
def nothing(x):
    pass

# named ites for easy reference
barsWindow = 'Bars'
hl = 'H Low'
hh = 'H High'
sl = 'S Low'
sh = 'S High'
vl = 'V Low'
vh = 'V High'

# set up for video capture on camera 0
cap = cv.VideoCapture('input_image.png')

# create window for the slidebars
cv.namedWindow(barsWindow, flags = cv.WINDOW_AUTOSIZE)

# create the sliders
cv.createTrackbar(hl, barsWindow, 0, 179, nothing)
cv.createTrackbar(hh, barsWindow, 0, 179, nothing)
cv.createTrackbar(sl, barsWindow, 0, 255, nothing)
cv.createTrackbar(sh, barsWindow, 0, 255, nothing)
cv.createTrackbar(vl, barsWindow, 0, 255, nothing)
cv.createTrackbar(vh, barsWindow, 0, 255, nothing)

# set initial values for sliders
cv.setTrackbarPos(hl, barsWindow, 0)
cv.setTrackbarPos(hh, barsWindow, 179)
cv.setTrackbarPos(sl, barsWindow, 0)
cv.setTrackbarPos(sh, barsWindow, 255)
cv.setTrackbarPos(vl, barsWindow, 0)
cv.setTrackbarPos(vh, barsWindow, 255)

while(True):
    ret, frame = cap.read()
   # frame = cv.GaussianBlur(frame, (3,3), 0)
    
    # convert to HSV from BGR
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # read trackbar positions for all
    hul = cv.getTrackbarPos(hl, barsWindow)
    huh = cv.getTrackbarPos(hh, barsWindow)
    sal = cv.getTrackbarPos(sl, barsWindow)
    sah = cv.getTrackbarPos(sh, barsWindow)
    val = cv.getTrackbarPos(vl, barsWindow)
    vah = cv.getTrackbarPos(vh, barsWindow)

    # make array for final values
    HSVLOW = np.array([hul, sal, val])
    HSVHIGH = np.array([huh, sah, vah])

    kernel = np.ones((7,7),np.uint8)

    # apply the range on a mask
    mask = cv.inRange(hsv, HSVLOW, HSVHIGH)
    res = cv.bitwise_and(frame, frame, mask = mask)
    erosion = cv.erode(res,kernel,iterations = 1)
    dilation = cv.dilate(res,kernel,iterations = 1)
    opening = cv.morphologyEx(res, cv.MORPH_OPEN, kernel)
    closing = cv.morphologyEx(res, cv.MORPH_CLOSE, kernel)

    # display the camera and masked images
    cv.imshow('Masked', res)
    cv.imshow('Camera', frame)
    cv.imshow('eroded', erosion)
    cv.imshow('dilated', dilation)
    cv.imshow('opening', opening)
    cv.imshow('closing', closing)

	# check for q to quit program with 5ms delay
    if cv.waitKey(5) & 0xFF == ord('q'):
        break

# clean up our resources
cap.release()
cv.destroyAllWindows()

