# Standard imports
import cv2
import numpy as np;
 
cap = cv2.VideoCapture(0)

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
# Read image
#im = cv2.imread("123.jpg", cv2.IMREAD_GRAYSCALE)
while(True):

	ret, im = cap.read()

	# Set up the detector with default parameters.
	# detector = cv2.SimpleBlobDetector_create()  #python2
	detector = cv2.SimpleBlobDetector_create()
	 
	# Detect blobs.
	keypoints = detector.detect(im)
	 
	# Draw detected blobs as red circles.
	# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
	im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	 
	# Show keypoints
	cv2.imshow('frame',im_with_keypoints)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()