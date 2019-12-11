import cv2
import matplotlib.pyplot as plt
import os
import numpy as np

frame = cv2.imread('warp.jpg')

## hue-lightness-saturation is used for low light conditions to extract white lanes
hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
lower_white = np.array([0, 160, 10])
upper_white = np.array([255, 255, 255])

mask = cv2.inRange(frame, lower_white, upper_white)
result = cv2.bitwise_and(frame, frame, mask = mask)
	
##convert image to grayscale, apply threshold, blur and extract edges
gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
blur = cv2.GaussianBlur(thresh, (3,3), 0)
canny_edge = cv2.Canny(blur, 40, 60)

img_size = (frame.shape[1], frame.shape[0])

# Perspective points to be warped
src = np.float32([[590, 440],
                  [690, 440],
                  [200, 640],
                  [1000, 640]])

# Window to be shown
dst = np.float32([[200, 0],
                  [1200, 0],
                  [200, 710],
                  [1200, 710]])

# Matrix to warp the image for birdseye window
matrix = cv2.getPerspectiveTransform(src, dst)
# Inverse matrix to unwarp the image for final window
minv = cv2.getPerspectiveTransform(dst, src)
birdseye = cv2.warpPerspective(frame, matrix, img_size)

# Get the birdseye window dimensions
height, width = birdseye.shape[:2]

# Divide the birdseye view into 2 halves to separate left & right lanes
birdseyeLeft  = birdseye[0:height, 0:width // 2]
birdseyeRight = birdseye[0:height, width // 2:width]

# Display birdseye view image
cv2.imshow('images', frame)
cv2.imshow("Birdseye" , birdseye)
cv2.imshow("Birdseye Left" , birdseyeLeft)
cv2.imshow("Birdseye Right", birdseyeRight)

cv2.imshow('image',thresh)
cv2.waitKey(0) == 1
cv2.destroyAllWindows()
