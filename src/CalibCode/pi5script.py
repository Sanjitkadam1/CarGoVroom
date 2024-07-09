from picamera2 import Picamera2 # type: ignore
import cv2 as cv
import numpy as np
import time
import serial 

picam = Picamera2()

# runs 

def initcam():
	config = picam.create_still_configuration()
	picam.configure(config)
	picam.start()
	time.sleep(2)
	print("Starting the camera")

def takephoto(startX, startY, endX, endY):
	picam.capture_file("test.jpeg")
	img = cv.imread("test.jpeg")
	if img is None:
		raise FileNotFoundError
	
	cropped = img[startY:endY, startX:endX]
	return cropped


def detectColor(img):
	hsvimg = cv.cvtColor(img, cv.COLOR_BGR2HSV)

	#Finding green 
	greenLow = np.array([51, 100, 100])
	greenHigh = np.array([61, 255, 255])

	greenMask = cv.inRange(hsvimg, greenLow, greenHigh)
	greenper = np.count_nonzero(greenMask)
	
	#Finding red
	lower_red1 = np.array([0, 100, 100])
	upper_red1 = np.array([10, 255, 255])
	lower_red2 = np.array([170, 100, 100])
	upper_red2 = np.array([180, 255, 255])

	redmask1 = cv2.inRange(img, lower_red1, upper_red1)
	redmask2 = cv2.inRange(img, lower_red2, upper_red2)
	redMask = cv2.bitwise_or(redmask1, redmask2)
	redper = np.count_nonzero(redMask)

	#for debugging purposes
	cv.imwrite("greenthresh.jpeg", greenMask)
	cv.imwrite("redthresh.jpeg", redMask)

	if (greenper > redper):
		return 0
	else :
		return 1


ser = serial.Serial(
    port='dev/ttyUSB0',
    baudrate=9600,
    timeout=0.75
)

while True:
	if ser.in_waiting > 0:
		X1byte = ser.read(2)
		Y1byte = ser.read(2)
		X2byte = ser.read(2)
		Y2byte = ser.read(2)

		ser.write(1)
		
		#Convert pixels 


		startX = int.from_bytes(X1byte)
		startY = int.from_bytes(Y1byte)
		endX = int.from_bytes(X2byte)
		endY = int.from_bytes(Y2byte)

		img = takephoto(startX, startY, endX, endY)
		color = detectColor(img)
		ser.write(color)