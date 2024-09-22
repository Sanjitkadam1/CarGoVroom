#-----------------------Package import-----------------------#
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
import json 
import time 
import smbus # type: ignore
import math
print("Imported all nessesary packages")
#------------------------Innit Code-------------------------#
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

#	Servo init
print("Servo Calibrating...")
Bservo = 14 #GPIO: 14, Pin: 8
min_Bservo = 550  # 0.55 ms
max_Bservo = 2450  # 2.45 ms
mid_Bservo = 1550  # 1.55 ms
print("Servo Calibration Complete")

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

# Function to conver Degress into PWM
def Deg2PWM(x):
    if x > 40 or x < -40:
        return Exception
    return (6.5*x) + 1550

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

#-------------------------Main Code-------------------------#

def calcAng():
	backnum = 5 #the amount you backtrack, subject to change
	#we need to figure out which direction it is turned to
	turned = ""
	left = depth(1) #taking left and right values
	right = depth(2)
	goStraight(-backnum) #Need to implement #moving backwards a small amount
	left1 = depth(1) #taking left and right values again
	right1 = depth(2)
	if left1>left:
		turned = "l" #If the left measurement gets LARGER when the car goes backwards, then it is facing the left
		print("adjusting...")
	elif left1<left:
		turned = "r" #If the left measurement gets SMALLER when the car goes backwards, then it is facing the right 
		print("adjusting...")
	elif left1==left:
		turned = "0" #If the left measurement stays the SAME when the car goes backwards, then it is straight
		print("youre straighter than Pranav rn")
		Deg2PWM(0)
		goStraight(backnum)
		return "you're straighter than Pranav"
	else:
		return "error: calcAng No worky" #Failsafe if none of them work, mainly for debugging
        
	total = left1 + right1 + 16 #adding the left and right depth sensor values with the length of the car
	B = math.acos(total/100) #dividing that number with the width of the field track (100mm) and then arcos-ing the value to get the angle
	b = math.degrees(B) #turning radians to degrees
	ang = 90 - b #subtracting that angle to find the angle(ang) of with the car is off by
	if(turned == "l"):
		print("adjust left")
		Deg2PWM(-ang) #if its left then its a negative angle(?)
		goStraight(backnum) #go forward the amount we leave
		Deg2PWM(0)
		print("checking...")
		calcAng()
	elif(turned == "r"):
		print("adjust right")
		Deg2PWM(ang)
		goStraight(backnum)
		Deg2PWM(0)
		print("checking...")
		calcAng()


