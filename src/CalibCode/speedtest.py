import os 
import time
os.system ("sudo pigpio")
time.sleep(1)
import pigpio 

ESC = 20

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 0)

while True:
    print("How much do you want this to move (cm)")
    inp = input()
    print("Speed you want to go at (cm/sec)")
    speed = input()
    PWM = (speed/0.20667) + 744.6654
    time = speed/inp
    pi.set_servo_pulswidth(ESC, PWM)
    time.sleep(time)
