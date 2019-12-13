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
	frame = frame[300:650,:]

	blur1 = cv2.medianBlur(frame,9)	
	blur = cv2.GaussianBlur(blur1,(7,7),0)

	ret, th = cv2.threshold(blur, 180, 255, cv2.THRESH_TOZERO_INV)
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
	cv2.imshow('dilated', dilated)
	#cv2.imshow('otsu', th3)

	#out.write(dilated)

	if cv2.waitKey(5) & 0xFF == ord('q'):
		break

cap.release()
#out.release()
cv2.destroyAllWindows()

'''


img = cv2.imread('IGVC Videos/2.png')
while(True):
	frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	frame = frame[300:720,:]	

	blur1 = cv2.medianBlur(frame,9)	
	blur = cv2.GaussianBlur(blur1,(7,7),0)

	ret, th = cv2.threshold(blur, 200, 255, cv2.THRESH_TOZERO_INV)
	ret, th = cv2.threshold(th, 120, 255, cv2.THRESH_BINARY)
	
	ret,th1 = cv2.threshold(blur,127,255,cv2.THRESH_BINARY)
	#th2 = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
	th2 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,9,0)
	th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	
	opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
	dilated = cv2.dilate(opening, kernel, iterations=1)	

	cv2.imshow('frame', frame)
	#cv2.imshow('blur', blur)

	#print(frame.shape)

	#cv2.imshow('thresh', th)
	cv2.imshow('dilated', dilated)
	#cv2.imshow('otsu', th3)

	if cv2.waitKey(5) & 0xFF == ord('q'):
		break

'''
