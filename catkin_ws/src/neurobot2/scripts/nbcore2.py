#!/usr/bin/env python
import time
import socket
import rospy
import datetime
#from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray

##################### connection
conn = socket.socket()
#sss = raw_input("continue 192.168. <x.x>: ")
#sss = "192.168." + sss
#conn.connect( (sss, 8080) )
conn.connect( ("192.168.1.154", 8080) )
print("connected")
#####################

# pack function for sending
def packSpeed(aa,bb, p):

    a = int(aa)
    b = int(bb)

    if (a > 9):
	a = 9
    if (b > 9):
	b = 9
    if (a < -9):
	a = -9
    if (b < -9):
	b = -9

    if a>-1:
        l = '+{}'.format(a)
    else:
        l = (a)
    if b>-1:
        r = '+{}'.format(b)
    else:
        r = (b)
    msg = 'lft{}_rgt{}_pwr{}'.format(l,r, p)
    #print(msg)
    return msg


a = 0
hahah = [0, 0, 0, 0, 0] # l,r,0,0,p
def callback(data):
    global hahah
    #rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
    #rospy.loginfo('I heard %s', data.data)
    hahah = data.data
    #rospy.spin()

def listener():
    print('preprocedure')
    global a
    global hahah
    rospy.init_node('nbcore', anonymous=True)
    pub = rospy.Publisher('neurobotcore', Int32MultiArray, queue_size=1)
    Corestr = Int32MultiArray()
    Corestr.data = []
    rate = rospy.Rate(10) # 10hz
    currentI = 0
    ardata = []
    timePI = 0
    while not rospy.is_shutdown():
	#print('recieve')
	ardata = []
	conn.send(packSpeed(hahah[0]/10, hahah[1]/10, hahah[4]))
	striing = conn.recv(1024)
	for letter in striing[0:10]:
		ardata.append(ord(letter))    
	#print(ardata)
	ardata[1] = int((7 + ((ardata[1]-115)*0.067))*1000)
	currentI = (((ardata[2]*2.92)-94)/10)
	if currentI < 1:
		currentI = 1
	ardata[2] = int((currentI*0.22) * 1000) # in mA
	timeN = datetime.datetime.now()
	timeCOMP = (((timeN.minute*60)+timeN.second)*1000)+(timeN.microsecond/1000)
	timePI = int(striing[10:len(striing)+1])
	#print(timePI)
	print(timeCOMP, timePI)
	ardata.append(timeCOMP - timePI)
        Corestr.data = ardata
        #rospy.loginfo(Corestr)
        pub.publish(Corestr)
	
        rate.sleep()
	rospy.Subscriber('neurobotspeed', Int32MultiArray, callback)
	#rospy.loginfo(hahah)


if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
