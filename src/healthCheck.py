#-------------------------Packages--------------------------#
import time as t
import os
os.system ("sudo pigpiod")
print("importing packages...")
t.sleep(1)
import pigpio
import RPi.GPIO as PIN # type: ignore
import numpy as np # type: ignore
import cv2 as cv # type: ignore
from picamera2 import Picamera2 # type: ignore
print("Imported all nessesary packages")

#-------------------------Init Code-------------------------#

# Depth init
print("Echolocation Calibrating...")
# if num == 0: #Front
# 		TRIG = 17 #GPIO: 17, Pin 11
# 		ECHO = 27 #GPIO: 27, Pin 13
# 	if num == 1: #Left 
# 		TRIG = 22 #GPIO: 22, Pin 15
# 		ECHO = 23 #GPIO: 23, Pin 16
# 	if num == 2: #Right
# 		TRIG = 24 #GPIO: 24, Pin 18
# 		ECHO = 25 #GPIO: 25, Pin 22
TRIG1 = 17  # Front
TRIG2 = 22  # Left
TRIG3 = 24  # Right
ECHO1 = 27  # Front
ECHO2 = 23  # Left
ECHO3 = 25  # Right
# set values in the depth function
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

#-------------------------Functions-------------------------#
def depth(num):
	#This code is for the Echo Sensors
	
	if num == 0: #Front
		TRIG = 17 #GPIO: 17, Pin 11
		ECHO = 27 #GPIO: 27, Pin 13
	if num == 1: #Left 
		TRIG = 22 #GPIO: 22, Pin 15
		ECHO = 23 #GPIO: 23, Pin 16
	if num == 2: #Right
		TRIG = 24 #GPIO: 24, Pin 18
		ECHO = 25 #GPIO: 25, Pin 22

	PIN.output(2, PIN.HIGH)
	t.sleep(0.00001)   # Creating a 10uS (microsecond) pulse
	PIN.output(2, PIN.LOW)
    
	while PIN.input(3)==0:
		pulse_start = t.time()
	
	while PIN.input(3)==1:
		pulse_end = t.time()
		
	rawDist = pulse_end - pulse_start

	#Implement speed divider
	cmDist = rawDist * 34600/2 
  #34600 cm/s is the speed of sound in room temprature air. speed * time = distance. divided by 2 bcz its a round trip
	cmDist = round(cmDist, 2)
	return cmDist

#-------------------------Checking code-------------------------#

inp = input()
while inp != "stop":
	print("Select what to check")
	print("gyro - Accel and gyro / depth - Depth sensors / stop - end the program")
	inp = input()
	if inp == "depth":
		center = depth(0)
		right = depth(2)
		left = depth(1)
		print(f"center = {center}")
		print(f"left = {left}")
		print(f"right = {right}")
	else :
		print("put that shit again")