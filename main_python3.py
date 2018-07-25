import cv2
import numpy as np
import buoy


## Input File
cap_img = cv2.imread('photos/DSCF3426.JPG')
cap_vid = cv2.VideoCapture('photos/20180707_153536.mp4') # for video
indicator = 0

## Processing Image or Video
text = input("Do you want to process an Image(Yes/No) : ")
if( text == "Yes" or text == "yes"):
	print("Processing Image....\n")
	frame = cap_img
else:
	print("Processing Video....\n")
	indicator = 1
	frame = cap_vid


def nothing(x):
	pass

b = buoy.Buoy()

cv2.namedWindow('Colorbars')
cv2.createTrackbar("Max", "Colorbars",0,255, nothing)
cv2.createTrackbar("Min", "Colorbars",0,255, nothing)

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
cv2.namedWindow('res', cv2.WINDOW_NORMAL)

while(1):

	huh=cv2.getTrackbarPos("Max", "Colorbars")
	hul=cv2.getTrackbarPos("Min", "Colorbars")
	if(indicator == 1):
		_, frame = cap_vid.read() # for video
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	#Hue is the last value
	lower_bounds = np.array([0,0,0])
	upper_bounds = np.array([60,255,255])
	kernel = np.ones((10,10), np.uint8)
	
	mask = cv2.inRange(hsv, lower_bounds, upper_bounds)
	mask = cv2.erode(mask, kernel, iterations=1)
	mask = cv2.dilate(mask, kernel, iterations=1)
	res = cv2.bitwise_and(frame,frame, mask= mask)

	
	_, contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	contours.sort(key=cv2.contourArea, reverse=True)

	b.find(contours)

	#print "Distance: " + str(b.measure())

	c = b.get_contour()
	x,y,w,h = b.get_find_dimensions()

	circle, radius = cv2.minEnclosingCircle(c)
	circ = [0, 0]

	circ[0] = int(circle[0])
	circ[1] = int(circle[1])
	radius = int(radius)
	circ = tuple(circ)

	cv2.circle(res,circ, radius, (255,255,255), -1)
 
	cv2.drawContours(res, [c], -1, (0,255,0), 15)

	font				   = cv2.FONT_HERSHEY_SIMPLEX
	bottomLeftCornerOfText = (x,y-20)
	fontScale			  = 10
	fontColor			  = (255,255,255)
	lineType			   = 4
	

	cv2.putText(frame,'Buoy', 
		bottomLeftCornerOfText, 
		font, 
		fontScale,
		fontColor,
		lineType)


	cv2.Canny(mask, 100, 200)
	
	#circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,20,
     #                               param1=5,param2=5,minRadius=0,maxRadius=0)


	try:	
		print((len(circles)))
	except:
		pass
	

	cv2.rectangle(frame, (x, y), (x+w, y+h), (203,192,255), 6)
	
	cv2.imshow('frame',frame)
	cv2.imshow('mask',mask)
	cv2.imshow('res',res)
	
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()
cap_vid.release()
cap_img.release()
