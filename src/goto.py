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
  angL = math.atan((B[1] - A[1])/(B[0] - A[0]))
  ang = getAngle()
  Bservo(ang)
  pi.set_servo_pulsewidth(esc, 1500)
  stop()
  while position() != B:
    pi.set_servo_pulsewidth(esc, 1570)
    ang = getAngle()
    n = angL - ang
    Bservo(n)
  stop()
  if(A != B):
    goto(position(),B)
  else:
    return "reached",B


# plt.grid(True)
# plt.show()