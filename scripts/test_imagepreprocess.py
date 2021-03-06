#!/usr/bin/python
import cv2
import math
import sys
import time
import numpy as np
import os
import pdb
from optparse import OptionParser
import imp
mainpath = os.getcwd()
helperpath = os.getcwd() + '/../src/icarus_helper.py'
icarus_helper = imp.load_source('icarus_helper',helperpath)
parser = OptionParser("test_imagepreprocess.py [options]")

#parser.add_option("--targetmode",dest="targetmode",default="Acquire",help="Acquire,Train,Test,Execute")

image_paths = []
(opts,args) = parser.parse_args()
mainpath = os.getcwd()
if sys.platform == 'linux2':
	trainimage_dir = mainpath + '/../media/RealImages/'
	environment_dir = mainpath + '/../media/EnvironmentImages/'	
else:
	trainimage_dir = mainpath +'..\\..\\media\\RealImages\\'
	environment_dir = mainpath +'..\\..\\media\\EnvironmentImages\\'
folders = os.listdir(trainimage_dir)
for f in range(len(folders)):
	if sys.platform == 'linux2':
		mypath = trainimage_dir + '/' + folders[f] + '/'
	else:
		mypath = trainimage_dir + '\\' + folders[f] + '\\'
	
	myfiles = os.listdir(mypath)
	for i in range(len(myfiles)):
		if sys.platform == 'linux2':
			image_paths.append(trainimage_dir + '/' + folders[f] + '/' + myfiles[i])
		else:
			image_paths.append(trainimage_dir + '\\' + folders[f] + '\\' + myfiles[i])
myfiles = os.listdir(environment_dir)
for i in range(len(myfiles)):
	if sys.platform == 'linux2':
		image_paths.append(environment_dir + '/' + myfiles[i])
	else:
		image_paths.append(environment_dir + '\\' + myfiles[i])


def mainloop():
	time.sleep(3)
	initvariables()
	cv2.namedWindow("Original Image",1)
	cv2.namedWindow("Processed Image",1)
	for i in range(len(image_paths)):
	    #lasttime = curtime
		#curtime = time.time()
		orig_image = cv2.imread(image_paths[i])
		new_image = icarus_helper.preprocess(orig_image)
		print 'Finished {}/{} Images'.format(i+1,len(image_paths))
		#elapsedtime = (curtime-lasttime)
		cv2.imshow("Original Image",orig_image)
		cv2.waitKey(1)
		cv2.imshow("Processed Image",new_image)
		cv2.waitKey(1)






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


if __name__ == '__main__':
        mainloop()


