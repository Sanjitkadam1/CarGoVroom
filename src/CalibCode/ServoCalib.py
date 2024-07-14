import RPi.GPIO as GPIO #type: ignore
import time

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

# Create a PWM instance
pwm = GPIO.PWM(17, 50)  # 50 Hz
pwm.start(7.5)  # Neutral position

try:
    while True:
        # Rotate servo to 0 degrees
        pwm.ChangeDutyCycle(5)
        time.sleep(1)
        # Rotate servo to 90 degrees
        pwm.ChangeDutyCycle(7.5)
        time.sleep(1)
        # Rotate servo to 180 degrees
        pwm.ChangeDutyCycle(10)
        time.sleep(1)
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
