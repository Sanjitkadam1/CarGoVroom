import time
import serial

# Open serial port
try:
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
    ser.flush()
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)


while True:
	try:
		message = bytes([11])
		ser.write(message)
		print ("sent message")	
		time.sleep(1)
	except KeyboardInterrupt:
        	print("Exiting program.")
        	break

ser.close()
