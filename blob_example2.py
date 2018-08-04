import cv2, matplotlib
import numpy as np
import matplotlib.pyplot as plt

coins = cv2.imread('123.jpg')
coins_gray = cv2.cvtColor(coins, cv2.COLOR_BGR2GRAY)
coins_preprocessed = cv2.GaussianBlur(coins_gray, (5, 5), 0)

# get binary image
_, coins_binary = cv2.threshold(coins_preprocessed, 150, 255, cv2.THRESH_BINARY_INV)

# invert image to get coins
coins_binary = cv2.bitwise_not(coins_binary)
cv2.imshow("Coins", coins_binary)
 
# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create()
 
# Detect blobs.
keypoints = detector.detect(coins_binary)
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(coins_binary, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)

_, contours, hierarchy = cv2.findContours(coins_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contour_list = []
center_list = []
area_list = []
for contour in contours:
    approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
    area = cv2.contourArea(contour)
    if (area > 50):
        contour_list.append(contour)
        (x,y),radius = cv2.minEnclosingCircle(contour)
        center = (int(x),int(y))
        center_list.append(center)
        area_list.append(area)
        #print("_________-------------_________")
        #print('Contour:'+str(contour))
        #print("Area:"+str(area))
        #print("Center"+str(center))
        #print("")

median_area = np.median(area_list)
print('Median Area:'+str(median_area))

square_areas = []
for x in area_list:
	if (x > 2*median_area):
		square_areas.append(x)
		area_list.remove(x)

print('Square areas')
print(square_areas)

square_centers = []
for elements in contour_list:
	area = cv2.contourArea(elements)
	if area in square_areas:
		(x,y),_ = cv2.minEnclosingCircle(elements)
		center = (int(x),int(y))
		square_centers.append(center)
		center_list.remove(center)


print('Square Centers:')
print(square_centers)

distance_list = []
min_list = []


for center_1 in center_list:
	x1,y1 = center_1
	for center_2 in square_centers:
		x2,y2 = center_2
		distance = ((x2-x1)**2)+((y2-y1)**2)
		distance_list.append(distance)

for x in range(13):
	x = min(distance_list)
	min_list.append(x)
	distance_list.remove(x)

for center_1 in center_list:
	x1,y1 = center_1
	for center_2 in square_centers:
		x2,y2 = center_2
		distance = ((x2-x1)**2)+((y2-y1)**2)
		if distance in min_list:
			cv2.line(coins,center_1,center_2,(0,0,0),2)
			print('x1:'+str(x1)+' y1:'+str(y1))
			print('x2:'+str(x2)+' y2:'+str(y2))
			print('_____')



	
print('min:')
print(min_list)
cv2.drawContours(coins, contour_list,  -1, (255,0,0), 1)
cv2.imshow('Objects_Detected',coins)
cv2.waitKey(0)