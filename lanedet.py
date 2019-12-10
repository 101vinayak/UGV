import cv2
import numpy as np
import matplotlib

def nothing(x):
	pass

barsWindow = 'Bars'
hl = 'H Low'
hh = 'H High'
sl = 'S Low'
sh = 'S High'
vl = 'V Low'
vh = 'V High'

cap = cv2.VideoCapture('IGVC Videos/3.MP4')
kernel = np.ones((5,5), np.uint8)

cv2.namedWindow(barsWindow, flags = cv2.WINDOW_AUTOSIZE)

cv2.createTrackbar(hl, barsWindow, 0, 179, nothing)
cv2.createTrackbar(hh, barsWindow, 0, 179, nothing)
cv2.createTrackbar(sl, barsWindow, 0, 255, nothing)
cv2.createTrackbar(sh, barsWindow, 0, 255, nothing)
cv2.createTrackbar(vl, barsWindow, 0, 255, nothing)
cv2.createTrackbar(vh, barsWindow, 0, 255, nothing)

cv2.setTrackbarPos(hl, barsWindow, 0)
cv2.setTrackbarPos(hh, barsWindow, 179)
cv2.setTrackbarPos(sl, barsWindow, 0)
cv2.setTrackbarPos(sh, barsWindow, 255)
cv2.setTrackbarPos(vl, barsWindow, 0)
cv2.setTrackbarPos(vh, barsWindow, 255)

while(True):
	ret, frame = cap.read()
	frame = cv2.GaussianBlur(frame, (3,3), 0)

	ret, th = cv2.threshold(frame, 200, 255, cv2.THRESH_TOZERO_INV)
	ret, th3 = cv2.threshold(th, 115, 255, cv2.THRESH_BINARY)

	# convert to HSV from BGR
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# read trackbar positions for all
	hul = cv2.getTrackbarPos(hl, barsWindow)
	huh = cv2.getTrackbarPos(hh, barsWindow)
	sal = cv2.getTrackbarPos(sl, barsWindow)
	sah = cv2.getTrackbarPos(sh, barsWindow)
	val = cv2.getTrackbarPos(vl, barsWindow)
	vah = cv2.getTrackbarPos(vh, barsWindow)

	# make array for final values
	HSVLOW = np.array([hul, sal, val])
	HSVHIGH = np.array([huh, sah, vah])

	kernel = np.ones((7,7),np.uint8)

	# apply the range on a mask
	mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)
	res = cv2.bitwise_and(frame, frame, mask = mask)

	opening = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
	dilated = cv2.dilate(opening, kernel, iterations=1)
	
	lines = cv2.HoughLinesP(dilated.astype(np.uint8), rho=1, theta=np.pi/180, threshold=100, maxLineGap=20, minLineLength=50)
	if lines is not None:
		for line in lines:
			x1, y1, x2, y2 = line[0]
			cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
	cv2.imshow('frame', frame)
	
	# display the camera and masked images
	cv2.imshow('Masked', res)
	cv2.imshow('thresh', th3)
	cv2.imshow('result', dilated)

	# check for q to quit program with 5ms delay
	if cv2.waitKey(5) & 0xFF == ord('q'):
		break

# clean up our resources
cap.release()
cv2.destroyAllWindows()
