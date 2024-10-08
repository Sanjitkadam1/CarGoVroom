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

#-------------------------Checking code-------------------------#

inp = input()
while inp != "stop":
	print("Select what to check")
	print("gyro - Accel and gyro / depth - Depth sensors / stop - end the program")
	inp = input()
	if inp == "depth":
		print("If the program is taking too long to get depth that sensors echo is not set up properly.")
		center = depth(0)
		print(f"center = {center}")
		right = depth(2)
		print(f"right = {right}")
		left = depth(1)
		print(f"left = {left}")

	else :
		print("put that shit again")