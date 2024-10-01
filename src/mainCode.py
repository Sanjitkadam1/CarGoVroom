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
#-------------------------Functions-------------------------#

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


def Bservo(x): #function to turn the servo
	servo = 14 #GPIO: 14, Pin: 8 
	if x > 40 or x < -40: #our wheels cant turn more than 40 degrees both ways.
		return Exception
	pulse_width = (6.5*x) + 1550 #equation we have made for pulsewidth conversion. y(pulsewidth) = 6.5(amount changing per degree)*x(degrees) + 1550(center)
	pi.set_servo_pulsewidth(servo, pulse_width)
	

# needs to made
def turn90(side):
	turnRadius = 0
	PI = 22/7
	Bservo(40)
	go(0.5*PI*turnRadius) # change this later when you know the turn radius


# works
def gyroVals(): 
	rawDataX = sm.read_i2c_block_data(0x68, 0x43, 2) #reads the data from X, Y, and Z channels of the gyro
	rawDataY = sm.read_i2c_block_data(0x68, 0x45, 2)
	rawDataZ = sm.read_i2c_block_data(0x68, 0x47, 2)
	
	rawX = (rawDataX[0] << 8) | rawDataX[1] #ask sol
	rawY = (rawDataY[0] << 8) | rawDataY[1]
	rawZ = (rawDataZ[0] << 8) | rawDataZ[1]

	# 16 bit negative (?)
	if rawX > 32767:
		rawX -= 65536
	if rawY > 32767:
		rawY -= 65536
	if rawZ > 32767:
		rawZ -= 65536

	gyroX = rawX-gyroCalibX #returning values
	gyroZ = rawZ-gyroCalibZ
	gyroY = rawY-gyroCalibY
		
	
	return gyroX, gyroY, gyroZ

# works
def accelVals (): 
	rawDataX = sm.read_i2c_block_data(0x68, 0x3B, 2) #reads the data from X, Y, and Z channels of the Accelerometer
	rawDataY = sm.read_i2c_block_data(0x68, 0x3D, 2)
	rawDataZ = sm.read_i2c_block_data(0x68, 0x3F, 2)

	rawX = (rawDataX[0] << 8) | rawDataX[1] #ask sol
	rawY = (rawDataY[0] << 8) | rawDataY[1]
	rawZ = (rawDataZ[0] << 8) | rawDataZ[1]

	# 16 bit negative 
	if rawX > 32767:
		rawX -= 65536
	if rawY > 32767:
		rawY -= 65536
	if rawZ > 32767:
		rawZ -= 65536

	accelX = rawX-accelCalibX #returning values
	accelY = rawY-accelCalibY
	accelZ = rawZ-accelCalibZ



	return accelX, accelY, accelZ

# Get from the pi
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

# Needs to be made
def go(distance):
	print("Sol you dipshit do this")

# Needs to be made
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

# works?
def checkCorner():
	right = depth(2)
	left = depth(1)	
	totalY = left + right
	if (totalY > 300):
		if left>right:
			return True, "left"
		else:
			return True, "right"
	else:
		return False, "none"

def avoidObj(track, turns, num):  #needs testing (and probably redoing with new sensors)
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


# implement a button pressing thing 

for i in range(0, 2): #code for the first two rounds, obstacle section only(?)
	turns = 0
	firstNum = detectObjs(track, turns)
	avoidObj(track, turns, firstNum)

	while turns < 4: #keeps count of the amount of turns
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