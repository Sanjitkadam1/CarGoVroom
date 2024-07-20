#-------------------------Packages--------------------------#
import time as t
import os
os.system ("sudo pigpiod")
print("importing packages...")
t.sleep(1)
import pigpio
import RPi.GPIO as PIN # type: ignore
import numpy as np # type: ignore
import argparse
import json
print("Imported all nessesary packages")
import matplotlib.pyplot as plt
#-------------------------Init Code-------------------------#
#	General init
print("Initialization Starting...")
parse = argparse.ArgumentParser(description="speed")
parse.add_argument('inputTrack', type=json.loads, help="Input your track object in JSON format for the first param")
args = parse.parse_args()
track = args.inputTrack
track = object.track.from_json()
START = t.time()

#	Motor init
pi = pigpio.pi()
esc = 15
pi.set_servo_pulsewidth(esc, 0) 

#	Servo init
print("Big Servo Calibrating...")
Bservo = 14 #GPIO: 14, Pin: 8
min_Bservo = 550  # 0.55 ms
max_Bservo = 2450  # 2.45 ms
mid_Bservo = 1550  # 1.55 ms
print("Big Servo Calibration Complete")

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

def start():
	Xdist = depth(0)
	if Xdist > 200:
		num = 1
	elif Xdist>150:
		num = 3
    # elif Xdist > 100:
    #     Xdist -= 100
    #     num = 5
    # else:
    #     print("ERROR NO OBJECTS AHEAD")
    #     num = -1
    # return num
	
def makeMap(track, num):
    greenX, greenY, redX, redY = track.plot()
    plt.scatter(greenX, greenY, c='green')
    plt.scatter(redX, redY, c='red')
    plt.title("Objects placed on the map")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()
	
	for i in greenX.__iter__:
		if (greenY[i] > 2100):
			xVals = [greenX[i], greenX[i]]
			yVals = [greenY[i], 3000]
			plt.plot(xVals, yVals)
		elif (greenY[i] < 900):
			xVals[greenX[i], greenX[i]]
			yVals[greenY[i], 0]
			plt.plot(xVals, yVals)
		elif (greenX[i] > 2100):
			xVals[greenX[i], 3000]
			yVals[greenY[i], greenY[i]]
		elif (greenX[i] < 900):
			xVals[greenX[i], 1000]
			yVals[greenY[i], greenY[i]]

		

	
	
    
#-------------------------Main Code-------------------------#

num = start()

makeMap(track, num)