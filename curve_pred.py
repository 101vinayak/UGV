import cv2
import numpy as np
import os
from matplotlib import pyplot as plt, cm, colors

kernel = np.ones((5,5), np.uint8)

# Defining variables to hold meter-to-pixel conversion
ym_per_pix = 30.0 / 720
# Standard lane width is 3.7 meters divided by lane width in pixels which is
# calculated to be approximately 720 pixels not to be confused with frame height
xm_per_pix = 3.7 / 720

CWD_PATH = os.getcwd()

def readVideo():

    # Read input video from current working directory
    inpImage = cv2.VideoCapture('IGVC Videos/2.MP4')

    return inpImage

def processImage(inpImage):

	frame = cv2.cvtColor(inpImage, cv2.COLOR_BGR2GRAY)
	frame = frame[300:720,:]

	blur = cv2.medianBlur(frame,9)	
	blur = cv2.GaussianBlur(blur,(7,7),0)

	ret, th = cv2.threshold(blur, 200, 255, cv2.THRESH_TOZERO_INV)
	ret, th = cv2.threshold(th, 115, 255, cv2.THRESH_BINARY)
	
	opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
	dilated = cv2.dilate(opening, kernel, iterations=1)	
	
	canny = cv2.Canny(dilated, 40, 60)

	# Display the processed images
	cv2.imshow("Image", inpImage)
	cv2.imshow("frame", frame)

	cv2.imshow("Thresholded", th)
	cv2.imshow("Blurred", blur)
	cv2.imshow("Canny Edges", canny)

	return frame,th,blur,canny

def perspectiveWarp(inpImage):

    # Get image size
    img_size = (inpImage.shape[1], inpImage.shape[0])

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
    birdseye = cv2.warpPerspective(inpImage, matrix, img_size)

    # Get the birdseye window dimensions
    height, width = birdseye.shape[:2]

    # Divide the birdseye view into 2 halves to separate left & right lanes
    birdseyeLeft  = birdseye[0:height, 0:width // 2]
    birdseyeRight = birdseye[0:height, width // 2:width]

    # Display birdseye view image
    # cv2.imshow("Birdseye" , birdseye)
    # cv2.imshow("Birdseye Left" , birdseyeLeft)
    # cv2.imshow("Birdseye Right", birdseyeRight)

    return birdseye, birdseyeLeft, birdseyeRight, minv

image = readVideo()
while True:

	_, frame = image.read()

	birdView, birdViewL, birdViewR, minverse = perspectiveWarp(frame)

	img, thresh, blur, canny = processImage(birdView)
	imgL, threshL, blurL, cannyL = processImage(birdViewL)
	imgR, threshR, blurR, cannyR = processImage(birdViewR)

	# Wait for the ENTER key to be pressed to stop playback
	if cv2.waitKey(5) & 0xFF == ord('q'):
		break

image.release()
cv2.destroyAllWindows()
