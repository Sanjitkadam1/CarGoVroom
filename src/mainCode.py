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
import json 
import matplotlib.pyplot as plt
import time 
import smbus # type: ignore


#-------------------------Init Code-------------------------#
#	General init
print("Initialization Starting...")
t.sleep(0.5)
START = t.time()
track = object.track()

#	Motor init
pi = pigpio.pi()
esc = 15
pi.set_servo_pulsewidth(esc, 0)

#	Servo init
print("Servo Calibrating...")
Bservo = 14 #GPIO: 14, Pin: 8
min_Bservo = 550  # 0.55 ms
max_Bservo = 2450  # 2.45 ms
mid_Bservo = 1550  # 1.55 ms
print("Servo Calibration Complete")

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

# Camera init
print("Camera Calibrating...")
picam = Picamera2()
config = picam.create_still_configuration()
picam.configure(config)
picam.start()
t.sleep(2)
print("Camera Calibration Complete")

# Gyroscope init 
sm = smbus.SMBus(1)
gyroCalibX = 0
gyroCalibY = 0
gyroCalibZ = 0
accelCalibX = 0
accelCalibY = 0
accelCalibZ = 0
sm.write_byte_data(0x68, 0x6B, 0x00)
sm.write_byte_data(0x68, 0x1A, 0x06)
sm.write_byte_data(0x68, 0x1B, 0x70)
sm.write_byte_data(0x68, 0x1C, 0x1F)

print("Initialization Complete")
t.sleep(1)
#-------------------------Functions-------------------------#

def detectObjs(track, turn):
	Xdist = depth(0)
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
	
	distanceThresh = 20 # SET THIS
	if (Xdist > distanceThresh):
		go(Xdist - distanceThresh)
		Xdist = distanceThresh
	elif (Xdist < distanceThresh):
		go(-(distanceThresh - Xdist))

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

def Bservo(pulse_width):
	servo = 14 #GPIO: 14, Pin: 8
	#This code moves the servo, You can either input the premade degrees, res to reset, or just some pulse_width if needed
	if (pulse_width == "10l"):
		pi.set_servo_pulsewidth(1615) #added 65
	elif (pulse_width == "10r"):
		pi.set_servo_pulsewidth(1485) #subtracted 65
	elif (pulse_width == "20l"):
		pi.set_servo_pulsewidth(1680) #added 130
	elif (pulse_width == "20r"):
		pi.set_servo_pulsewidth(1420) #subtracted 130
	elif (pulse_width == "30l"):
		pi.set_servo_pulsewidth(1745) #added 195
	elif (pulse_width == "30r"):
		pi.set_servo_pulsewidth(1355) #subtracted 195
	elif (pulse_width == "40l"):
		pi.set_servo_pulsewidth(1810) #added 260
	elif (pulse_width == "40r"):
		pi.set_servo_pulsewidth(1290) #subtracted 260
	elif (pulse_width == "res"):
		pi.set_servo_pulsewidth(num)
	else:
		pi.set_servo_pulsewidth(servo, pulse_width)

def turn90(side):
	turnRadius = 0
	PI = 22/7
	Bservo(40)
	goTo(0.5*PI*turnRadius) # change this later when you know the turn radius

def gyroVals(): 
	rawDataX = sm.read_i2c_block_data(0x68, 0x43, 2)
	rawDataY = sm.read_i2c_block_data(0x68, 0x45, 2)
	rawDataZ = sm.read_i2c_block_data(0x68, 0x47, 2)
	
	rawX = (rawDataX[0] << 8) | rawDataX[1]
	rawY = (rawDataY[0] << 8) | rawDataY[1]
	rawZ = (rawDataZ[0] << 8) | rawDataZ[1]

	# 16 bit negative
	if rawX > 32767:
		rawX -= 65536
	if rawY > 32767:
		rawY -= 65536
	if rawZ > 32767:
		rawZ -= 65536

	gyroX = rawX-gyroCalibX
	gyroZ = rawZ-gyroCalibZ
	gyroY = rawY-gyroCalibY
		
	
	return gyroX, gyroY, gyroZ
	
def accelVals (): 
	rawDataX = sm.read_i2c_block_data(0x68, 0x3B, 2)
	rawDataY = sm.read_i2c_block_data(0x68, 0x3D, 2)
	rawDataZ = sm.read_i2c_block_data(0x68, 0x3F, 2)

	rawX = (rawDataX[0] << 8) | rawDataX[1]
	rawY = (rawDataY[0] << 8) | rawDataY[1]
	rawZ = (rawDataZ[0] << 8) | rawDataZ[1]

	# 16 bit negative
	if rawX > 32767:
		rawX -= 65536
	if rawY > 32767:
		rawY -= 65536
	if rawZ > 32767:
		rawZ -= 65536

	accelX = rawX-accelCalibX
	accelY = rawY-accelCalibY
	accelZ = rawZ-accelCalibZ



	return accelX, accelY, accelZ

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
	PIN.output(TRIG, PIN.LOW)

	PIN.output(TRIG, PIN.HIGH)
	t.sleep(0.00001)   # Creating a 10uS (microsecond) pulse
	PIN.output(TRIG, PIN.LOW)
	fail = t.time()
	failed = False
	while PIN.input(ECHO)==0 and not failed:
		pulse_start = t.time()
		failed = (fail-pulse_start)>2
	
	while PIN.input(ECHO)==1:
		pulse_end = t.time()
	
	if failed:
		return depth(num)

	rawDist = pulse_end - pulse_start

	#Implement speed divider
	cmDist = rawDist * 34600/2 
  #34600 cm/s is the speed of sound in room temprature air. speed * time = distance. divided by 2 bcz its a round trip
	cmDist = round(cmDist, 2)
	return cmDist

# Needs to be completed
def shiftCar(distance):
	turnRad = 0
	angle = np.arccos(1 - distance/2*turnRad)
	PI = 22/7
	dist = (angle/360) * 2 * PI * turnRad
	Bservo(30)

	


def goStraight(distance):
		esc = 20
		# goes ahead roughly 12 cm at 1600 for 0.25sec goes behind roughly 7.25 cm at 1300 for 0.25sec
		initd = depth(0)
		error = 2
		if (distance>0):
			pi.set_servo_pulsewidth(esc, 1500)
			time.sleep(0.001)
			i = distance/12
			rem = distance%12
			for q in range(0, i):
				pi.set_servo_pulsewidth(esc, 1600)
				time.sleep(0.25)
				pi.set_servo_pulsewidth(esc, 0)
				time.sleep(0.1)
			pi.set_servo_pulsewidth(esc, 1600)
			time.sleep((rem/12)*0.25)
			pi.set_servo_pulsewidth(0)
			finald = depth(0)
			offby = finald - initd
			if ((distance - offby.__abs__).__abs__ > error):
				goStraight(offby)
		else:
			pi.set_servo_pulsewidth(esc, 1500)
			time.sleep(0.001)
			pi.set_servo_pulsewidth(esc, 1300)
			time.sleep(0.001)
			pi.set_servo_pulsewidth(esc, 1500)
			i = distance/7.25
			rem = distance%7.25
			for q in range(0, i):
				pi.set_servo_pulsewidth(esc, 1300)
				time.sleep(0.25)
				pi.set_servo_pulsewidth(esc, 0)
				time.sleep(0.1)
			pi.set_servo_pulsewidth(esc, 1300)
			time.sleep((rem/12)*0.25)
			pi.set_servo_pulsewidth(0)
			finald = depth(0)
			offby = finald - initd
			if ((distance - offby.__abs__).__abs__ > 2):
				goStraight(offby)

def center():
	error = 3
	while True:
		left = depth(1, 0)
		right = depth(2, 0)
		error = 2
		left = depth(1)
		right = depth(2)
		if right == left:
			return None
		elif right > left:
			if right < (left+error):
				return None
			else:
				dist = right-left
				shiftCar(dist/2, "right", 30)
		else:
			if (right+error > left):
				return None
			else:
				dist = left-right
				shiftCar(dist/2, "left", 30)
				
def checkCorner():
	right = depth(2)
	left = depth(2)	
	totalY = depth(1) + depth(2)
	if (totalY > 300):
		if left>right:
			return True, "left"
		else:
			return True, "right"
	else:
		return False, "none"
		
def avoidObj(track, turns, num): 
	right, left = track.getObjs(turns, num)
	dists = [200, 150, 100]
	Xdist = depth(0)
	distObj = Xdist - dists[((num+1)/2)-1]
	if (right == "green"):
		go(distObj)
	elif (right == "red"):
		if (left == "green"):
			print("ERROR DUPLICATE OBJECT DETECTED OR BINARY ERROR")
		else:
			shiftCar(25, "right", 50)
			# add go if needed
	else:
		if (left == "red"):
			go(distObj)
		else:
			shiftCar(25, "left", 50)
			# add go if needed

#-------------------------Main Code-------------------------#

print("Code begining now! Keep the car still")

for i in range(2000):
	sampleX, sampleY, sampleZ = gyroVals()
	gyroCalibX += sampleX
	gyroCalibY += sampleY
	gyroCalibZ += sampleZ

gyroCalibX/=2000
gyroCalibY/=2000
gyroCalibZ/=2000

# gyroCalibX = round(gyroCalibX)
# gyroCalibY = round(gyroCalibY)
# gyroCalibZ = round(gyroCalibZ)
		
# print(f"Gyro Calibration Values: X={gyroCalibX}, Y={gyroCalibY}, Z={gyroCalibZ}")

# for i in range(2000):
# 	sampleX, sampleY, sampleZ = accelVals()
# 	accelCalibX += sampleX
# 	accelCalibY += sampleY
# 	accelCalibZ += sampleZ

# accelCalibX/=2000
# accelCalibY/=2000
# accelCalibZ/=2000

# accelCalibX = round(accelCalibX)
# accelCalibY = round(accelCalibY)
# accelCalibZ = round(accelCalibZ)

# print(f"Accel Calibration Values: X={accelCalibX}, Y={accelCalibY}, Z={accelCalibZ}")


# implement a button pressing thing 

for i in range(0, 2):
	turns = 0

	center()
	firstNum = detectObjs(track, turns)
	avoidObj(track, turns, firstNum)

	while turns < 4:
			corner, side = checkCorner()
			center()
			if (corner):
				turn90(side)
				turns+=1
				center()
			num = detectObjs(track, turns)
			avoidObj(track, turns, num)

	turn = 0

	if (firstNum == 3):
		center()
		num = detectObjs(track, turns)
		avoidObj(track, turns, num)
		END  = t.time()
		timeTaken = START - END
		print("Should have ended now.")
		print(f"Path found in - {timeTaken} seconds")
	else:
		for i in range(2):
			center()
			num = detectObjs(track, turns)
			avoidObj(track, turns, num)
		print("Should have ended now.")
		END  = t.time()
		timeTaken = START - END
		print("Should have ended now.")
		print(f"Path found in - {timeTaken} seconds")

	# json_track = track.to_json()

	# print(f"TRACK DETAILS IN JSON. {json_track}")

	greenX, greenY, redX, redY = track.plot()

	plt.scatter(greenX, greenY, c='green')
	plt.scatter(redX, redY, c='red')

	plt.title("Objects placed on the map")
	plt.xlabel("X")
	plt.ylabel("Y")

	# plt.imshow()
	# sm.close()