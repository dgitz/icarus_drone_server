import numpy as np
import cv2
import datetime
import time
import numpy as np
import socket
import roslib
roslib.load_manifest('icarus_drone_server')
packagepath = roslib.packages.get_pkg_dir('icarus_drone_server')
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

matlabserver_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
matlabserver_socket.connect(('192.168.0.102',5005))
resize = 5
class ros_service:
	
	def __init__(self):
		cv2.namedWindow("Gray",1)
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/ardrone/front/image_raw",Image,self.callbackCameraAcquire)
		print 'Starting Image Acquisition'
	def callbackCameraAcquire(self,data):
		color_im = self.bridge.imgmsg_to_cv(data)
		#pdb.set_trace()
		color_image = np.array(color_im)
		new_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
		h,s,v = cv2.split(new_image)
		cv2.imshow("Gray",v)
		gray_image = v
		(height,width) = gray_image.shape	
		gray_image = cv2.resize(gray_image,(width/resize,height/resize))
		myheader = '$CAM,DFV'
		l = '{:08d}'.format(height*width/(resize*resize))
		matlabserver_socket.send(myheader)
		matlabserver_socket.send(l)
		matlabserver_socket.sendall(gray_image)		
def mainloop():
	rospy.init_node('ros_service',anonymous=True)
	rc = ros_service()
	rate = rospy.Rate(10.0)
	while not (rospy.is_shutdown()):
		rate = 1

# When everything done, release the capture
if __name__ == '__main__':
        mainloop()
cv2.destroyAllWindows()