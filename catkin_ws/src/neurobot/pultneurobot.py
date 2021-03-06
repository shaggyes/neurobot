import pygame
import time
import socket
######################
conn = socket.socket()
#sss = raw_input("continue 192.168. <x.x>: ")
#sss = "192.168." + sss
#conn.connect( (sss, 8080) )
conn.connect( ("192.168.1.154", 8080) )
print("connected")
######################

white = (255, 255, 255)
red = (255, 0, 0)
grey = (100, 100, 100)
green = (0, 255, 0)
blue = (10, 10, 250)
 
pygame.init()
pygame.display.set_caption('Keyboard for robot pobot')
size = [640, 480]
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
 
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
 
# by default the key repeat is disabled
# call set_repeat() to enable it
pygame.key.set_repeat(50, 50)

def filter(sensor, prev, filtConst):
	return ((sensor-prev)*filtConst + prev)
prevcurr = 0

# pack function for sending
def packSpeed(aa,bb):

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
    msg = 'lft{}_rgt{}'.format(l,r)
    #print(msg)
    return msg

ardata = []
filtdata = [0, 0, 0, 0, 0, 0, 0, 0, 0]
k = 5
while True:
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
            # checking if left modifier is pressed
            if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                k = k - 0.5
            if event.key == pygame.K_TAB:
                k = 9
            if pygame.key.get_mods() & pygame.KMOD_RSHIFT:
                k = k + 0.5
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

    ardata = []
    #print('recieve')
    conn.send(packSpeed(x,y))
    #data = b""
    striing = conn.recv(1024)
    for letter in striing:
    	ardata.append(ord(letter))    
    #print(ardata)
    
    if (ardata[0] == 1):
	btn = True

    time.sleep(0.05)
    # draw a wheel speed
    if (x < 0): pygame.draw.rect(screen, red, ((250, 300), (20, 120)), 0)
    elif (x > 0): pygame.draw.rect(screen, green, ((250, 300), (20, 120)), 0)
    if (y < 0): pygame.draw.rect(screen, red, ((370, 300), (20, 120)), 0)
    elif (y > 0): pygame.draw.rect(screen, green, ((370, 300), (20, 120)), 0)
    # draw obstacles
    filtdata[3] = int(filter(ardata[3], filtdata[3], 0.2))
    filtdata[6] = int(filter(ardata[6], filtdata[6], 0.2))
    filtdata[5] = int(filter(ardata[5], filtdata[5], 0.2))
    pygame.draw.rect(screen, blue, ((100, 255-filtdata[3]), (20, 20)), 0)
    pygame.draw.rect(screen, blue, ((300, 255-filtdata[6]), (20, 20)), 0)
    pygame.draw.rect(screen, blue, ((520, 255-filtdata[5]), (20, 20)), 0)

    myfont = pygame.font.SysFont("monospace", 15)
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
    volt = myfont.render(str(7+((ardata[1]-115)*0.067))+"V", 1, (155,200,0))
    screen.blit(volt, (50, 320))

    current = (ardata[2]*2.92-94)/10
    if current < 1:
    	current = 1
    prevcurr = filter(current*0.22, prevcurr, 0.1)
    curr = myfont.render(str(float('{:.3f}'.format(prevcurr))) + "A", 1, (15,200,150))
    screen.blit(curr, (130, 320))

    kkk = myfont.render("Speed " + str(k*10)+"%", 1, (15,200,15))
    screen.blit(kkk, (500, 320))
    GOfont = pygame.font.SysFont("monospace", 90)
    GOlabel = GOfont.render(str("GAME OVER"), 1, (5,0,20))
    if (btn == True):
	screen.blit(GOlabel, (50, 180))

    # draw display update
    pygame.draw.rect(screen, grey, ((280, 300), (80, 120)), 0)
    pygame.display.update()
    clock.tick(20)
conn.close()
