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
print("Imported all nessesary packages")

fig, ax = plt.subplots()
ax.plot([1000,2000,2000,1000,1000],[1000,1000,2000,2000,1000], label = "innerbox")
ax.plot([0,3000,3000,0,0],[0,0,3000,3000,0], label = "outerbox")

#input the data from the LIDAR into a 2D arrays, X and Y (Like matplotlib)
#Sort through the values and disregard any values that are on the innerbox or outerbox lines. 
#The values that are left are the obstacles
#Save the obstacle as a landmark, fill in the next points since we know the dimensions of the obstacle
#Any new values that are given by the LIDAR that touch the obstacle is once again disregarded
#Take a picture to see if the object is green or red, then know if we need to move left or right
#If right/left then take a point that is right/left of it the width of the vehicle plus some more
#take the current position
#Run calcAng to find current angle
#calculate the line to go there
#Angle the wheels so it hits there and keep going forward, the LIDAR constantly checks the position of the vehicle so that it is always on the line
#Course correct so it stays on the line
#once it goes there repeat



plt.show()

