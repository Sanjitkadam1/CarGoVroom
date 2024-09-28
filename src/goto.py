import time as t
import os
os.system ("sudo pigpiod")
print("importing packages...")
t.sleep(1)
import pigpio # type: ignore
import RPi.GPIO as PIN # type: ignore
import numpy as np 
import cv2 as cv # type: ignore
from picamera2 import Picamera2 # type: ignore
import json 
import smbus # type: ignore
import matplotlib.pyplot as plt
import math
print("Imported all nessesary packages")

fig, ax = plt.subplots()
innerbox = ([1000,2000,2000,1000,1000],[1000,1000,2000,2000,1000])
ax.plot(innerbox, label = "innerbox", color = 'black')
outerbox = ([0,3000,3000,0,0],[0,0,3000,3000,0])
ax.plot(outerbox, label = "outerbox", color = 'black')

def checkPos(A, B):
    tolerance = 5 # set this 
    checkx =  np.abs(A[0] - B[0]) <= tolerance
    checky =  np.abs(A[1] - B[1]) <= tolerance
    return checkx and checky

def stop():
    esc = 18
    pi.set_servo_pulsewidth(esc, 1500)
    t.sleep(0.01)
    pi.set_servo_pulsewidth(esc, 1300)
    t.sleep(0.01)
    pi.set_servo_pulsewidth(esc, 1500)
    t.sleep(0.01)
    pi.set_servo_pulsewidth(esc, 1300)
    t.sleep(0.01)
    pi.set_servo_pulsewidth(esc, 1500)

#A and B are positions
def goto(A, B):
    esc = 18
    angL = math.atan((B[1] - A[1])/(B[0] - A[0])) #gets the angle of the line
    ang = getAngle() #gets the cars angle
    Bservo(angL - ang) #changes the wheel angle to the difference between angL and ang
    while not checkPos(postion(), B): #while we arent at B yet, 
        pi.set_servo_pulsewidth(esc, 1570) #motor starts moving car
        ang = getAngle() #gets cars angle
        Bservo(angL - ang) #changes the wheel angle to the difference between angL and ang
    stop()
    if(position() != B):
        goto(position(),B) #if we arent at B yet it will recursively call the function again
    else:
        return "reached", B #if not then we end the function
    
pi = pigpio.pi()
esc = 18
pi.set_servo_pulsewidth(esc, 0)
print("say yes")
inp = input()
if inp.equals("no"):
    exit()
else:
    pi.set_servo_pulsewidth(esc, 1500)
    pi.set_servo_pulsewidth(esc, 1600)
    t.sleep(1)

stop()