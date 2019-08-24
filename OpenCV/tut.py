import numpy as np
import cv2

img = cv2.imread('f2.png',1)
cv2.imshow('image',img)

k = cv2.waitKey(0) & 0xFF
if k==27:
	cv2.destroyAllWindows()
elif k==ord('s'):
	cv2.imwrite('saved.png',img)
	cv2.destroyAllWindows()
