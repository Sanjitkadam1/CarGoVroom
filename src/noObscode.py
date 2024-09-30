#-------------------------Packages--------------------------#
import time as t
import os
os.system ("sudo pigpiod")
print("importing packages...")
t.sleep(1)
import pigpio # type: ignore
import pigpio # type: ignore
import RPi.GPIO as PIN # type: ignore
import numpy as np # type: ignore
import cv2 as cv # type: ignore
from picamera2 import Picamera2 # type: ignore
import matplotlib.pyplot as plt # type: ignore
import matplotlib.pyplot as plt # type: ignore
import time 
import smbus # type: ignore
import math
print("Imported all nessesary packages")

#-------------------------Init Code-------------------------#
#	General init
print("Initialization Starting...")
t.sleep(0.5)
START = t.time()
track = object.track()

#	Motor init
pi = pigpio.pi()
esc = 18
pi.set_servo_pulsewidth(esc, 0)

#	Servo init
print("Servo Calibrating...")
Bservo = 14 #GPIO: 14, Pin: 8
print("Servo Calibration Complete")

# Camera init
print("Camera Calibrating...")
picam = Picamera2()
config = picam.create_still_configuration()
picam.configure(config)
picam.start()
t.sleep(2)
print("Camera Calibration Complete")

print("Initialization Complete")
t.sleep(1)


def detectObjs(track, turn):
	picam.capture_file("test.jpeg")
	img = cv.imread("test.jpeg")
	height, width, channels = img.shape
	hsvimg = cv.cvtColor(img, cv.COLOR_BGR2HSV)

	#Finding green 
	greenLow = np.array([51, 100, 100])
	greenHigh = np.array([61, 255, 255])
	greenMask = cv.inRange(hsvimg, greenLow, greenHigh)

	greenContours, greenHierarchy = cv.findContours(greenMask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	side = None
	for contour in greenContours:
		MAX = -1
		x, y, Cwidth, Cheight = cv.boudingRect(contour)
		if Cheight > height/10 and (Cwidth*Cheight) > MAX and Cwidth > width/10:
			MAX = Cheight*Cwidth
			if (MAX > minArea):
				if (x > width/2 and (x-Cwidth) > width/2):
					side = "left"
				elif x < width/2: 
					side = "right"

	if (side == "left"):
		objGreen = object.obj(turn, num, "green")
		track.add(objGreen)
	elif (side == "right"):
		objGreen = object.obj(turn, num+1, "green")
		track.add(objGreen)

	#Finding red
	lower_red1 = np.array([0, 100, 100])
	upper_red1 = np.array([10, 255, 255])
	lower_red2 = np.array([170, 100, 100])
	upper_red2 = np.array([180, 255, 255])

	redmask1 = cv.inRange(img, lower_red1, upper_red1)
	redmask2 = cv.inRange(img, lower_red2, upper_red2)
	redMask = cv.bitwise_or(redmask1, redmask2)

	redContours, redHierarchy = cv.findContours(redMask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	side = None
	for contour in redContours:
		MAX = -1
		x, y, Cwidth, Cheight = cv.boudingRect(contour)
		if Cheight > height/10 and (Cwidth*Cheight) > MAX and Cwidth > width/10:
			MAX = Cheight*Cwidth
			minArea = 0 # !!!! SET THIS V. IMP
			if (MAX > minArea):
				if (x > width/2 and (x-Cwidth) > width/2):
					side = "left"
				elif x < width/2: 
					side = "right"
	
	if (objGreen.turn == "left" and not side == None):
		print("ERROR DUPLICATE OBJECT DETECTED OR BINARY ERROR")

	if (side == "left"):
		objRed = object.obj.__init__(turn, num, "red")
		track.add(objRed)
	elif (side == "right"):
		if (objGreen.turn == "right"):
			print("ERROR DUPLICATE OBJECT DETECTED")
		objRed = object.obj.__init__(turn, num+1, "red")
		track.add(objRed)

	return turn, num

#Starting at Starting position
Start
startingPos = postion()
rounds = 3
turns = 0
Carwidth = 190 #Settable value

while rounds != 1:
	goto(3000,startingPos[1])
	pos = postion()
	Bservo(30)
	pi.set_servo_pulsewidth(servo,1600)
	time.sleep(2)
	pi.set_servo_pulsewidth(servo,1500)
	turns = turns + 1
	if turns == 4:
		turns = 0
		rounds = rounds + 1
goto(startingPos)