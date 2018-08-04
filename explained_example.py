import cv2
import numpy as np
from math import pi


raw_image = cv2.imread('123.JPG')

frame = raw_image

gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
cv2.imshow('gray',gray)
cv2.waitKey(0)

gray = cv2.GaussianBlur(gray,(5,5),0);
gray = cv2.medianBlur(gray,5)

cv2.imshow('Blur',gray)
cv2.waitKey(0)


gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
		cv2.THRESH_BINARY,11,3.5)

cv2.imshow('Adaptive Threshold',gray)
cv2.waitKey(0)

kernel = np.ones((3,3),np.uint8)
gray = cv2.erode(gray,kernel,iterations = 1)
cv2.imshow('Erode',gray)
cv2.waitKey(0)

gray = cv2.dilate(gray,kernel,iterations = 1)
cv2.imshow('Dilate',gray)
cv2.waitKey(0)

_, contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contour_list = []
center_list = []
for contour in contours:
    approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
    area = cv2.contourArea(contour)
    (x,y),radius = cv2.minEnclosingCircle(contour)
    center = (int(x),int(y))
    cal_area = radius*radius*pi
    area2 = 2*area
    perimeter = 2*pi*radius
    center_list.append(center)
    if ((len(approx) > 8) & (len(approx) < 23) & (area > 50) & (cal_area < area2)):
        contour_list.append(contour)

cv2.drawContours(raw_image, contour_list,  -1, (255,0,0), 1)
cv2.imshow('Objects_Detected',raw_image)


cv2.waitKey(0)