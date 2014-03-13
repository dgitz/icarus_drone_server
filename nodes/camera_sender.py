import numpy as np
import cv2
import datetime
import time
import numpy as np
import socket
cap = cv2.VideoCapture(0)
matlabserver_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
matlabserver_socket.connect(('192.168.0.102',5005))
resize = 10
while(True):
	starttime = time.time()
	# Capture frame-by-frame
	ret, frame = cap.read()
	#color_image = np.array(frame)
	#(height,width,depth) = color_image.shape
	myheader = '$CAM,DFV00009216'
	#l = '{:08d}'.format(height*width*depth/(resize*resize))
	print '{}'.format(myheader)
	matlabserver_socket.send(myheader)
	#matlabserver_socket.send(l)
	matlabserver_socket.sendall(frame)
	# Our operations on the frame come here
	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Display the resulting frame
	'''cv2.imshow('frame',color_image)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break'''

	etime = time.time() - starttime
	print 'Rate: {} Hz'.format(1/etime)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
