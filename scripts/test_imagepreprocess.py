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
folders = os.listdir(trainimage_dir)
for f in range(len(folders)):
	mypath = trainimage_dir + '\\' + folders[f] + '\\'
	
	myfiles = os.listdir(mypath)
	for i in range(len(myfiles)):
		image_paths.append(trainimage_dir + '\\' + folders[f] + '\\' + myfiles[i])

def mainloop():
	time.sleep(3)
	initvariables()
	cv2.namedWindow("Original Image",1)
	cv2.namedWindow("Processed Image",1)
	for i in range(len(image_paths)):
	    #lasttime = curtime
		#curtime = time.time()
		orig_image = cv2.imread(image_paths[i])
		time.sleep(.1)
		new_image = preprocess(orig_image)
		cv2.imshow("Original Image",orig_image)
		cv2.waitKey(1)
		cv2.imshow("Processed Image",new_image)
		cv2.waitKey(1)
		print 'Finished {}/{} Images'.format(i+1,len(image_paths))
		#elapsedtime = (curtime-lasttime)







def initvariables():
	dumb = 1

def preprocess(orig_image):
    #new_image = orig_image
	black_filter = np.uint8([[[0,0,255]]])
	contour_image = np.uint8([[[0,0,255]]])
	im = np.uint8([[[0,0,0]]])
	new_image = cv2.cvtColor(orig_image,cv2.COLOR_BGR2HSV)
	new_image = new_image * black_filter
	new_image = cv2.cvtColor(new_image,cv2.COLOR_BGR2GRAY)
	(thresh,new_image) = cv2.threshold(new_image,20,255,cv2.THRESH_BINARY)
	if 1:
		contours,hierarchy = cv2.findContours(new_image,1,2)
		cnt = contours[0]
		rect = cv2.minAreaRect(cnt)
		box = cv2.cv.BoxPoints(rect)
		box = np.int0(box)
		cv2.drawContours(new_image,[box],0,(0,0,255),2)
			
	cv2.imshow("Original Image",orig_image)
	cv2.waitKey(1)
	cv2.imshow("Processed Image",new_image)
	cv2.waitKey(1)
	return new_image

if __name__ == '__main__':
        mainloop()


