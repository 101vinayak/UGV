import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

## current working directory path
CWD_path = os.cwd()


## Reading the video frame by frame
def readVideo():

	# Read input video from current working directory
    	frame = cv2.VideoCapture('track_opencv.avi')

    	return frame

##Func to process the image for lane detetction
def Imgprocessing(frame):
	
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
	
	##display the processed images
	cv2.imshow("Image", frame)
	cv2.imshow("HLS Filtered", result)
	cv2.imshow("Grayscale", gray)
	cv2.imshow("Thresholded", thresh)
	cv2.imshow("Blurred", blur)
	cv2.imshow("Canny Edges", canny_edge)

	return frame, result, gray, thresh, blur, canny_edge

##Func to apply perspective warp
def warp(img):
	
	## image size
	img_size = (img.shape[1], img.shape[0])
	
	
