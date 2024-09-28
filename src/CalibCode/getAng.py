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

def getAng(len,ang):
    index60 = 0
    index120 = 0
    cnt = 0
    for i in ang:
        if ang[i] == 60:
            index60 = i
            cnt = cnt + 1
        elif ang[i] == 120:
            index120 = i
            cnt = cnt + 1
    while index60 < index120:   
        # np.sin((ang + index60)len)
        
        

