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

#-------------------------Init Code-------------------------#
#	General init
START = t.time()

#	Motor init
pi = pigpio.pi()
esc = 15
pi.set_servo_pulsewidth(esc, 0) 
max_motor = 1500 #max motor speed
min_motor = 500

#	Servo init
servo = 14 # set servo pin
min_servo = 550  # 0.55 ms
max_servo = 2450  # 2.45 ms
mid_servo = 1550  # 1.55 ms

# Mini Servo init 
# NotImplementedError

#   Depth init
TRIG1 = 0  # Front
TRIG2 = 0  # Left
TRIG3 = 0  # Right
ECHO1 = 0
ECHO2 = 0
ECHO3 = 0
# set values in the depth function
# raise NotImplementedError
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

# Camera init
#needs to be added
#-------------------------Functions-------------------------#
def detectColor(img): # type: ignore
	#This code is how we are going to detect colors. We set a threshold for each color we need to detect, Red, Green, Pink, and Gray. And can create a mask for it. 

	# ASSIGN THRESHOLD
	thresh = 20
	hsvimg = cv.cvtColor(img, cv.COLOR_BGR2HSV)

	#Finding green 
	greenLow = np.array([51, 100, 100])
	greenHigh = np.array([61, 255, 255])

	greenMask = cv.inRange(hsvimg, greenLow, greenHigh)
	greenper = np.count_nonzero(greenMask)
	
	#Finding red
	lower_red1 = np.array([0, 100, 100])
	upper_red1 = np.array([10, 255, 255])
	lower_red2 = np.array([170, 100, 100])
	upper_red2 = np.array([180, 255, 255])

	redmask1 = cv.inRange(img, lower_red1, upper_red1)
	redmask2 = cv.inRange(img, lower_red2, upper_red2)
	redMask = cv.bitwise_or(redmask1, redmask2)
	redper = np.count_nonzero(redMask)

	if (redper > thresh):
		smallestX, smallestY = 100000000, 100000000
		greatestX, greatestY = -1, -1
		
        # Run a denoising algorithm 
		
		print("Red object detected")
		
		for x in range(redMask.shape[0]):
			for y in range(redMask.shape[1]):
				if redMask[x, y] == 255:
					if x <= smallestX and y <= smallestY and redMask[x+5, y+5] == 255:
						smallestX = x
						smallestY = y
					elif x >= greatestX and y >= greatestY and redMask[x-5, y-5] == 255:
						greatestX = x
						greatestY = y
		
		midX = (greatestX + smallestX)/2
		return midX, "red"
	
	if (greenper > thresh):
		smallestX, smallestY = 100000000, 100000000
		greatestX, greatestY = -1, -1
		
        # Run a denoising algorithm 
		
		print("Red object detected")
		
		for x in range(redMask.shape[0]):
			for y in range(redMask.shape[1]):
				if redMask[x, y] == 255:
					if x <= smallestX and y <= smallestY and redMask[x+5, y+5] == 255:
						smallestX = x
						smallestY = y
					elif x >= greatestX and y >= greatestY and redMask[x-5, y-5] == 255:
						greatestX = x
						greatestY = y
		
		midX = (greatestX + smallestX)/2
		return midX, "green"
	
	return None

def Bservo(pulse_width):
	servo = 14 #GPIO: 14, Pin: 8
	#This code moves the servo, You can either input the premade degrees, res to reset, or just some pulse_width if needed
	if (pulse_width == "10"):
		Bservo(1650)
	elif (pulse_width == "20"):
		Bservo(1720)
	elif (pulse_width == "30"):
		Bservo(1800)
	elif (pulse_width == "45"):
		Bservo(1925)
	elif (pulse_width == "res"):
		Bservo(mid_servo)
	else:
		pi.set_servo_pulsewidth(servo, pulse_width)

def Motor():
	esc = 15
	pi.set_servo_pulsewidth(esc, 0) 
	# Needs more testing to determine values

def turn90():
	# NEEDS SEVERE TUNING
	# Motor speed reduces to 40%
	# needs to be implemented 
	# servo starts slowly turning to 45 degrees
	Bservo("10")
	t.sleep(1)
	Bservo("20")
	t.sleep(1)
	Bservo("30")
	t.sleep(1)
	Bservo("45")
	t.sleep(2)
	Bservo("res")
	return("turned")

def setSpeed(): # type: ignore

	print()



def depth(num, speed):
	#This code is for the Echo Sensors
	
	if num == 0: #Front
		TRIG = 0 #GPIO: 17, Pin 11
		ECHO = 0 #GPIO: 27, Pin 13
	if num == 1: #Left 
		TRIG = 0 #GPIO: 22, Pin 15
		ECHO = 0 #GPIO: 23, Pin 16
	if num == 2: #Right
		TRIG = 0 #GPIO: 24, Pin 18
		ECHO = 0 #GPIO: 25, Pin 22

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

#-------------------------Main Code-------------------------#

LeftYstart = depth(1, 0)
RightYstart = depth(2, 0)