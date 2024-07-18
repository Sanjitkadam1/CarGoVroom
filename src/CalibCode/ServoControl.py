import os
import time as t
os.system("sudo pigpiod")
t.sleep(1)
import pigpio

pi = pigpio.pi()

# Function to set the servo position
def set_servo_position(pulse_width):
    pi.set_servo_pulsewidth(servo_pin, pulse_width)

def servo_direct_control():
    num = mid_pulse_width
    set_servo_position(num)
    while True:
        print("r, l, c, stop")
        print()
        inp = input()
        if inp not in ("r", "l", "c", "stop"):
            print("Invalid input. Please enter 'r', 'l', 'c', or 'stop'.")
            continue
        if inp == "r":
            num = num + 50
        elif inp == "l":
            num = num - 50
        elif inp == "c":
            num = mid_pulse_width
        elif inp == "stop":
            break
        set_servo_position(num)
        print(num)
def servo_degree_control():
    num = mid_pulse_width
    set_servo_position(num)
    while True:
        print("10l","10r", "20l","20r", 30, 45, "res", "stop")
        print()
        #65 is 10 degrees
        inp = input()
        if (inp == "10l"):
            set_servo_position(1615) #added 65
        elif (inp == "10r"):
            set_servo_position(1485) #subtracted 65
        elif (inp == "20l"):
            set_servo_position(1680) #added 130
        elif (inp == "20r"):
            set_servo_position(1420) #subtracted 130
        elif (inp == "30l"):
            set_servo_position(1745) #added 195
        elif (inp == "30r"):
            set_servo_position(1355) #subtracted 195
        elif (inp == "40l"):
            set_servo_position(1810) #added 260
        elif (inp == "40r"):
            set_servo_position(1290) #subtracted 260
        elif (inp == "res"):
            set_servo_position(num)
        elif (inp == "stop"):
            break
        
        


def servo_trim():
    num = mid_pulse_width
    set_servo_position(num)
    while True:
        print("r, l, c, stop")
        print()
        inp = input()
        if inp not in ("r", "l", "c", "stop"):
            print("Invalid input. Please enter 'r', 'l', 'c', or 'stop'.")
            continue
        if inp == "r":
            num = num + 5
        elif inp == "l":
            num = num - 5
        elif inp == "c":
            num = mid_pulse_width
        elif inp == "stop":
            break
        set_servo_position(num)
        print(num)

servo_pin = 14
min_pulse_width = 550  # 1 ms
max_pulse_width = 2450  # 2 ms
mid_pulse_width = 1550  # 1.55 ms

while True:
    set_servo_position(mid_pulse_width)
    print("------------------------Servo Control------------------------")
    print("direct control, trim, degree, stop")
    print()
    inp = input()
    if inp == "direct control":
        servo_direct_control()
    elif inp == "trim":
        servo_trim()
    elif inp == "degree":
        servo_degree_control()
    elif inp == "stop":
        break

# Clean up and stop the pigpio daemon
pi.set_servo_pulsewidth(servo_pin, 0)  # Stop sending pulses to the servo
pi.stop()
