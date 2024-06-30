import os
import time
os.system ("sudo pigpiod")
time.sleep(1)
import pigpio

pi = pigpio.pi()
ESC = 14
pi.set_servo_pulsewidth(ESC, 0) 

max_value = 1500 
min_value = 500

pi.set_servo_pulsewidth(ESC, 0)
print("Calibration start")
pi.set_servo_pulsewidth(ESC, max_value)
pi.set_servo_pulsewidth(ESC, min_value)
time.sleep(7)
print ("Calibrating....")
time.sleep (5)
pi.set_servo_pulsewidth(ESC, 0)
time.sleep(2)
print ("Arming ESC now...")
pi.set_servo_pulsewidth(ESC, min_value)
time.sleep(1)
print ("Calibration Complete")
        