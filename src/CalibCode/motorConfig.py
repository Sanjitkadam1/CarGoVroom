import os     #importing os library so as to communicate with the system
import time as t   #importing time library to make Rpi wait because its too impatient 
os.system ("sudo pigpiod") #Launching GPIO library
t.sleep(1) 
import pigpio #importing GPIO library

max_motor = 2500 #max motor speed
min_motor = 2100  #min motor speed
pi = pigpio.pi()
esc = 15

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
