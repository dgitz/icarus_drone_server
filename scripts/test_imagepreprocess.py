#!/usr/bin/python
import cv2
import math
import sys
import time
import numpy as np
import os
import pdb
from optparse import OptionParser
parser = OptionParser("test_imagepreprocess.py [options]")

#parser.add_option("--targetmode",dest="targetmode",default="Acquire",help="Acquire,Train,Test,Execute")

image_paths = []
(opts,args) = parser.parse_args()
mainpath = os.getcwd()
trainimage_dir = mainpath +'..\\..\\media\\RealImages\\'
environment_dir = mainpath +'..\\..\\media\\EnvironmentImages\\'
folders = os.listdir(trainimage_dir)
for f in range(len(folders)):
	mypath = trainimage_dir + '\\' + folders[f] + '\\'
	
	myfiles = os.listdir(mypath)
	for i in range(len(myfiles)):
		image_paths.append(trainimage_dir + '\\' + folders[f] + '\\' + myfiles[i])
myfiles = os.listdir(environment_dir)
for i in range(len(myfiles)):
	image_paths.append(environment_dir + '\\' + myfiles[i])


def mainloop():
	time.sleep(3)
	initvariables()
	cv2.namedWindow("Original Image",1)
	cv2.namedWindow("Processed Image",1)
	cv2.namedWindow("Thresholded Image",1)
	cv2.setMouseCallback("Processed Image",my_mouse_callback)
	for i in range(len(image_paths)):
	    #lasttime = curtime
		#curtime = time.time()
		orig_image = cv2.imread(image_paths[i])
		new_image = preprocess(orig_image)
		print 'Finished {}/{} Images'.format(i+1,len(image_paths))
		#elapsedtime = (curtime-lasttime)







def initvariables():
	global mouse_x
	global mouse_y
	mouse_x = -1
	mouse_y = -1

def my_mouse_callback(event,x,y,flags,param):
	global mouse_x
	global mouse_y
	mouse_x = x
	mouse_y = y

def preprocess(orig_image):
	global mouse_x
	global mouse_y

	filter = np.uint8([[[0,0,255]]])
	#contour_image = np.uint8([[[0,0,255]]])
	height,width = orig_image.shape[:2]
	
	new_image = np.zeros((height,width,3),np.uint8)
	#thresh_image = np.zeros((height,width),np.uint8)
	#proc_image = np.zeros((height,width),np.uint8)
	proc_image = cv2.cvtColor(orig_image,cv2.COLOR_BGR2HSV)
	proc_image = proc_image * filter
	#proc_image = 255 - proc_image 
	proc_image = cv2.cvtColor(proc_image,cv2.COLOR_BGR2GRAY)
	proc_image = cv2.equalizeHist(proc_image)
	(thresh,thresh_image) = cv2.threshold(proc_image,50,255,cv2.THRESH_BINARY_INV)
	'''erode_kernel = np.ones((5,5),np.uint8)
	hproc_image = cv2.erode(thresh_image,erode_kernel,iterations=5)
	dilate_kernel = np.ones((1,1),np.uint8)
	proc_image = cv2.dilate(proc_image,dilate_kernel)'''
	new_image[...,0] = thresh_image * orig_image[...,0]
	new_image[...,1] = thresh_image * orig_image[...,1]
	new_image[...,2] = thresh_image * orig_image[...,2]

	if 0:
		contours,hierarchy = cv2.findContours(proc_image,mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
		cnt = contours[0]
		for i in range(len(contours)):
			if len(contours[i]) > len(cnt):
				cnt = contours[i]
		rect = cv2.minAreaRect(cnt)
		box = cv2.cv.BoxPoints(rect)
		box = np.int0(box)
		print len(cnt)
		cv2.drawContours(orig_image,cnt,-1,(0,0,255),2)

			
	cv2.imshow("Original Image",orig_image)
	cv2.waitKey(1)
	cv2.imshow("Thresholded Image",thresh_image)
	cv2.waitKey(1)
	cv2.imshow("Processed Image",new_image)
	cv2.waitKey(1)
	return new_image

if __name__ == '__main__':
        mainloop()


