import cv2
import matplotlib.pyplot as plt
import numpy as np

kernel = np.ones((5,5), np.uint8)

cap = cv2.VideoCapture(1)

#img = cv2.imread('IGVC Videos/2.png')
#cv2.imshow('img', img)
while(True):	
	ret, img = cap.read()	
	cv2.imshow('img', img)	
	'''
	for ix in range(img.shape[0]):
		for jx in range(img.shape[1]):
			
			color = img[ix,jx]
			#print(color[1])
			img[ix,jx] = color
	'''
	frame = img[300:720,:]	
	frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)	
	
	blur1 = cv2.medianBlur(frame,9)	
	blur = cv2.GaussianBlur(blur1,(7,7),0)

	ret, th = cv2.threshold(blur, 50, 255, cv2.THRESH_TOZERO_INV)
	ret, th = cv2.threshold(th,40, 255, cv2.THRESH_BINARY)
	
	ret,th1 = cv2.threshold(blur,127,255,cv2.THRESH_BINARY)
	#th2 = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
	th2 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,9,0)
	th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	
	opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
	dilated = cv2.dilate(opening, kernel, iterations=1)	

	cv2.circle(dilated,(300,200), 10, (255,255,255), -1)

	cv2.imshow('frame', img)
	#cv2.imshow('blur', blur)

	#print(frame.shape)

	#cv2.imshow('thresh', th)
	cv2.imshow('dilated', dilated)
	#cv2.imshow('otsu', th3)

	if cv2.waitKey(5) & 0xFF == ord('q'):
		break

cap.release()
#out.release()
cv2.destroyAllWindows()
