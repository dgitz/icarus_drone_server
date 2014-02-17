#!/usr/bin/python
import cv2

import math
import sys
import time
import numpy as np

from optparse import OptionParser
parser = OptionParser("test_imagepreprocess.py [options]")

#parser.add_option("--targetmode",dest="targetmode",default="Acquire",help="Acquire,Train,Test,Execute")


(opts,args) = parser.parse_args()
#
def mainloop():
	time.sleep(3)
	initvariables()
	
	while False: #Dumb
		lasttime = curtime
		curtime = time.time()
		elapsedtime = (curtime-lasttime)
		boottime = int((curtime-starttime)*1000)
		#sprint boottime
		updaterate = 1/elapsedtime #Hz
		#print updaterate
		dt = datetime.datetime.now()
	
		
		



def initvariables():
	global Current_Yaw_rad
	global Current_Pitch_rad
	global Current_Roll_rad
	global fc_badpacket_counter
	global startime
	global imagenum
	global depth_image
	global color_image
	global mouse_x
	global mouse_y
	global high
	global DEPTH_CAMERA_HEIGHT
	global DEPTH_CAMERA_WIDTH
	global DEPTH_IMAGE_METERS_TO_GRAY
	global num_condensed_array_rows
	global num_condensed_array_cols				
	global max_dist_sector_in
	global min_dist_sector_in
	global lasttime_depth
	global mask_image
	lasttime_depth = 0
	imagenum = 0
	num_condensed_array_rows = 3
	num_condensed_array_cols = 3
	max_dist_sector_in = np.zeros(num_condensed_array_rows*num_condensed_array_cols)
	min_dist_sector_in = np.zeros(num_condensed_array_rows*num_condensed_array_cols)
	mask_image = np.ones((480,640))
	mask_image[375:480,0:640] = np.NaN
	mask_image[250:375,150:375] = np.NaN
	DEPTH_IMAGE_METERS_TO_GRAY = 1.0/4.0
	DEPTH_CAMERA_HEIGHT = -1
	DEPTH_CAMERA_WIDTH = -1
	depth_image_max_intensity = 1
	depth_image_scale = 24
	high = 0
	mouse_x = 0
	mouse_y = 0
	imagenum = 0
	starttime = 0
	timelastsend = 0
	Current_Yaw_rad = 0.0
	Current_Pitch_rad = 0.0
	Current_Roll_rad = 0.0
	fc_badpacket_counter = 0
	WaypointCount = 0	
	
def preprocess(im):
    dumb = 1

		
if __name__ == '__main__':
        mainloop()


