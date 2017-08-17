import random, pygame, sys
from pygame.locals import *
from time import sleep
import RPi.GPIO as GPIO

print('ON')

#Define Pin GPIO addresses

Ping=17
#Ping is Master to Slave serial

Pong=4
#Pong is Slave to Master serial

Pins=[18,27,22,23,24,10,9,25,11,8,7,5,6,12,13,19]
#Comm pins (should be 16)

Nibble=[16,26,20,21]
#Data bus conveying current pin

Kill=14
#Master reset, exits script

SoftKill=15
#Game reset

#Set up Ping, Pong, Kills, and Nibble
GPIO.setmode(GPIO.BCM)
GPIO.setup(Ping, GPIO.OUT)
GPIO.output(Ping, 0)
GPIO.setup(Pong, GPIO.IN)
GPIO.setup(Kill, GPIO.OUT)
GPIO.output(Kill, 0)
GPIO.setup(SoftKill, GPIO.OUT)
GPIO.output(SoftKill, 0)
x=0
for x in range(0,4):
    GPIO.setup(Nibble[x],GPIO.IN)
    
size=len(Pins)
#should be 16

#Set up Pins
for x in range(0,size):
    GPIO.setup(Pins[x], GPIO.IN)
#End Setup

#Debounce
input_value=GPIO.input(Pong)
#print(str(input_value))
sleep(0.1)
input_value=GPIO.input(Pong)
#print(str(input_value))
sleep(0.1)
input_value=GPIO.input(Pong)
#print(str(input_value))
sleep(0.1)

print('GPIO Setup Complete')

#Set up game display

pygame.init()

FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((1920,1080),pygame.RESIZABLE)

pygame.display.set_caption("GPIO Game")

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

img0 = pygame.image.load("black.png")
img1 = pygame.image.load("img1.png")
img2 = pygame.image.load("img2.png")
img3 = pygame.image.load("img3.png")
img4 = pygame.image.load("img4.png")
img5 = pygame.image.load("img5.png")
img6 = pygame.image.load("img6.png")
img7 = pygame.image.load("img7.png")
img8 = pygame.image.load("img8.png")
img9 = pygame.image.load("img9.png")
img10 = pygame.image.load("img10.png")
img11 = pygame.image.load("img11.png")
img12 = pygame.image.load("img12.png")
img13 = pygame.image.load("img13.png")
img14 = pygame.image.load("img14.png")
img15 = pygame.image.load("img15.png")
img16 = pygame.image.load("img16.png")

imgs=[img0,img1,img2,img3,img4,img5,img6,img7,img8,img9,img10,img11,img12,img13,img14,img15,img16]


imgx = [0,480,960,1440]
imgy = [0,270,540,810]


DISPLAYSURF.fill(BLACK)


#Set up game variables


#Begin Master Loop

play = 1

level = 1

for x in range(0,4):
    for y in range(0,4):
        #DISPLAYSURF.blit(imgs[1+x+4*y],(imgx[x],imgy[y]))
        DISPLAYSURF.blit(imgs[0],(imgx[x],imgy[y]))
pygame.display.flip()

#Game is ready, wait for slave to signal ready
#while True:
    #do nothing
#    if GPIO.input(Pong):
#        print("Pong")
#        GPIO.output(Ping,1)
#        while GPIO.input(Pong):
#            #wait for Slave to respond
#            if not GPIO.input(Pong):
#                break
#        GPIO.output(Ping,0)
#        break
#print("Slave awake and ready")
GPIO.output(SoftKill,1)
sleep(0.0001)
GPIO.output(SoftKill,0)

print('Initialized')

wincondition = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

Connect=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LastConnect=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

while play:

    #GPIO.output(SoftKill,1)
    #GPIO.output(SoftKill,0)


    #Detect wire connectivity

    #Make sure slave is on wire 0
    wirein=0
    while not(wirein==1):
        binary = "0b"
        for y in range(0,4):
            binary = binary + str(GPIO.input(Nibble[y]))
        wirein=int(binary,2)+1
    
    
    Connect=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #sleep(0.1)
    while wirein < 16:


        #Game is ready, wait for slave to signal next pin
        while not GPIO.input(Pong):
            #do nothing
            if GPIO.input(Pong):
                break
#        print("Pong")
        
        binary = "0b"
        for y in range(0,4):
            binary = binary + str(GPIO.input(Nibble[y]))
        wirein=int(binary,2)+1
#        print(str(wirein))

        for w in range(0,size):
            input_value = GPIO.input(Pins[w])
            if input_value == 1:
                Connect[w]=wirein
        #Now signal for next pin
#        print("Ping")
        GPIO.output(Ping,1)
        sleep(0.0001)
        GPIO.output(Ping,0)
        #while True:
        #    if GPIO.input(Pong) == 1:
        #        GPIO.output(Ping,0)
        #        sleep(0.1)
        #        break
    #End of pins
    if not(Connect==LastConnect):
        for a in range(0,size):
            b=a%4
            c=a//4
            DISPLAYSURF.blit(imgs[Connect[a]],(imgx[b],imgy[c]))
        pygame.display.flip()

    LastConnect=Connect

    GPIO.output(SoftKill,1)
    sleep(0.0001)
    GPIO.output(SoftKill,0)
    sleep(0.5)
    
    if Connect == wincondition:
        print("WIN!")
        level = level + 1
        random.shuffle(Pins)
        if level == 3:
            play = 0
            break
        Connect=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        LastConnect=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        DISPLAYSURF.fill(BLACK)
        pygame.display.flip()
        sleep(0.2)
        DISPLAYSURF.fill(WHITE)
        pygame.display.flip()
        sleep(0.2)
        DISPLAYSURF.fill(BLACK)
        pygame.display.flip()
        sleep(0.2)
        DISPLAYSURF.fill(WHITE)
        pygame.display.flip()
        sleep(0.2)
        DISPLAYSURF.fill(BLACK)
        pygame.display.flip()
        sleep(0.2)
        

    for event in pygame.event.get():
        if event.type == QUIT:
            print(str("end"))
            GPIO.output(SoftKill,1)
            sleep(0.01)
            GPIO.cleanup()
            print("cleaned")
            pygame.quit()
            sys.exit()

print(str("end"))
GPIO.output(SoftKill,1)
sleep(0.01)
GPIO.cleanup()
print("cleaned")
pygame.quit()
sys.exit() 
