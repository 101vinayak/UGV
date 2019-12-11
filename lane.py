import cv2
import time
import numpy

FPS = 60
cap = cv2.VideoCapture('track_opencv.avi')
kernel = numpy.ones((5,5), numpy.uint8)

while cap.isOpened():
	ret, frame = cap.read()
	if not ret:
		break
	
	frame = cv2.GaussianBlur(frame, (5,5), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	th3 = cv2.adaptiveThreshold(hsv,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

	lower_white = numpy.array([052,012,123])
	upper_white = numpy.array([179,255,255])
	upper_w = numpy.array([179,255,255])
	
	print(th3.shape)

	mask = cv2.inRange(lower_white, upper_white)
	
	median = cv2.medianBlur(mask,5)
	
	opening = cv2.morphologyEx(median,cv2.MORPH_OPEN, kernel)
	dilation = cv2.dilate(opening, kernel, iterations=1)
	
	lines = cv2.HoughLinesP(dilation,1,numpy.pi/180,100,minLineLength=30,maxLineGap=150)
	
	if lines is not None:
		for line in lines:
			x1, y1, x2, y2 = line[0]
			cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
	cv2.imshow('frame', frame)
	cv2.imshow('thresh', th3)
	cv2.imshow('result', dilation)
	
	if cv2.waitKey(1) & 0xff == ord('q'):
		break
	time.sleep(1.0/FPS)	
	
cap.release()
cv2.destroyAllWindows()
