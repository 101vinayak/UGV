import cv2
import numpy as np

def nothing(x):
    pass

def colourfilter(img, lower, upper):
    hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv, lower, upper)
    res=cv2.bitwise_and(img, img, mask=mask)
    return res

cap=cv2.VideoCapture('IGVC Videos/3.MP4')

cv2.namedWindow('FRAME', cv2.WINDOW_NORMAL)
cv2.resizeWindow('FRAME', 500, 500)
cv2.namedWindow('COLOR FILTERED', cv2.WINDOW_NORMAL)
cv2.resizeWindow('COLOR FILTERED', 500, 500)
cv2.createTrackbar('Bmin', 'COLOR FILTERED', 0, 255, nothing)
cv2.createTrackbar('Gmin', 'COLOR FILTERED', 0, 255, nothing)
cv2.createTrackbar('Rmin', 'COLOR FILTERED', 0, 255, nothing)
cv2.createTrackbar('Bmax', 'COLOR FILTERED', 255, 255, nothing)
cv2.createTrackbar('Gmax', 'COLOR FILTERED', 255, 255, nothing)
cv2.createTrackbar('Rmax', 'COLOR FILTERED', 255, 255, nothing)

while True:
    ret, frame=cap.read()
    frame=frame[300:670, :]
    blur1=cv2.GaussianBlur(frame, (5,5), 0)
    blur=cv2.medianBlur(blur1 ,5)
    b1=cv2.getTrackbarPos('Bmin', 'COLOR FILTERED')
    g1 = cv2.getTrackbarPos('Gmin', 'COLOR FILTERED')
    r1 = cv2.getTrackbarPos('Rmin', 'COLOR FILTERED')
    b2 = cv2.getTrackbarPos('Bmax', 'COLOR FILTERED')
    g2 = cv2.getTrackbarPos('Gmax', 'COLOR FILTERED')
    r2 = cv2.getTrackbarPos('Rmax', 'COLOR FILTERED')
    low=np.array([b1, g1, r1])
    up=np.array([b2, g2, r2])
    filter=colourfilter(blur, low, up)

    cv2.imshow('FRAME', frame)
    cv2.imshow('COLOR FILTERED', filter)

    if cv2.waitKey(1) & 0xFF== ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
