#tcptest
#!/usr/bin/env python

import socket


TCP_IP = '192.168.0.102'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while(True):
	s.send(MESSAGE)
	#data = s.recv(BUFFER_SIZE)
	

	#print "received data:", data
s.close()
