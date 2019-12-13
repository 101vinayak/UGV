import cv2
import matplotlib.pyplot as plt
import numpy as np

kernel = np.ones((5,5), np.uint8)
cap = cv2.VideoCapture('IGVC Videos/3.MP4')

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (568,1024))

while(True):

	ret, frame_org = cap.read()	
	frame = cv2.cvtColor(frame_org, cv2.COLOR_BGR2GRAY)
	frame = frame[250:650,:]

	blur1 = cv2.medianBlur(frame,5)	
	blur = cv2.GaussianBlur(blur1,(5,5),0)

	ret, th = cv2.threshold(blur, 200, 255, cv2.THRESH_TOZERO_INV)
	ret, th = cv2.threshold(th, 110, 255, cv2.THRESH_BINARY)

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

	base = np.zeros((470,1280))
	lines = cv2.HoughLinesP(dilated,1,np.pi/180,100,minLineLength=30,maxLineGap=70)
	
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
	
	points = []
	for ix in range(0,1280):
		
		if img[300][ix] == 255:
			points.append(ix)
		
		try:
			a = min(points)
			b = max(points)
			mid = (b-a)/2
		except:
			mid = 0
		
		cv2.circle(img,(mid,300), 10, (255,255,255), 1)

	cv2.imshow('result', img)
	#out.write(dilated)

	if cv2.waitKey(5) & 0xFF == ord('q'):
		break

cap.release()
#out.release()
cv2.destroyAllWindows()
