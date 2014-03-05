#!/usr/bin/python
import roslib
roslib.load_manifest('icarus_drone_server')
packagepath = roslib.packages.get_pkg_dir('icarus_drone_server')
import rospy
from std_msgs.msg import String, Header
from sensor_msgs.msg import NavSatFix, NavSatStatus, Imu,CameraInfo
from icarus_drone_server.msg import *
import pdb
import math
import sys
import os
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from stereo_msgs.msg import DisparityImage
from sensor_msgs.msg import Joy
import tf
import datetime
import time
import socket
import errno
import serial
import shutil
import socket
import numpy as np
np.set_printoptions(threshold=np.nan)

xmitmode = 'TCP'
if xmitmode == 'UDP':
	matlabserver_ip = '192.168.0.102'
	matlabserver_port = 5006
elif xmitmode == 'TCP':
	matlabserver_ip = '192.168.0.102'
	matlabserver_port = 5005

#import rgbdslam.msg

CONFIDENCE_LIMIT = 75

from collections import namedtuple
from pprint import pprint
import numpy as np

from optparse import OptionParser
parser = OptionParser("drone_server.py [options]")
#parser.add_option("--gcs-device",dest="gcs_device",default="None",help="GCS Device Connection: /dev/ttyUSB0,10.7.45.208,etc")
#parser.add_option("--mode",dest="mode",default="None",help="net,slam,None")
parser.add_option("--nav",dest="nav",default=False)
parser.add_option("--slam",dest="slam",default=False)
parser.add_option("--targetmode",dest="targetmode",default="Test",help="Acquire,Train,Test,Execute,Test")
parser.add_option("--target_acquire_mode",dest="target_acquire_mode",default="Live",help="Live,Simulated")
parser.add_option("--target_acquire_class",dest="target_acquire_class",default="None",help="Name of Target Class")
parser.add_option("--target_acquire_count",dest="target_acquire_count",default="400",help="Number of Images to acquire")
parser.add_option("--target_acquire_rate",dest="target_acquire_rate",default="10",help="Number of Images to acquire per second")
parser.add_option("--script",dest="script",default='Script7',help="Image Preprocessing Script")
parser.add_option("--use_joystick",dest="use_joystick",default='True',help="True or False")
parser.add_option("--debug",dest="debug",default='True',help="True or False")


(opts,args) = parser.parse_args()
#print "Flight Controller: " + opts.fc_device
#print "device_gcs.device: " + opts.gcs_device
#print "Flight Controller GPS: " + opts.fcgps_device
#print "Remote: " + opts.remote_device

#WaypointStruct = namedtuple('WaypointStruct',['seq','frame','command','current','autocontinue','param1','param2','param3','param4','x','y','z'])
 
		

#my_MissionItems.append(missionitem())
#my_MissionItems[0].x = 41.3
#my_MissionItems[0].y = -87.3
#print my_MissionItems[0].calc_relbearing(12.0,37.0)
#print my_MissionItems[0].calc_distance(12.0,37.0)


targetmode = opts.targetmode

if opts.slam == "True":
	slam_enabled = True
else:
	slam_enabled = False
if opts.nav == "True":
	nav_enabled = True
else:
	nav_enabled = False
if opts.use_joystick == "True":
	use_joystick = True
else:
	use_joystick = False
if opts.debug == "True":
	DEBUG = True
else:
	DEBUG = False
resize = 1
row_sectors = 1
col_sectors = 1
if opts.script == 'Script2':
	resize = 2
	row_sectors = 4
	col_sectors = 4
elif opts.script == 'Script4':
	resize = 10
	row_sectors = 6
	col_sectors = 6
elif opts.script == 'Script6':
	resize = 4
	row_sectors = 6
	col_sectors = 6
elif opts.script == 'Script7':
	resize = 10

if targetmode == "Acquire":
	target_acquire_mode = opts.target_acquire_mode
	if target_acquire_mode == "Live":
		target_acquire_class = opts.target_acquire_class
		target_acquire_count = int(opts.target_acquire_count)
		target_acquire_rate = float(opts.target_acquire_rate)
		target_acquire_classdir = packagepath + '/media/UnmappedImages/{}/'.format(target_acquire_class)

		if not os.path.exists(target_acquire_classdir):
			os.makedirs(target_acquire_classdir,0777)
		else:
			shutil.rmtree(target_acquire_classdir)
			os.makedirs(target_acquire_classdir,0777)
		



	
	


'''if slam_enabled:
	pub_gps = rospy.Publisher('GPS',rgbdslam.msg.GPS)
	pub_pos = rospy.Publisher('Position',rgbdslam.msg.Position)
	pub_attitude = rospy.Publisher('Attitude',rgbdslam.msg.Attitude)
	pub_data_to_fc_gps = rospy.Publisher('Data_To_FC_GPS',rgbdslam.msg.DataToFCGPS)
	pub_data_to_fc = rospy.Publisher('Data_To_FC',rgbdslam.msg.DataToFC)
	pub_data_from_fc = rospy.Publisher('Data_From_FC',rgbdslam.msg.DataFromFC)'''



my_MissionItems = []
#WaypointStruct = namedtuple('WaypointStruct',['seq','frame','command','current','autocontinue','param1','param2','param3','param4','x','y','z'])

class ros_service:
	
	def __init__(self):
		if targetmode == "Acquire":
			cv2.namedWindow("RGB",1)
			self.bridge = CvBridge()
			self.image_sub = rospy.Subscriber("/ardrone/front/image_raw",Image,self.callbackCameraAcquire)
			print 'Starting Image Acquisition'
		elif targetmode == "Execute":	
			self.bridge = CvBridge()
			self.poseestimate_sub = rospy.Subscriber("/ardrone/predictedPose",filter_state,self.cb_pose_estimate)
			self.frontimg_sub = rospy.Subscriber("/ardrone/front/image_raw",Image,self.cb_newfront_img)
			if xmitmode == 'TCP':
				matlabserver_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				matlabserver_socket.connect((matlabserver_ip,matlabserver_port))
			elif xmitmode == 'UDP':
				matlabserver_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		elif targetmode == 'Test': #For Development/debugging only
			if use_joystick:
				self.joy = rospy.Subscriber('joy', Joy, self.joyCallback)
	def joyCallback(self, joy):
		self.joyaxis_pitch = 1
		self.joyaxis_roll = 0
		self.joyaxis_throttle = 3
		self.joyaxis_yaw = 2
		self.joybutton_takeoff = 0
		self.joybutton_land = 2
		if joy.buttons[self.joybutton_takeoff]:
			if DEBUG:print 'Taking Off'
		if joy.buttons[self.joybutton_land]:
			if DEBUG:print 'Landing'
		if DEBUG:print 'P: {:.2f} R: {:.2f} Y: {:.2f} T: {:.2f}'.format(joy.axes[self.joyaxis_pitch],joy.axes[self.joyaxis_roll],joy.axes[self.joyaxis_yaw],joy.axes[self.joyaxis_throttle])

		
	def cb_newfront_img(self,data):
		global imagenum
		color_im = self.bridge.imgmsg_to_cv(data)
		color_image = np.array(color_im)
		(height,width,depth) = color_image.shape	
		color_image = cv2.resize(color_image,(width/resize,height/resize))
		myheader = '$CAM,DFV'
		l = '{:08d}'.format(height*width*depth/(resize*resize))
		if xmitmode == 'UDP':
			matlabserver_socket.sendto(myheader,(matlabserver_ip,matlabserver_port))
			matlabserver_socket.sendto(l,(matlabserver_ip,matlabserver_port))
			matlabserver_socket.sendto(color_image,(matlabserver_ip,matlabserver_port))
		elif xmitmode == 'TCP':
			matlabserver_socket.send(myheader)
			matlabserver_socket.send(l)
			matlabserver_socket.sendall(color_image)
		time.sleep(.25)
	def cb_pose_estimate(self,data):
		global pose_x
		global pose_y
		global pose_z
		global pose_roll
		global pose_yaw
		global pose_pitch
		pose_roll = data.roll
		pose_pitch = data.pitch
		pose_yaw = data.yaw
		pose_x = data.x
		pose_y = data.y
		pose_z = data.z
		
	def callbackCameraAcquire(self,data):
		global imagenum
		global gInitComplete
		if gInitComplete:
			try:
				if imagenum < target_acquire_count:
					imagenum = imagenum + 1
					time.sleep(1/target_acquire_rate)
					tempstr = 'Image{:04d}.png'.format(imagenum)
					color_im = self.bridge.imgmsg_to_cv(data)
					#pdb.set_trace()
					color_image = np.array(color_im)
					cv2.imshow("RGB",color_image)
					(height,width,depth) = color_image.shape	
					color_image = cv2.resize(color_image,(width/resize,height/resize))
					
					filename = '{}{}'.format(target_acquire_classdir,tempstr)
					cv2.imwrite(filename,color_image)
					print 'Image: {}/{} Completed.'.format(imagenum,target_acquire_count)
					cv2.waitKey(1)
				else:
					print 'Image Acquisition Finished'
				
			except CvBridgeError,e:
				print e

	
def mainloop():
	initvariables()
	global WaypointCount
	global Current_Pitch_rad
	global Current_Roll_rad
	global Current_Yaw_rad
	global starttime
	global first_attitude_packet
	global Initial_Yaw_rad
	global my_MissionItems
	global imagenum
	global pose_x
	global pose_y
	global pose_z
	global pose_roll
	global pose_pitch
	global pose_yaw
	global target_x
	global target_y
	global target_class
	global last_target_x
	global last_target_y
	global gInitComplete
	my_MissionItems = []
	#device_gcs.display()
	first_attitude_packet = True
	Initial_Yaw_rad = 0.0
	initiallocation = [41.8702840000,87.6492970000,240.0]
	curlocation = [0,0,0]
	curlocation[0] = initiallocation[0]
	curlocation[1] = initiallocation[1]
	curlocation[2] = initiallocation[2]
	#rospy.init_node('pc',anonymous=True)
	
	
	rospy.init_node('ros_service',anonymous=True)
	rc = ros_service()
	rate = rospy.Rate(10.0)
	listener = tf.TransformListener()
	break_counter = 0
	break_counter_max = 20

	

	curx = 0.0
	cury = 0.0
	curz = 0.0
	lastx = 0.0
	lasty = 0.0
	del_dist = 0.0
	lasttime = 0.0
	starttime = time.time()
	curtime = starttime
	user_command = "q"
	#device_mc.changemode(mavlink.MAV_MODE_PREFLIGHT)		
	print "Waiting 2 seconds..."
	rospy.sleep(2)
	gInitComplete = True
	print 'Initialization Complete.  Starting Mode: {}'.format(targetmode)
	#device_mc.changemode(mavlink.MAV_MODE_MANUAL_DISARMED)	
	
        
	#device_fc.changemode(mavlink.MAV_MODE_PREFLIGHT)
	
	#rospy.sleep(5) #Wait 15 seconds to allow all devices to powerup
	
	#device_mc.changemode(mavlink.MAV_MODE_MANUAL_DISARMED)

	while not (rospy.is_shutdown()):
		#time.sleep(1)
		#tempstr = 'image{}.png'.format(imagenum)
		#imagenum = imagenum + 1
		#print tempstr
		#cv2.imwrite(tempstr,color_image)
		#time.sleep(.001)
		rospy.sleep(0.001)
		lasttime = curtime
		curtime = time.time()
		elapsedtime = (curtime-lasttime)
		boottime = int((curtime-starttime)*1000)
		#sprint boottime
		updaterate = 1/elapsedtime #Hz
		#print updaterate
		dt = datetime.datetime.now()
		#print "x: {}, y: {}, z: {}, r: {}, p: {}, y: {}".format(pose_x,pose_y,pose_z,pose_roll,pose_pitch,pose_yaw)
		if targetmode == 'Execute':
			
			icarus_msghandler(matlabserver_socket)
			print 'Class: {} X:{} Y: {}'.format(target_class,target_x,target_y)
	print 'Exiting Program'
	matlabserver_socket.close()
	time.sleep(5)
			
			
		
		

def icarus_msghandler(mysocket):
	try:
		global target_x
		global target_y
		global last_target_x
		global last_target_y
		global target_class
		if xmitmode == 'TCP':
			packet_type = mysocket.recv(8)
			packet_length = mysocket.recv(8)
		elif xmitmode == 'UDP':
			packet_type = mysocket.recvfrom(8)
			packet_length = mysocket.recvfrom(8)
		if packet_type.find('$') >= 0:
			packet_length = int(packet_length)
			if xmitmode == 'TCP':
				msg = mysocket.recv(packet_length)
			elif xmitmode == 'UDP':
				msg = mysocket.recvfrom(packet_length)
			if packet_type == '$TGT,DFV':
				mystr = msg.split(',')
				if int(mystr[3]) > CONFIDENCE_LIMIT:
					target_class = mystr[0]
					if target_class <> 'None':
						target_x = int(mystr[1])
						target_y = int(mystr[2])
						last_target_x = target_x
						last_target_y = target_y
					else:
						target_x = last_target_x
						target_y = last_target_y
	except IndexError:
		pdb.set_trace()
			
	
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
	global pose_x
	global pose_y
	global pose_z
	global pose_roll
	global pose_pitch
	global pose_yaw
	global front_image_vector
	global imagenum
	global target_x
	global target_y
	global target_class
	global last_target_x
	global last_target_y
	global gInitComplete
	gInitComplete = False
	last_target_x = 0
	last_target_y = 0
	target_x = -1
	target_y = -1
	target_class = 'None'
	imagenum = 0
	front_image_vector = []
	pose_x = 0
	pose_y = 0
	pose_z = 0
	pose_roll = 0
	pose_pitch = 0
	pose_yaw = 0
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
	
def dec2gpsdeg(num):
  #a = [0, 0, 0]
  #a[0] = int(num)
  #a[1] = int((num*60.0) % 60)
  #a[2] = (num*3600.0)%60
  a = [0,0]
  a[0] = int(num)
  a[1] = (num*60.0)%60
  return a
def datetime2gpsdatetime(item):
  a = [0,0,0,0,0,0]
  a[0] = item.hour
  a[1] = item.minute
  a[2] = item.second + item.microsecond/1000000.0
  a[3] = item.day
  a[4] = item.month
  a[5] = item.year-2000
  return a


def calcchecksum(item):
	s = 0
	for i in range(len(item) ):
    		s = s ^ ord(item[i])
	s = "%02X" % s
	return s

		
if __name__ == '__main__':
        mainloop()


