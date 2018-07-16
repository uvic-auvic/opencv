import cv2
import numpy as np

WIDTH_PIXEL_TO_METERS = 1000.0
HEIGHT_PIXEL_TO_METERS = 1000.0

class Buoy():
	contour = None

	x=0
	y=0
	w=0
	h=0

	def __init__(self):
		pass

	def find(self, contours):
		self.contour = contours[0]
		self.x,self.y,self.w,self.h = cv2.boundingRect(self.contour)

	
	def get_contour(self):
		return self.contour

	def get_find_dimensions(self):
		return self.x,self.y,self.w,self.h

	def measure(self):
		d1 = HEIGHT_PIXEL_TO_METERS / self.h
		d2 = WIDTH_PIXEL_TO_METERS / self.w
		return ((d1 + d2) / 2)
		
