import pygame, sys
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
GPIO.setup(Pong, GPIO.OUT)
GPIO.output(Pong, 0)
GPIO.setup(Ping, GPIO.IN)
GPIO.setup(Kill, GPIO.IN)
GPIO.setup(SoftKill, GPIO.IN)
x=0
for x in range(0,4):
    GPIO.setup(Nibble[x],GPIO.OUT)
    GPIO.output(Nibble[x],0)
    
size=len(Pins)
#should be 16

#Set up Pins
for x in range(0,size):
    GPIO.setup(Pins[x], GPIO.OUT)
    GPIO.output(Pins[x], 0)
#End Setup

#Debounce
input_value=GPIO.input(Ping)
#print(str(input_value))
sleep(0.1)
input_value=GPIO.input(Ping)
#print(str(input_value))
sleep(0.1)
input_value=GPIO.input(Ping)
#print(str(input_value))
sleep(0.1)

isKill=GPIO.input(Kill)

#Setup Game Screen

print("Setting up display")

pygame.init()

FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((1920,1080),pygame.RESIZABLE)

pygame.display.set_caption("GPIO Game")

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)


img1 = pygame.image.load("Brain 0-0.jpeg")
img2 = pygame.image.load("Brain 0-1.jpeg")
img3 = pygame.image.load("Brain 0-2.jpeg")
img4 = pygame.image.load("Brain 0-3.jpeg")
img5 = pygame.image.load("Brain 1-0.jpeg")
img6 = pygame.image.load("Brain 1-1.jpeg")
img7 = pygame.image.load("Brain 1-2.jpeg")
img8 = pygame.image.load("Brain 1-3.jpeg")
img9 = pygame.image.load("Brain 2-0.jpeg")
img10 = pygame.image.load("Brain 2-1.jpeg")
img11 = pygame.image.load("Brain 2-2.jpeg")
img12 = pygame.image.load("Brain 2-3.jpeg")
img13 = pygame.image.load("Brain 3-0.jpeg")
img14 = pygame.image.load("Brain 3-1.jpeg")
img15 = pygame.image.load("Brain 3-2.jpeg")
img16 = pygame.image.load("Brain 3-3.jpeg")

imgs=[img1,img2,img3,img4,img5,img6,img7,img8,img9,img10,img11,img12,img13,img14,img15,img16]


imgx = [0,480,960,1440]
imgy = [0,270,540,810]

for x in range(0,4):
    for y in range(0,4):
        print(str(x+4*y))
        DISPLAYSURF.blit(imgs[x+4*y],(imgx[x],imgy[y]))
        #DISPLAYSURF.blit(imgs[0],(imgx[x],imgy[y]))
pygame.display.flip()


#Begin Master Loop
while not (isKill):
    #Begin Game Loop (this breaks after win on reset)

    #Reset Game conditions
    for x in range(0,size):
        GPIO.output(Pins[x], 0)

    for x in range(0,4):
        GPIO.output(Nibble[x],0)

    #Signal
#    GPIO.output(Pong,1)

    #wait
#    ready = 0
#    print("Waiting")
#    while not ready:
#        ready = GPIO.input(Ping)
#        isKill= GPIO.input(Kill)
#        if ready:
#            GPIO.output(Pong,0)
#            break
#        if isKill:
#            break
        #print("no go")
    #End wait

    isKill=GPIO.input(Kill)
    isSoft=GPIO.input(SoftKill)

    #Begin Game
    print("Game start!")

    for event in pygame.event.get():
        if event.type == QUIT:
            print(str("end"))
            sleep(0.01)
            GPIO.cleanup()
            print("cleaned")
            pygame.quit()
            sys.exit()
    
    while not (isSoft or isKill):
        for x in range(0,size):
            GPIO.output(Pins[x],1)
            binary=bin(x)
            binary=binary[2:]

            #Make binary be 4 digits long
            big=len(binary)
            while big < 4:
                binary="0"+binary
                big=len(binary)
                if big == 4:
                    break
            #Set up nibble serial bus
            for b in range(0,big):
                GPIO.output(Nibble[b],int(binary[b]))

            #Pong Master, pin is ready
            sleep(0.01)
            GPIO.output(Pong,1)
            #wait for ping
            ready = 0
            while not ready:
                ready = GPIO.input(Ping)
                isSoft= GPIO.input(SoftKill)
                isKill= GPIO.input(Kill)
                if ready or isKill or isSoft:
                    GPIO.output(Pong,0)
                    break
            GPIO.output(Pins[x],0)

            isSoft=GPIO.input(SoftKill)
            isKill=GPIO.input(Kill)



            if KeyboardInterrupt:
                isKill=1
                break
            
            if isKill or isSoft or KeyboardInterrupt:
                break
            


        #End turn, go back to Pin[0]

    #End game condition, reset
    print("Restart Game")
            
#Kill code condition, HARD resest


print(str("end"))
GPIO.cleanup()
print("cleaned")
pygame.quit()
sys.exit()
