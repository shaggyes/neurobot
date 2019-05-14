#!/usr/bin/env python
import sys
import time
import rospy
import datetime
import serial
import os

from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist

sensor1, sensor2, sensor3, sensor4, sensor5, sensor6 = 0,0,0,0,0,0
CommandList = [0, 0, 0, 0, 0] # l,r,0,0,p
def callback(data):
    global CommandList
    #rospy.loginfo('I heard %s', data.data)
    CommandList = data.data
def senseback1(data):
    global sensor1
    #rospy.loginfo('I heard %s', data)
    #print(data.range)
    sensor1 = int(data.range*100)
def senseback2(data):
    global sensor2
    sensor2 = int(data.range*100)
def senseback3(data):
    global sensor3
    sensor3 = int(data.range*100)
def senseback4(data):
    global sensor4
    sensor4 = int(data.range*100)
def senseback5(data):
    global sensor5
    sensor5 = int(data.range*100)
def senseback6(data):
    global sensor6
    sensor6 = int(data.range*100)

def listener():
	global CommandList, sensor1, sensor2, sensor3, sensor4, sensor5, sensor6

	rospy.init_node('nbcore', anonymous=True)
	pub = rospy.Publisher('neurobotcore', Int32MultiArray, queue_size=1)
	rate = rospy.Rate(10) # 10hz
	Corestr = Int32MultiArray()
	Corestr.data = []
	pubTwist = rospy.Publisher('cmd_vel', Twist, queue_size=1)
	Tweet = Twist()
	Tweet.linear.x, Tweet.angular.z = 0,0
	ardata = []
	currentI = 0

	while not rospy.is_shutdown():

		rospy.Subscriber('neurobotspeed', Int32MultiArray, callback)
		rospy.Subscriber('nebot/sensor/sonar_front', Range, senseback1)
		rospy.Subscriber('nebot/sensor/sonar_left', Range, senseback2)
		rospy.Subscriber('nebot/sensor/sonar_right', Range, senseback3)
		rospy.Subscriber('nebot/sensor/sonar_backf', Range, senseback4)
		rospy.Subscriber('nebot/sensor/sonar_backl', Range, senseback5)
		rospy.Subscriber('nebot/sensor/sonar_backr', Range, senseback6)

		ardata = [0, 12000, 1000, sensor3, sensor5, sensor2, sensor1, sensor4, sensor6, 36, 1]
			
		#currentI = 0.2
		#if currentI < 0.1:
		#	currentI = 0.1
		#ardata[2] = int(currentI*1000)
		timeN = datetime.datetime.now()
		timeHourInMS = (((timeN.minute*60)+timeN.second)*1000)+(timeN.microsecond/1000)
		ardata[10] = (timeHourInMS)

		Corestr.data = ardata
		#rospy.loginfo(Corestr)
		#print(ardata)
		pub.publish(Corestr)
		Tweet.linear.x = ((CommandList[0]+CommandList[1])/100)
		Tweet.angular.z = ((CommandList[0] - CommandList[1])/50)
		pubTwist.publish(Tweet)
		rate.sleep()



if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
