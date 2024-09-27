import time as t
import os
os.system ("sudo pigpiod")
print("importing packages...")
t.sleep(1)
import pigpio # type: ignore
import RPi.GPIO as PIN # type: ignore
import numpy as np 
import cv2 as cv # type: ignore
from picamera2 import Picamera2 # type: ignore
import json 
import time 
import smbus # type: ignore
import matplotlib.pyplot as plt
import math
print("Imported all nessesary packages")

fig, ax = plt.subplots()
innerbox = ([1000,2000,2000,1000,1000],[1000,1000,2000,2000,1000])
ax.plot(innerbox, label = "innerbox", color = 'black')
outerbox = ([0,3000,3000,0,0],[0,0,3000,3000,0])
ax.plot(outerbox, label = "outerbox", color = 'black')

# arr1, arr2 = getAngLen()
# pointsX, pointsY = []
# for i in zip(arr1, arr2):
#   if(i[0] != 1000 or i[0] != 2000 or i[0] != 0 or i[0] != 3000):
#     if(i[1] != 0 or i[1] != 3000 or i[1] != 1000 or i[1] != 2000):
#       pointsX.append(i[0])
#       pointsY.append(i[1])

# plt.scatter(pointsX, pointsY, color = 'red', marker = 'x',label = "potential obstacles")


#A and B are arrays!
def goto(A, B):
  angL = math.atan((B[1] - A[1])/(B[0] - A[0])) #gets the angle of the line
  ang = getAngle() #gets the cars angle
  Bservo(angL - ang) #changes the wheel angle to the difference between angL and ang
  pi.set_servo_pulsewidth(esc, 1500) #Makes sure it is stopped
  stop()
  while position() != B: #while we arent at B yet, 
    pi.set_servo_pulsewidth(esc, 1570) #motor starts moving car
    ang = getAngle() #gets cars angle
    Bservo(angL - ang) #changes the wheel angle to the difference between angL and ang
  stop()
  if(A != B):
    goto(position(),B) #if we arent at B yet it will recursively call the function again
  else:
    return "reached",B #if not then we end the function


# plt.grid(True)
# plt.show()