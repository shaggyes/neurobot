#!/usr/bin/env python
import pygame
import time
import rospy
import datetime
import sys
#from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray
b = 0
hah = [0,0,0,255,0,255,255,0,0, 36, 0] # plus temp and time
def yellow(data):
    global hah
    #rospy.loginfo('Secheard %s', data.data)
    hah = data.data
    

def talker():
    global b
    global hah
############################ // pygame main
    prevcurr = 0

    white = (255, 255, 255)
    red = (255, 0, 0)
    grey = (100, 100, 100)
    green = (0, 255, 0)
    blue = (10, 10, 250)

    pygame.init()
    pygame.display.set_caption('Keyboard for Neurobot3Ros')
    size = [640, 480]
    screen = pygame.display.set_mode(size)
    #clock = pygame.time.Clock()

    x = 0
    y = 0
    obst1 = 0
    obst2 = 0
    obst3 = 0
    obst4 = 0
    obst5 = 0
    obst6 = 0
    voltage = 0
    current = 0
    btn = False

    pygame.key.set_repeat(50, 50)

    ardata = []
    filtdata = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    k = 5
############################

    rospy.init_node('nbpult', anonymous=True)
    pub = rospy.Publisher('neurobotspeed', Int32MultiArray, queue_size=1)
    
    
    speed = Int32MultiArray()
    speed.data = []
    rate = rospy.Rate(10) # 10hz
    lol = 0
    myfont = pygame.font.SysFont("monospace", 15)
    GOfont = pygame.font.SysFont("monospace", 90)
    GOlabel = GOfont.render(str("GAME OVER"), 1, (5,0,20))
    while not rospy.is_shutdown():
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
		    pygame.quit()
		    sys.exit()
		# check if key is pressed
		# if you use event.key here it will give you error at runtime
		if event.type == pygame.KEYDOWN:
		    #print('will sendspeed with ', k)
		    if event.key == pygame.K_LEFT:
			x = k
			y = -k
		    if event.key == pygame.K_RIGHT:
			x = -k
			y = k
		    if event.key == pygame.K_UP:
			x = k
			y = k
		    if event.key == pygame.K_DOWN:
			y = -k
			x = -k
		    # checking if turbo modifier is pressed
		    if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
			k = k - 0.5
		    if event.key == pygame.K_TAB:
			k = 9
		    if pygame.key.get_mods() & pygame.KMOD_RSHIFT:
			k = k + 0.5
		    if event.key == pygame.K_ESCAPE:
			btn = True
		    if event.key == pygame.K_f:
			if (lol == 0):
				lol = 1
			else:
				lol = 0	
		    if event.key == pygame.K_BACKSPACE:
		    	pygame.quit()
		    	sys.exit()
		    #conn.send(packSpeed(x,y))    
		else:
		    #print('send0')
		    #conn.send('lft00_rgt00')
		    x = 0
		    y = 0

	if k > 10:
		k = 10
	elif k < 1:
		k = 1

	screen.fill(white)


	rospy.Subscriber('neurobotcore', Int32MultiArray, yellow)
        speed.data = [x*10, y*10, 0, 0, btn]
        #rospy.loginfo(yellow.data)
        pub.publish(speed)
	rospy.loginfo(hah)

	ardata = hah

################## draw part
	if (ardata[0] == 1):
		btn = True

	time.sleep(0.05)
	# draw a wheel speed
	if (x < 0): pygame.draw.rect(screen, red, ((250, 300), (20, 120)), 0)
	elif (x > 0): pygame.draw.rect(screen, green, ((250, 300), (20, 120)), 0)
	if (y < 0): pygame.draw.rect(screen, red, ((370, 300), (20, 120)), 0)
	elif (y > 0): pygame.draw.rect(screen, green, ((370, 300), (20, 120)), 0)
	# draw obstacles
	filteredD = myfont.render("Filtered", 1, (200,10,160))
	if (lol == 0):
		filtdata[3:8] = ardata[3:8]
		prevcurr = ardata[2]/1000
	else:
		filtdata[3] = int(filter(ardata[3], filtdata[3], 0.2))
		filtdata[6] = int(filter(ardata[6], filtdata[6], 0.2))
		filtdata[5] = int(filter(ardata[5], filtdata[5], 0.2))
		prevcurr = filter(ardata[2]/1000, prevcurr, 0.1)
		screen.blit(filteredD, (500, 370))

	pygame.draw.rect(screen, blue, ((100, 255-filtdata[3]), (20, 20)), 0)
	pygame.draw.rect(screen, blue, ((300, 255-filtdata[6]), (20, 20)), 0)
	pygame.draw.rect(screen, blue, ((520, 255-filtdata[5]), (20, 20)), 0)

	label = myfont.render(str(filtdata[3]), 1, (155,0,0))
	screen.blit(label, (115, 100))
	label2 = myfont.render(str(filtdata[6]), 1, (155,0,0))
	screen.blit(label2, (320, 100))
	label3 = myfont.render(str(filtdata[5]), 1, (155,0,0))
	screen.blit(label3, (540, 100))
	label4 = myfont.render(str(ardata[4]), 1, (55,0,200))
	screen.blit(label4, (115, 440))
	label5 = myfont.render(str(ardata[7]), 1, (55,0,200))
	screen.blit(label5, (310, 450))
	label6 = myfont.render(str(ardata[8]), 1, (55,0,200))
	screen.blit(label6, (540, 440))

	####################
	volt = myfont.render(str(float(ardata[1])/1000)+"V", 1, (155,200,0))
	screen.blit(volt, (50, 320))

	curr = myfont.render(str(float('{:.3f}'.format(prevcurr))) + "A", 1, (15,200,150))
	screen.blit(curr, (130, 320))

	kkk = myfont.render("Speed " + str(k*10)+"%", 1, (15,200,15))
	screen.blit(kkk, (500, 320))

	if (btn == True):
		screen.blit(GOlabel, (50, 180))
	timeN = datetime.datetime.now()
	timeHOURinMS = (((timeN.minute*60)+timeN.second)*1000)+(timeN.microsecond/1000)
	timedelta = timeHOURinMS - ardata[10]
	timeP = myfont.render(str(timedelta)+"ms", 1, (15,20,100))  ########### on core
	screen.blit(timeP, (50, 370))
	tempPi = myfont.render(str(float(ardata[9]))+"c0", 1, (230,30,30))
	screen.blit(tempPi, (130, 370))	
	
	# draw display update
	pygame.draw.rect(screen, grey, ((280, 300), (80, 120)), 0)
	pygame.display.update()
##################
        rate.sleep()



def filter(sensor, prev, filtConst):
	return ((sensor-prev)*filtConst + prev)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
