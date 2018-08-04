import numpy as np
import cv2
from math import pi

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture('trim1.MP4')


indicator = 0
## Processing Webcam or Video
text = input("Do you want use webcam(Yes/No) : ")
if( text == "Yes" or text == "yes" or text =='y'):
	print("Processing Webcam....\n")
else:
	print("Processing Video....\n")
	indicator = 1

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)


while(True):
    # Capture frame-by-frame
    if indicator == 1:
    	ret, frame = cap2.read()
    else:
    	ret,frame = cap1.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #orignal = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    orignal = frame.copy()
    gray = cv2.GaussianBlur(gray,(5,5),0)
    gray = cv2.medianBlur(gray,5)

    gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
			cv2.THRESH_BINARY,11,3.5)

    kernel = np.ones((3,3),np.uint8)
    gray = cv2.erode(gray,kernel,iterations = 1)
    gray = cv2.dilate(gray,kernel,iterations = 1)

    _, contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours_list = []
    for contour in contours:
    	approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
    	area = cv2.contourArea(contour)
    	(x,y),radius = cv2.minEnclosingCircle(contour)
    	cal_area = radius*radius*pi
    	area2 = 1.6*area
    	if((len(approx) > 8) & (len(approx) < 23) & (area > 30)& (cal_area < area2)):
    		contours_list.append(contour)
    		print('Actual Area:'+str(area))
    		print('Circle Area for same Parameter:'+str(cal_area))
    		print('_______________')
    	cv2.drawContours(orignal, contours_list,  -1, (255,0,0), 1)

    # Display the resulting frame
    cv2.imshow('frame',orignal)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap1.release()
cap2.release()
cv2.destroyAllWindows()