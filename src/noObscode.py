#-------------------------Packages--------------------------#
import time as t
import os
os.system ("sudo pigpiod")
print("importing packages...")
t.sleep(1)
import pigpio # type: ignore
import RPi.GPIO as PIN # type: ignore
print("Imported all nessesary packages")

#-------------------------Init Code-------------------------#
#	General init
print("Initialization Starting...")

#	Motor init
pi = pigpio.pi()
esc = 18
pi.set_servo_pulsewidth(esc, 0)

#	Servo init
print("Servo Calibrating...")
Bservo = 14 #GPIO: 14, Pin: 8
print("Servo Calibration Complete")

#Button init
buttonPin = 21
PIN.setup(buttonPin, PIN.IN, pull_up_down=PIN.PUD_UP)

print("Initialization Complete")
t.sleep(1)

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

def Bservo(x): #function to turn the servo
	servo = 14 #GPIO: 14, Pin: 8 
	# if x > 40 or x < -40: #our wheels cant turn more than 40 degrees both ways.
	# 	return Exception
	pulse_width = (6.5*x) + 1550 #equation we have made for pulsewidth conversion. y(pulsewidth) = 6.5(amount changing per degree)*x(degrees) + 1550(center)
	pi.set_servo_pulsewidth(servo, pulse_width)

def stop():
    esc = 18
    pi.set_servo_pulsewidth(esc, 1500)
    t.sleep(0.01)
    pi.set_servo_pulsewidth(esc, 1300)
    t.sleep(0.01)
    pi.set_servo_pulsewidth(esc, 1500)
    t.sleep(0.01)
    pi.set_servo_pulsewidth(esc, 1300)
    t.sleep(0.01)
    pi.set_servo_pulsewidth(esc, 1500)

def start():
    esc = 18
    pi.set_servo_pulsewidth(esc, 1500)
    pi.set_servo_pulsewidth(esc, 1600)

def back():
    esc = 18
    stop()
    pi.set_servo_pulsewdith(esc, 1300)
    t.sleep(0.2)
    pi.set_servo_pulsewdith(esc, 1500)
    pi.set_servo_pulsewidth(esc, 1600)
    pi.set_servo_pulsewdith(esc, 1500)
    pi.set_servo_pulsewdith(esc, 1600)
    t.sleep(0.01)
    pi.set_servo_pulsewdith(esc, 1500)

#-------------------------Main Code-------------------------#
#Starting at Starting position

turningTime = 2 # the amount of time it takes to turn 90 degrees
rounds = 0
turns = 4

stop()
Bservo(10)
t.sleep(3)
Bservo(0)
print("Waiting for button press...")

while True:
	buttonState = PIN.input(buttonPin)
	if buttonState == PIN.LOW:
		print("going!!!")
		t.sleep(1)
		break

# while rounds <= 3:
# 	dist = depth(0)
# 	while dist < 110:
# 		dist = depth(0)
# 	stop()
# 	dist = depth(0)
# 	if dist < 90:
# 		back()
# 		t.sleep(0.5)
# 		stop()
# 	Bservo(-30)
# 	start()
# 	t.sleep(0.5)
# 	t.sleep(turningTime)
# 	stop()
# 	Bservo(0)
# 	turns = turns - 1
# 	if turns == 0:
# 		turns = 4
# 		rounds = rounds + 1

while rounds <= 3:
	dist = depth(0)
	start()
	while dist > 250:
		dist = depth(0)
		if dist < 200:
			Bservo(-10)
			t.sleep(0.5)
		Bservo(0)
	stop()
	# dist = depth(0)
	Bservo(-30)
	start()
	t.sleep(0.5)
	t.sleep(turningTime)
	stop()
	Bservo(0)
	turns = turns - 1
	if turns == 0:
		turns = 4
		rounds = rounds + 1

stop()