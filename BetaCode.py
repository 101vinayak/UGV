import cv2
import numpy as np

def nothing(x):
    pass

def colourfilter(img, lower, upper):
    hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv, lower, upper)

    res=cv2.bitwise_and(img, img, mask=mask)

    return res

def createWindow(name, l, b):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, l, b)

def dilate(img):
    kernel=np.ones((5,5), np.uint8)
    dilated=cv2.dilate(img, kernel, iterations=1)
    return dilated

def opened(img):
    kernel=np.ones((5,5), np.uint8)
    opening=cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return opening

cap=cv2.VideoCapture(1)
kernel = np.ones((5, 5), np.uint8)

cv2.namedWindow("FRAME", cv2.WINDOW_NORMAL)
cv2.namedWindow("COLOR FILTERED", cv2.WINDOW_NORMAL)
cv2.namedWindow("NOISE REMOVED", cv2.WINDOW_NORMAL)
cv2.namedWindow("BLURRED", cv2.WINDOW_NORMAL)

cv2.resizeWindow("FRAME", 500, 500)
cv2.resizeWindow("COLOR FILTERED", 500, 500)
cv2.resizeWindow("NOISE REMOVED", 500, 500)
cv2.resizeWindow("BLURRED", 500, 500)

#min=np.zeros((100,100,3), np.uint8)
#max=np.zeros((100,100,3), np.uint8)
cv2.createTrackbar("B1", "COLOR FILTERED" ,0,255,nothing)
cv2.createTrackbar("G1", "COLOR FILTERED",0,255,nothing)
cv2.createTrackbar("R1", "COLOR FILTERED",0,255,nothing)
cv2.createTrackbar("B2", "COLOR FILTERED",255,255,nothing)
cv2.createTrackbar("G2", "COLOR FILTERED",255,255,nothing)
cv2.createTrackbar("R2", "COLOR FILTERED",255,255,nothing)

while True:
    ret, frame=cap.read()
    cv2.imshow("FRAME", frame)
    #cv2.imshow("MIN", min)
    #cv2.imshow("MAX", max)

    blur1=cv2.GaussianBlur(frame, (5,5), 0)
    blur=cv2.medianBlur(blur1, 5)
    b1 = cv2.getTrackbarPos("B1", "COLOR FILTERED")
    g1 = cv2.getTrackbarPos("G1", "COLOR FILTERED")
    r1 = cv2.getTrackbarPos("R1", "COLOR FILTERED")
    b2 = cv2.getTrackbarPos("B2", "COLOR FILTERED")
    g2 = cv2.getTrackbarPos("G2", "COLOR FILTERED")
    r2 = cv2.getTrackbarPos("R2", "COLOR FILTERED")

    #min[:] = [b1, g1, r1]
    #max[:] = [b2, g2, r2]

    lower = np.array([b1, g1, r1])
    upper = np.array([b2, g2, r2])
    res = colourfilter(blur, lower, upper)
    cv2.imshow("COLOR FILTERED", res)

    gray = cv2.cvtColor(res , cv2.COLOR_BGR2GRAY)
    blur2=cv2.GaussianBlur(gray, (5,5), 0)
    blur3=cv2.medianBlur(blur2, 5)
    cv2.imshow("BLURRED", blur3)

    ret, th1 = cv2.threshold(gray, 190, 255, cv2.THRESH_TOZERO_INV)
    ret, th = cv2.threshold(th1, 130, 255, cv2.THRESH_BINARY)

    opening=opened(th)
    dilating=dilate(opening)
    cv2.imshow("NOISE REMOVED", dilating)

    edges = cv2.Canny(dilating, 225, 250)
    cv2.imshow('edges', edges)

    base = np.zeros((480, 640))
    lines = cv2.HoughLinesP(dilating, 1, np.pi / 50, 50, minLineLength=50, maxLineGap=70)  # What does it return?

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(base, (x1, y1), (x2, y2), (255, 255, 255), 2)

    opening = cv2.morphologyEx(base, cv2.MORPH_OPEN, kernel)
    dilated = cv2.dilate(opening, kernel, iterations=1)

    img = dilated
    cv2.imshow('result', img)
    if cv2.waitKey(5) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
