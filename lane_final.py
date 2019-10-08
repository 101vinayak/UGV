import cv2
import matplotlib.pyplot as plt
import numpy as np

cap = cv2.VideoCapture(0)

while(True):

	ret, frame = cap.read()
	'''
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	ret, frame = cv2.threshold(frame, 210, 255, cv2.THRESH_TOZERO_INV)
	ret, frame = cv2.threshold(frame, 180, 210, cv2.THRESH_BINARY)
	'''

	blur1 = cv2.medianBlur(frame,9)	
	blur2 = cv2.GaussianBlur(blur1,(7,7),0)
	
	ret,th1 = cv2.threshold(frame,127,255,cv2.THRESH_BINARY)
	th2 = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
	th3 = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	
	cv2.imshow('frame', frame)
	cv2.imshow('blur', blur2)
	cv2.imshow('mean', th1)
	cv2.imshow('gauss', th2)

	if cv2.waitKey(5) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()


