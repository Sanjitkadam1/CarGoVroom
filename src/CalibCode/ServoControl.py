import os
import time as t
os.system("sudo pigpiod")
t.sleep(1)
import pigpio # type: ignore

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
        print("Enter Degrees: ")
        inp = input()
        if(inp == "stop"):
            return 0
        try:
            PWM = Deg2PWM(inp)
        except:
            print("Ya boi put too much sauce in that PWM value")
        set_servo_position(PWM)
    
# Function to conver Degress into PWM
def Deg2PWM(x):
    x = int(x)
    if x > 40 or x < -40:
        return Exception
    return (6.5*x) + 1550


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
    print("------------------------Servo Control-------------------------")
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