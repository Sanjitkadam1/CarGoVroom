import os 
import time
os.system ("sudo pigpio")
time.sleep(1)
import pigpio 

ESC = 20

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 0)

while True:
    pi.set_servo_pulswidth(ESC, 0)
    time.sleep(1)
    print("How much do you want this to move (cm) in between the range: 188 < x < 350")
    inp = input()
    print("Speed you want to go at (cm/sec)")
    speed = input()
    PWM = (speed/0.20667) + 744.6654
    t = speed/inp
    pi.set_servo_pulswidth(ESC, PWM)
    time.sleep(t)
