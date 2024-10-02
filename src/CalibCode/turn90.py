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
import smbus # type: ignore
import matplotlib.pyplot as plt
import math
print("Imported all nessesary packages")

def turn90(side):
    ang = getAngle()

    if side == "left":
        Bservo(-30)
        pi.setservo_pulsewidth(esc, 1570)
        while ang != 0:
            ang = getAngle()
    elif side == "right":
        Bservo(30)
        pi.setservo_pulsewidth(esc, 1570)
        while ang != 0:
            ang = getAngle()
    
    stop()
    Bservo(0)

    