#-------------------------Packages--------------------------#

import time as t
import os
os.system ("sudo pigpiod")
print("importing packages...")
t.sleep(1)
import pigpio
import RPi.GPIO # type: ignore
import numpy as np
import cv2 as cv
from picamera2 import Picamera2 # type: ignore

#-------------------------Init Code-------------------------#
#	General init
ending = False
START = t.t()

#	Motor init
pi = pigpio.pi()
esc = 14
pi.set_servo_pulsewidth(esc, 0) 
max_motor = 1500 #max motor speed
min_motor = 500

#	Servo init
servo = 15
min_servo = 550  # 1 ms
max_servo = 2450  # 2 ms
mid_servo = 1550  # 1.55 ms

def set_servo_position(pulse_width):
    pi.set_servo_pulsewidth(servo, pulse_width)






while not ending:
	
    # Implement for frame 
	
	X, color = detectColor(img) # type: ignore
	if X != None:
		if (color == "red") and X :
			


def detectColor(img): # type: ignore
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

def turn():
	# Need to implement
	return NotImplementedError

def setSpeed(): # type: ignore

	print()