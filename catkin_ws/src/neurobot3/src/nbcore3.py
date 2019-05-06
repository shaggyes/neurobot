#!/usr/bin/env python
import sys
import time
import rospy
import datetime
import serial
import os
from subprocess import call
from std_msgs.msg import Int32MultiArray

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)

CommandList = [0, 0, 0, 0, 0] # l,r,0,0,p
def callback(data):
    global CommandList
    #rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
    #rospy.loginfo('I heard %s', data.data)
    CommandList = data.data
    #rospy.spin()

def speedSender ():
	global port, CommandList
	################################## union
	############# basic msg
	right = CommandList[1]/10
	left = CommandList[0]/10
	if (left > 9):
		left = 9
	if (right > 9):
		right = 9
	if (left < -9):
		left = -9
	if (right < -9):
		right = -9
	if (CommandList[4] == '1'):
		print("shutdown now")
		call("sudo shutdown now", shell=True)
	############# send to ardo
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
	################################### end union

##################################################### main part here:

def listener():
	global CommandList, port

	print('preprocedure')
	port.write('0')  ### important
	rospy.init_node('nbcore', anonymous=True)
	pub = rospy.Publisher('neurobotcore', Int32MultiArray, queue_size=1)
	rate = rospy.Rate(10) # 10hz
	Corestr = Int32MultiArray()
	Corestr.data = []
	ardata = []
	currentI = 0

	while not rospy.is_shutdown():

		rospy.Subscriber('neurobotspeed', Int32MultiArray, callback)
		speedSender()
		
		if port.inWaiting:
			ardata = []
			striing = []
			striing = port.read(9)
			for letter in striing[0:10]:
				ardata.append(ord(letter))    
			#print(ardata)
			ardata[1] = int((7 + ((ardata[1]-115)*0.067))*1000)
			currentI = (((ardata[2]*2.92)-94)/10)
			if currentI < 1:
				currentI = 1
			ardata[2] = int((currentI*0.22) * 1000) # in mA

			res = os.popen('vcgencmd measure_temp').readline()
			res = res.replace("temp=","")
			res = res.replace(".","")
			res = res.replace("'C\n","")
			tempI = int(res)/10
			ardata.append(tempI)

			timeN = datetime.datetime.now()
			timeHourInMS = (((timeN.minute*60)+timeN.second)*1000)+(timeN.microsecond/1000)
			ardata.append(timeHourInMS)
			#print(timeHourInMS)
			Corestr.data = ardata
			#rospy.loginfo(Corestr)
			pub.publish(Corestr)
		####################

		rate.sleep()



if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
