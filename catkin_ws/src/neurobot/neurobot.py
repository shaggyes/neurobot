#!/usr/bin/env python3

import time
import socket

import serial, time
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)
port.write('0')  ### important

sock = socket.socket()
sock.bind( ("", 8080) )
sock.listen(20)
print("Listening socket")

right = 0
left = 0

def unpackSpeed(msg):
	if (msg[0:3] == 'lft'):
		left = int(msg[3:5])
		right = int(msg[9:11])
	else:
		left = 0
		right = 0

	if (len(msg) > 11):
		print("additions:")
	return left, right

conn, addr = sock.accept()
print("New connection from " + addr[0])
ardata = [1]

while True:
	data = conn.recv(1024)
	udata = data.decode("utf-8")
	#print("Data: " + udata)
	time.sleep(0.01)
	left, right = unpackSpeed(udata)
	#############
	if (left > 9):
		left = 9
	if (right > 9):
		right = 9
	if (left < -9):
		left = -9
	if (right < -9):
		right = -9
	#############
	if (left > 0):
		if (right > 0):
			f = int(float(left)/2+0.5)
			port.write(chr(f+48))
			print('forw')
		else:
			f = (left+2)/3
			port.write(chr(f+67))
			print('left')
	elif (left < 0):
		if (right > 0):
			f = (right+2)/3
			port.write(chr(f+64))
			print('right')
		else:
			f = int(float(-1*left)/2+0.5)
			port.write(chr(f+53))
			print('back')
	else:
		port.write('0')


	###################
	if port.inWaiting:
		striing = port.read(9)
		ardata = []
		for letter in striing:
			ardata.append(ord(letter))
		conn.send(striing)
conn.close()
conn, addr = sock.accept()
