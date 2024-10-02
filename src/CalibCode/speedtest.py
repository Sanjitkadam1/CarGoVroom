import time as t
import os
os.system ("sudo pigpiod")
print("importing packages...")
t.sleep(1)
import pigpio # type: ignore
import RPi.GPIO as PIN # type: ignore
import numpy as np 
from picamera2 import Picamera2 # type: ignore
import matplotlib.pyplot as plt
import math
print("Imported all nessesary packages")
import serial

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


pi = pigpio.pi()

while True:
    print("Enter how many seconds you want to go run: ")
    inp = input()
    start()
    t.sleep(int(inp))
    stop()


