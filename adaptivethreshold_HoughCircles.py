import cv2
import numpy as np


raw_image = cv2.imread('123.jpg')
cv2.imshow('Original Image', raw_image)
cv2.waitKey(0)

frame = raw_image

gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray,(5,5),0)
gray = cv2.medianBlur(gray,5)

cv2.imshow('Blur', gray)
cv2.waitKey(0)

gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
		cv2.THRESH_BINARY,11,3.5)

cv2.imshow('AdaptiveThreshold', gray)
cv2.waitKey(0)

kernel = np.ones((3,3),np.uint8)
gray = cv2.erode(gray,kernel,iterations = 1)
gray = cv2.dilate(gray,kernel,iterations = 1)

cv2.imshow('Eroded and dilated', gray)
cv2.waitKey(0)

img_size = gray.shape
print (img_size)

circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 200, param1=30, param2=20, minRadius=0, maxRadius=0)
print (circles)

_, contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contour_list = []
for contour in contours:
    approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
    area = cv2.contourArea(contour)
    if ((len(approx) > 8) & (len(approx) < 23) & (area > 30) ):
        contour_list.append(contour)
        print(contour)

cv2.drawContours(raw_image, contour_list,  -1, (255,0,0), 1)
cv2.imshow('Objects_Detected',raw_image)
cv2.waitKey(0)