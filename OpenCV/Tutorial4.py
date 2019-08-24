import numpy as np
import cv2

cap = cv2.VideoCapture(0)
ret = cap.set(cv2.CAP_PROP_FRAME_WIDTH,1000)
ret = cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1000)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output2.avi',fourcc,20,(1000,1000))

while(True):
	
	ret, frame = cap.read()
	frame = cv2.flip(frame, flipCode=1)            ## flipped sideways
	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	cv2.imshow('frame', frame)
	
	out.write(frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
out.release()

cap = cv2.VideoCapture('output2.avi')
while(cap.isOpened()):
	
	ret, frame = cap.read()
	cv2.show('frame', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
