import pygame, sys
from time import sleep
import RPi.GPIO as GPIO

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

#Begin Master Loop
while not (isKill):
    #Begin Game Loop (this breaks after win on reset)

    #Reset Game conditions
    for x in range(0,size):
        GPIO.output(Pins[x], 0)

    for x in range(0,4):
        GPIO.output(Nibble[x],0)

    #Signal
    GPIO.output(Pong,1)

    #wait
    ready = 0
    print("Waiting")
    while not ready:
        ready = GPIO.input(Ping)
        isKill= GPIO.input(Kill)
        if ready:
            GPIO.output(Pong,0)
            break
        if isKill:
            break
        #print("no go")
    #End wait

    isKill=GPIO.input(Kill)
    isSoft=GPIO.input(SoftKill)

    #Begin Game
    print("Game start!")
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
            GPIO.output(Pong,1)
            sleep(0.01)
            #wait for ping
            ready = 0
            while not ready:
                ready = GPIO.input(Ping)
                isSoft= GPIO.input(SoftKill)
                isKill= GPIO.input(Kill)
                if ready or isKill or isSoft:
                    break
            GPIO.output(Pong,0)
            GPIO.output(Pins[x],0)

            isSoft=GPIO.input(SoftKill)
            isKill=GPIO.input(Kill)
            
            if isKill or isSoft:
                break
            


        #End turn, go back to Pin[0]

    #End game condition, reset
    print("Restart Game")
            
#Kill code condition, HARD resest


print(str("end"))
GPIO.cleanup()
print("cleaned")
