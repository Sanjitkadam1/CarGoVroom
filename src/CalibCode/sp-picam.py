from picamera2 import Picamera2 # type: ignore
import cv2 as cv
import numpy as np
import time

picam = Picamera2()

# runs 

def initcam():
	config = picam.create_still_configuration()
	picam.configure(config)
	picam.start()

	time.sleep(2)
	print("Starting the camera")

def takephoto ():
	picam.capture_file("test.jpeg")

def detectColor():
	img = cv.imread("test.jpeg")
	if img is None:
		raise FileNotFoundError
	hsvimg = cv.cvtColor(img, cv.COLOR_BGR2HSV)

	#Finding green 
	greenLow = np.array([38, 50, 50])
	greenHigh = np.array([80, 255, 255])
	greenMask = cv.inRange(hsvimg, greenLow, greenHigh)
	greenper = np.sum(greenMask == 255)

	cv.imshow("original photo", img)
	cv.imwrite("greenthresh.jpeg", greenMask)
	return "green"

initcam()
takephoto()
color = detectColor()
print(color)

picam.stop()
