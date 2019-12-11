import cv2
import numpy as np

kernel = np.ones((7,7), np.uint8)
cap = cv2.VideoCapture('IGVC Videos/3.MP4',0)

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (568,1024))

while(True):

	ret, frame_org = cap.read()	
	frame = cv2.cvtColor(frame_org, cv2.COLOR_BGR2GRAY)
	frame = frame[250:650,:]
	
	blur1 = cv2.medianBlur(frame,7)	
	blur = cv2.GaussianBlur(blur1,(5,5),0)

	ret, th = cv2.threshold(blur, 200, 255, cv2.THRESH_TOZERO_INV)
	ret, th = cv2.threshold(th, 110, 255, cv2.THRESH_BINARY)
	
	opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
	dilated = cv2.dilate(opening, kernel, iterations=1)
	
	cv2.imshow('th',dilated)
	
	_,contours,hier = cv2.findContours(dilated,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours:
	    if cv2.contourArea(cnt)>50:  # remove small areas like noise etc
		hull = cv2.convexHull(cnt)    # find the convex hull of contour
		hull = cv2.approxPolyDP(hull,0.1*cv2.arcLength(hull,True),True)
		if True:
		    cv2.drawContours(frame,[hull],0,(0,255,0),2)
	
	cv2.imshow('img',frame)
	
	if cv2.waitKey(5) & 0xFF == ord('q'):
		break

cap.release()
#out.release()
cv2.destroyAllWindows()
