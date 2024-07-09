import RPi.GPIO as PIN 
import time

PIN.setmode(PIN.BCM)
PIN.setup(2, PIN.OUT)
PIN.output(2, PIN.LOW)
PIN.setup(3, PIN.IN)

def measureDist() -> int:
    PIN.output(2, PIN.HIGH)
    time.sleep(0.00001)   # Creating a 10uS (microsecond) pulse
    PIN.output(2, PIN.LOW)

    while PIN.input(3)==0:
      pulse_start = time.time()

    while PIN.input(3)==1:
       pulse_end = time.time()
    
    rawDist = pulse_end - pulse_start

    cmDist = rawDist * 34600/2 
    #34600 cm/s is the speed of sound in room temprature air. speed * time = distance. divided by 2 bcz its a round trip
    
    cmDist = round(cmDist, 2)
    return cmDist

time.sleep(2)

while True:
   print(f"Distance measured => {measureDist}")
   time.sleep(1)

