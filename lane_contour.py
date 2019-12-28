#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

import cv2
import matplotlib.pyplot as plt
import numpy as np
import time

dirc = []

kernel = np.ones((5,5), np.uint8)
cap = cv2.VideoCapture(1)

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (568,1024))

def colourfilter(img, lower, upper):
	hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask=cv2.inRange(hsv, lower, upper)

	res=cv2.bitwise_and(img, img, mask=mask)

	return res

while(True):

	ret, frame_org = cap.read()
	
	#frame = cv2.cvtColor(frame_org, cv2.COLOR_BGR2GRAY)
	frame = frame_org[:,:]
	
	lower = np.array([0, 0, 0])
	upper = np.array([255,18,255])
	
	frame = colourfilter(frame, lower, upper)
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	blur1 = cv2.medianBlur(frame,5)
	blur = cv2.GaussianBlur(blur1,(5,5),0)

	ret, th = cv2.threshold(blur, 190, 255, cv2.THRESH_TOZERO_INV)
	ret, th = cv2.threshold(th, 130, 200, cv2.THRESH_BINARY)

	'''
	ret,th1 = cv2.threshold(blur,127,255,cv2.THRESH_BINARY)
	#th2 = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
	th2 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,9,0)
	th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	'''

	opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
	dilated = cv2.dilate(opening, kernel, iterations=1)	

	cv2.imshow('frame', frame_org)
	cv2.imshow('blur', blur)

	#print(frame.shape)

	cv2.imshow('thresh', th)
	#cv2.imshow('otsu', th3)

	edges = cv2.Canny(dilated,225,250)
	cv2.imshow('edges', edges)

	base = np.zeros((480,640))
	lines = cv2.HoughLinesP(dilated,1,np.pi/180,50,minLineLength=50,maxLineGap=70)
	
	if lines is not None:
		for line in lines:
			x1, y1, x2, y2 = line[0]
			cv2.line(base, (x1, y1), (x2, y2), (255, 255, 255), 2)
	'''
	cv2.imshow('dilated', base)
	_,contours,hier = cv2.findContours(base,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

	for cnt in contours:
	    if cv2.contourArea(cnt)>500:  # remove small areas like noise etc
		hull = cv2.convexHull(cnt)    # find the convex hull of contour
		hull = cv2.approxPolyDP(hull,0.1*cv2.arcLength(hull,True),True)
		if len(hull)==4:
		    cv2.drawContours(base,[hull],0,(0,255,0),2)
	'''
	
	opening = cv2.morphologyEx(base, cv2.MORPH_OPEN, kernel)
	dilated = cv2.dilate(opening, kernel, iterations=1)
	
	img = dilated
	mid = []
	
	for ix in range(150):
	
		pts = []		
		for jx in range(640):
			if img[240+ix][jx] == 255:
				pts.append(jx)	
		try: 
			a = min(pts)
			b = max(pts)
			
			if b-a < 50:
				if a and b < 150:
					mid.append((640-b)/2)
				else:
					mid.append(b/2)
			else:
				mid.append((b-a)/2 + a)
		except:
			mid.append(320)
	
	mid = sum(mid)/len(mid)
	dirc.append(mid)
	cv2.circle(img,(mid,400), 10, (255,255,255), 1)
	
	ln = len(dirc)
	'''
	while ln>1:
		if abs(dirc[ln-1] - dirc[ln-2]) > 400:
			dirc[ln-1] = dirc[ln-2]
	'''
	if abs(dirc[ln-1] - dirc[ln-2])>30:
		
		if dirc[ln-1]<dirc[ln-2]:
			strng = 'LEFT'
		else:
			strng = 'RIGHT'
	else:
		strng = 'STRAIGHT'
		
	'''
	im = np.zeros((50,1280))
	for ix in range(50):
		for jx in range(1280):
			im[ix][jx] = dilated[290+ix][jx]
	'''
	
	cv2.imshow('result', img)
	#out.write(dilated)
	
	#time.sleep(10)
	
	def lane_contour():
		pub = rospy.Publisher('Direction', String, queue_size=10)
		rospy.init_node('lane_contour', anonymous=True)
		#rate = rospy.Rate(10) # 10hz
		hello_str = strng
		rospy.loginfo(hello_str)
		pub.publish(hello_str)
		#rate.sleep()
		
	try:
        	lane_contour()
    	except rospy.ROSInterruptException:
        	pass
        

	if cv2.waitKey(5) & 0xFF == ord('q'):
		break

cap.release()
#out.release()
cv2.destroyAllWindows()
