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
#	General init
print("Initialization Starting...")
t.sleep(0.5)
START = t.time()
track = object.track.__init__()
#	Motor init
pi = pigpio.pi()
esc = 15
pi.set_servo_pulsewidth(esc, 0) 
max_motor = 1500 #max motor speed
min_motor = 500  #min motor speed
mid_motor = 0    #mid motor speed

pi.set_servo_pulsewidth(esc, 0)
pi.set_servo_pulsewidth(esc, max_motor)
pi.set_servo_pulsewidth(esc, min_motor)
t.sleep(7)
print ("Motor Calibrating....")
t.sleep (5)
pi.set_servo_pulsewidth(esc, 0)
t.sleep(2)
print ("Arming ESC now...")
pi.set_servo_pulsewidth(esc, min_motor)
t.sleep(1)
print ("Motor Calibration Complete")

#	Servo init
print("Big Servo Calibrating...")
Bservo = 14 #GPIO: 14, Pin: 8
min_Bservo = 550  # 0.55 ms
max_Bservo = 2450  # 2.45 ms
mid_Bservo = 1550  # 1.55 ms
print("Big Servo Calibration Complete")

# Mini Servo init 
print("Mini Servo Calibrating...")
Mservo = 18 #GPIO: 18, Pin: 12
min_Mservo = 0  # 0 ms
max_Mservo = 0  # 0 ms
mid_Mservo = 0  # 0 ms
print("Mini Servo Calibration Complete")

# Depth init
print("Echolocation Calibrating...")
TRIG1 = 0  # Front
TRIG2 = 0  # Left
TRIG3 = 0  # Right
ECHO1 = 0  # Front
ECHO2 = 0  # Left
ECHO3 = 0  # Right
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
#-------------------------Functions-------------------------#

def detectObjs(track):
	Xdist  = depth(0)

	if Xdist > 200:
		Xdist -= 200
		num = 1
	elif Xdist > 150:
		Xdist -= 150
		num = 3
	elif Xdist > 100:
		Xdist -= 100
		num = 5
	else:
		print("ERROR NO OBJECTS AHEAD")
		num = -1
	
	distanceThresh = 0 # SET THIS
	if (Xdist > distanceThresh):
		go(Xdist - distanceThresh)
		Xdist = distanceThresh

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
		x, y, Cwidth, Cheight = cv.boudingRect(contour)
		if Cheight > height/5:
			if (x > width/2 and (x-Cwidth) > width/2):
				side = "left"
			elif x < width/2 

		
	
	#Finding red
	lower_red1 = np.array([0, 100, 100])
	upper_red1 = np.array([10, 255, 255])
	lower_red2 = np.array([170, 100, 100])
	upper_red2 = np.array([180, 255, 255])

	redmask1 = cv.inRange(img, lower_red1, upper_red1)
	redmask2 = cv.inRange(img, lower_red2, upper_red2)
	redMask = cv.bitwise_or(redmask1, redmask2)

	# Binary Thresh
	edges = cv.Canny(grayscale, 100, 200)
	contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


	for i in contours:
		MAX = -1
		MIN = 20000
		for j in i:
			if j<MIN:
				

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
		Bservo(mid_Bservo)
	else:
		pi.set_servo_pulsewidth(servo, pulse_width)

def Motor(speed):
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
	print("turned")

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

def shiftCar(distance, side) :
	return NotImplementedError

def go(distance):
	print("Not defined")

def center():
	Motor(0) # This is assuming Motor is set up
	while True:
		left = depth(1, 0)
		right = depth(2, 0)
		if right == left:
			return None
		elif right > left:
			if right < (left+2):
				return None
			else:
				dist = right-left
				shiftCar(dist, "right")
		else:
			if (right+2 > left):
				return None
			else:
				dist = left-right
				shiftCar(dist, "left")
				
def checkCorner():
	totalY = depth(1, 0) + depth(2, 0)
	if (totalY > 300):
		return True
	else:
		return False
		

#-------------------------Main Code-------------------------#

print("Code Begining now!")

# implement a button pressing thing 
end = False
turns = 0
corner = False
speed = 0

while turns == 4 and not end:
		if (checkCorner()):
			turn90()
			center()

		center()
		detectObjs(track)




