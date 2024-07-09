import time 
import RPi.GPIO
import numpy as np

ending = False

START = time.time()



while not ending:
	
    # Implement for frame 
	
	X, color = detectColor(img)
	if X != None:
		if (color == "red") and X :
			


def detectColor(img):
	# ASSIGN THRESHOLD
	thresh = 20
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

	if (redper > thresh):
		smallestX, smallestY = 100000000, 100000000
		greatestX, greatestY = -1, -1
		
        # Run a denoising algorithm 
		
		print("Red object detected")
		
		for x in range(redMask.shape[0]):
			for y in range(redMask.shape[1]):
				if redMask[x, y] == 255:
					if x <= smallestX and y <= smallestY and redMask[x+5, y+5] == 255:
						smallestX = x
						smallestY = y
					elif x >= greatestX and y >= greatestY and redMask[x-5, y-5] == 255:
						greatestX = x
						greatestY = y
						
        midX = (greatestX + smallestX)/2
        return midX, "red"

    if (greenper > thresh):
		smallestX, smallestY = 100000000, 100000000
		greatestX, greatestY = -1, -1
		
        # Run a denoising algorithm 
		
		print("Red object detected")
		
		for x in range(redMask.shape[0]):
			for y in range(redMask.shape[1]):
				if redMask[x, y] == 255:
					if x <= smallestX and y <= smallestY and redMask[x+5, y+5] == 255:
						smallestX = x
						smallestY = y
					elif x >= greatestX and y >= greatestY and redMask[x-5, y-5] == 255:
						greatestX = x
						greatestY = y
        midX = (greatestX + smallestX)/2
        return midX, "green"

    return None

def turn():
	# Need to implement
	return NotImplementedError

def setSpeed():
	 

def motorInit():
	