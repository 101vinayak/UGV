import numpy as np
import cv2

img = np.zeros((600,1000,3))

while(True):

	cv2.imshow('img',img)
	#cv2.line(img,(0,0),(1600,1000),(255,255,255),5)	## thickness is 5 rest are strting n ending pnts and color
	
	cv2.circle(img,(500,100), 90, (0,0,255), -1)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
