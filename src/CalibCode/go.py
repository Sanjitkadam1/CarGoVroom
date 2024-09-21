#-------------------------Packages--------------------------#
import time as t
import os
os.system ("sudo pigpiod")
print("importing packages...")
t.sleep(1)
import pigpio # type: ignore
import RPi.GPIO as PIN # type: ignore
import numpy as np # type: ignore
import cv2 as cv # type: ignore
from picamera2 import Picamera2 # type: ignore
print("Imported all nessesary packages")
import json 
import time 
import smbus # type: ignore

#	Motor init
pi = pigpio.pi()
esc = 15
pi.set_servo_pulsewidth(esc, 0) 

# Depth init
print("Echolocation Calibrating...")
TRIG1 = 17  # Front
TRIG2 = 22  # Left
TRIG3 = 24  # Right
ECHO1 = 27  # Front
ECHO2 = 23  # Left
ECHO3 = 25  # Right
PIN.setmode(PIN.BCM)
PIN.setup(TRIG1, PIN.OUT)
PIN.output(TRIG1, PIN.LOW)
PIN.setup(ECHO1, PIN.IN)
PIN.setup(TRIG2, PIN.OUT)
PIN.output(TRIG2, PIN.LOW)
PIN.setup(ECHO2, PIN.IN)
PIN.setup(TRIG3, PIN.OUT)
PIN.output(TRIG3, PIN.LOW)
PIN.setup(ECHO3, PIN.IN)
print("Echolocation Calibration Complete")

def depth(num):
	#This code is for the Echo Sensors
	if num == 0: #Front
		TRIG = 17 #GPIO: 17, Pin 11
		ECHO = 27 #GPIO: 27, Pin 13
	if num == 1: #Left 
		TRIG = 24 #GPIO: 22, Pin 15
		ECHO = 25 #GPIO: 23, Pin 16
	if num == 2: #Right
		TRIG = 22 #GPIO: 24, Pin 18
		ECHO = 23 #GPIO: 25, Pin 22

	PIN.output(TRIG, PIN.HIGH)
	t.sleep(0.00001)   # Creating a 10uS (microsecond) pulse
	PIN.output(TRIG, PIN.LOW)
    
	while PIN.input(ECHO)==0:
		pulse_start = t.time()
	
	while PIN.input(ECHO)==1:
		pulse_end = t.time()
		
	rawDist = pulse_end - pulse_start

	#Implement speed divider
	cmDist = rawDist * 34600/2 
  #34600 cm/s is the speed of sound in room temprature air. speed * time = distance. divided by 2 bcz its a round trip
	cmDist = round(cmDist, 2)
	return cmDist

def go(distance):
		esc = 20
		# goes ahead roughly 12 cm at 1600 for 0.25sec goes behind roughly 7.25 cm at 1300 for 0.25sec
		initd = depth(0)
		error = 2
		pi.set_servo_pulsewidth(esc, 1500)
		if (distance>12):
			atPoint = False
			while not atPoint:
				pi.set_servo_pulsewidth(esc, 1600)
				time.sleep(0.2)
				pi.set_servo_pulsewidth(esc, 0)
				check = depth(0)
				if (initd-check)<error and (initd-check)>-error:
					atPoint = True
while True:
	print("How far ahead do you want to go?")
	dist = input()
	go(dist)