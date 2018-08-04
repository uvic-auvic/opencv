import cv2, matplotlib
import numpy as np
import matplotlib.pyplot as plt

cap2 = cv2.VideoCapture('foot.MP4')

while (True):
    _, frame = cap2.read()
    orignal = frame.copy()

    big_area_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    big_area_preprocessed = cv2.GaussianBlur(big_area_gray, (5, 5), 0)

    # get binary image
    _, big_area_binary = cv2.threshold(big_area_preprocessed, 150, 255, cv2.THRESH_BINARY_INV)

    # invert image to get big_area
    big_area_binary = cv2.bitwise_not(big_area_binary)

    _, big_contours, hierarchy = cv2.findContours(big_area_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    big_contour_list = []
    center_list = []
    area_list = []
    for big_contour in big_contours:
        approx = cv2.approxPolyDP(big_contour, 0.01 * cv2.arcLength(big_contour, True), True)
        area = cv2.contourArea(big_contour)
        if ( 1000 > area > 50):
            print('approx:')
            print(len(approx))
            big_contour_list.append(big_contour)
            (x, y), radius = cv2.minEnclosingCircle(big_contour)
            center = (int(x), int(y))
            center_list.append(center)
            area_list.append(area)

    cv2.drawContours(orignal, big_contour_list, -1, (255, 0, 0), 1)

    cv2.imshow('frame', orignal)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap2.release()
cv2.destroyAllWindows()