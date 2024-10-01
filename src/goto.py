import time as t
import os
os.system ("sudo pigpiod")
print("importing packages...")
t.sleep(1)
import pigpio # type: ignore
import pigpio # type: ignore
import RPi.GPIO as PIN # type: ignore
import numpy as np # type: ignore
import cv2 as cv # type: ignore
from picamera2 import Picamera2 # type: ignore
import matplotlib.pyplot as plt # type: ignore
import matplotlib.pyplot as plt # type: ignore
import time 
import smbus # type: ignore
import math
import subprocess
import serial
print("Imported all nessesary packages")

port = "/dev/serial0"
baud_rate = 230400

ser = serial.Serial(port=port, baudrate=baud_rate, parity="N")

#	General init
print("Initialization Starting...")
t.sleep(0.5)
START = t.time()
#track = object.track()

#	Motor init
pi = pigpio.pi()
esc = 18
pi.set_servo_pulsewidth(esc, 0)

#	Servo init
print("Servo Calibrating...")
servo = 14 #GPIO: 14, Pin: 8
print("Servo Calibration Complete") 

Camera init
print("Camera Calibrating...")
picam = Picamera2()
config = picam.create_still_configuration()
picam.configure(config)
picam.start()
t.sleep(2)
print("Camera Calibration Complete")

print("Initialization Complete")
t.sleep(1)

def slice(ang, lens, upper, lower, ite=False):
    x = []
    y = []
    if ite:
        for i in range(0, len(ang)):
            if (ang[i] > lower) or (ang[i] < upper):
                rad = ang[i]*np.pi/180
                x.append(np.cos(rad)*lens[i])
                y.append(np.sin(rad)*lens[i])
    for i in range(0, len(ang)):
        if (ang[i] > lower) and (ang[i] < upper):
          rad = ang[i]*np.pi/180
          x.append(np.cos(rad)*lens[i])
          y.append(np.sin(rad)*lens[i])

    #REMOVES OUTLIERS -------

    # Convert x and y to numpy arrays for easier manipulation
    x = np.array(x)
    y = np.array(y)
# Calculate IQR (Interquartile Range)
    q1 = np.percentile(y, 25)
    q3 = np.percentile(y, 75)
    iqr = q3 - q1

    # Define the bounds for outliers
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    while i < len(y):
        if y[i] > upper_bound:
            y[i] = y[y != y[i]]
            x[i] = x[x != x[i]]
        elif y[i] < lower_bound:
            y[i] = y[y != y[i]]
            x[i] = x[x != x[i]]
        i+=1
    return x, y

def graph(angRet, lenRet): # Polar coordinates -> Cartesian (and graphs)
    angRet = np.array(angRet)

    ang_rad = np.deg2rad(angRet)

    x = np.cos(ang_rad)*lenRet
    y = np.sin(ang_rad)*lenRet

    ax = plt.scatter(x, y)
    plt.show()

def toCart(angRet, lenRet): # Polar coordinates -> Cartesian
    angRet = np.array(angRet)
    ang_rad = np.deg2rad(angRet)

    x = np.cos(ang_rad)*lenRet
    y = np.sin(ang_rad)*lenRet

    return x, y

def position(ang, lens): # This is relative to each turn
    offcenter = getAngle(ang, lens) 
    ang = np.array(ang)
    for i in range(0, len(ang)):
        if (ang[i]<offcenter):
            ang[i] = ang[i] - offcenter+360
        else:
            ang[i] = ang[i] - offcenter
    x, y = toCart(ang, lens)
    left = []
    right = []
    for i in range(0, len(x)):
        if y[i] > 0:
            if -250 < x[i] < 250:
                left.append(y[i])
        else:
            if -250 < x[i] < 250:
                right.append(y[i])
    xl = np.median(left)
    print("xl: ", xl)
    xr = -(np.median(right))
    print("xr: ", xr)
    front = []
    back = []
    for i in range(0, len(y)):
        if x[i] > 0:
            if -(0.5*xr) < y[i] < 0.5*xl:
                front.append(x[i])
        else:
            if -(0.5*xr) < y[i] < 0.5*xl:
                back.append(x[i])
    yf = np.median(front)
    print("yf: ", yf)
    if len(back) == 0:
        print("unreliable y (back missing)")
        yb = 3000 - (yf+diam)
    else: 
        yb = -(np.median(back))
    print("yb: ", yb)

    diam = 35.1

    leny = yb + yf + diam
    lenx = xr + xl + diam

    if not (2950 > leny) and (3050 < leny):
        print("unreliable y")
    if not ((950 > lenx) and (1050 < lenx)) or ((2950 > lenx) and (3050 < lenx)):
        print("unreliable x")

    return (xl, yb)

def getAngle(ang, lens):
    x = []
    y = []
    xi, yi = toCart(ang, lens)
    for i in range(0, len(yi)):
        if yi[i] > 0:
            if -150 < xi[i] < 150:
                x.append(xi[i])
                y.append(yi[i])
    n = len(x)
    x = np.array([x])
    y = np.array([y])

    # Calculate the components of the linear regression equation
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_x_sq = np.sum(x**2)
    sum_xy = np.sum(x * y)

    # Use the linear regression formula
    if (n * sum_x_sq - sum_x**2) != 0:  # Avoid division by zero
        m = (n * sum_xy - sum_x * sum_y) / (n * sum_x_sq - sum_x**2)
    else:
        m = 0  # Special case where the regression isn't possible

    # Now we calculate the angle from the regression slope
    if m != 0:
        rad = np.arctan(m)  # arctan of the slope gives the angle in radians
        deg = np.degrees(rad)  # Convert radians to degrees
    else:
        deg = 0  # If no slope, angle is 0

    print("Computed angle (deg):", deg)

    return deg

def readData():
    while True:
        data = ser.read(1)
        if data:
            if data[0] == 0x54:
                break

    packet = b''
    while True:
        data = ser.read(1)
        if data:
            packet = packet + data
            if data[0] == 0x54:
                break

    if not len(packet) > 46:
        return readData()

    if not (packet[0] == 0x2C):
        print("Woah", hex(packet[0]))
        return readData()
 
    Speed = int.from_bytes(packet[1:3], byteorder="little")
    startAngle = int.from_bytes(packet[3:5], byteorder="little")
    measure = packet[5:len(packet)-5]
    postdata = packet[len(packet)-5:]

    lengths = []
    intens = []
    for i in range(0, len(measure)//3):
        lengths.append(int.from_bytes(measure[(3*i):(3*i)+2], byteorder="little"))
        intens.append(int.from_bytes(measure[(3*i)+2:(3*i)+3]))


    endAngle = int.from_bytes(postdata[0:2])
    startAngle = startAngle/100
    endAngle = endAngle/100
    
    if (startAngle > 360) or (endAngle > 360):
        return readData()
    
    if (startAngle > endAngle):
        step = endAngle+360 - startAngle
    else:
        step = (endAngle-startAngle)/(len(lengths)-1)
    angles = []
    for i in range(0, len(lengths)):
        ang = startAngle + (step*i)
        if ang>360:
            ang = ang - 360
        angles.append(ang)
    
    return angles, lengths

def getData():   
	angRet = []
	lenRet = []
	for _ in range(0, 30):
		ang, lens = readData()
		for i in range(0, len(ang)):
			angRet = np.concatenate((angRet, np.array(ang)))
			lenRet = np.concatenate((lenRet, np.array(lens)))
    
	return angRet, lenRet

def Bservo(x):
    servo = 14
    if x > 30:
        pi.set_servo_pulsewidth(servo, (6.5*30) + 1550)
        return
    elif x < -30:
        pi.set_servo_pulsewidth(servo, (6.5*-30) +1550)
        return
    pulsewidth = (6.5*x) + 1550
    pi.set_servo_pulsewidth(servo, pulsewidth)
    return

fig, ax = plt.subplots()
innerbox = ([1000,2000,2000,1000,1000],[1000,1000,2000,2000,1000])
ax.plot(innerbox, label = "innerbox", color = 'black')
outerbox = ([0,3000,3000,0,0],[0,0,3000,3000,0])
ax.plot(outerbox, label = "outerbox", color = 'black')

def detectObjs(track, turn):
	picam.capture_file("test.jpeg")
	img = cv.imread("test.jpeg")
	height, width, channels = img.shape
	hsvimg = cv.cvtColor(img, cv.COLOR_BGR2HSV)

	#Finding green 
	greenLow = np.array([51, 100, 100])
	greenHigh = np.array([61, 255, 255])
	greenMask = cv.inRange(hsvimg, greenLow, greenHigh)

	greenContours, greenHierarchy = cv.findContours(greenMask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	side = None
	for contour in greenContours:
		MAX = -1
		x, y, Cwidth, Cheight = cv.boudingRect(contour)
		if Cheight > height/10 and (Cwidth*Cheight) > MAX and Cwidth > width/10:
			MAX = Cheight*Cwidth
			if (MAX > minArea):
				if (x > width/2 and (x-Cwidth) > width/2):
					side = "left"
				elif x < width/2: 
					side = "right"

	if (side == "left"):
		objGreen = object.obj(turn, num, "green")
		track.add(objGreen)
	elif (side == "right"):
		objGreen = object.obj(turn, num+1, "green")
		track.add(objGreen)

	#Finding red
	lower_red1 = np.array([0, 100, 100])
	upper_red1 = np.array([10, 255, 255])
	lower_red2 = np.array([170, 100, 100])
	upper_red2 = np.array([180, 255, 255])

	redmask1 = cv.inRange(img, lower_red1, upper_red1)
	redmask2 = cv.inRange(img, lower_red2, upper_red2)
	redMask = cv.bitwise_or(redmask1, redmask2)

	redContours, redHierarchy = cv.findContours(redMask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	side = None
	for contour in redContours:
		MAX = -1
		x, y, Cwidth, Cheight = cv.boudingRect(contour)
		if Cheight > height/10 and (Cwidth*Cheight) > MAX and Cwidth > width/10:
			MAX = Cheight*Cwidth
			minArea = 0 # !!!! SET THIS V. IMP
			if (MAX > minArea):
				if (x > width/2 and (x-Cwidth) > width/2):
					side = "left"
				elif x < width/2: 
					side = "right"
	
	if (objGreen.turn == "left" and not side == None):
		print("ERROR DUPLICATE OBJECT DETECTED OR BINARY ERROR")

	if (side == "left"):
		objRed = object.obj.__init__(turn, num, "red")
		track.add(objRed)
	elif (side == "right"):
		if (objGreen.turn == "right"):
			print("ERROR DUPLICATE OBJECT DETECTED")
		objRed = object.obj.__init__(turn, num+1, "red")
		track.add(objRed)

	return turn, num

def reedsShep():
    # Run the bash script and capture the output
    result = subprocess.run(['bash', 'movement.sh'], capture_output=True, text=True)

    # The output will be captured in result.stdout
    print("Script Output:")
    print(result.stdout)

    # If there is any error, it will be in result.stderr
    if result.stderr:
        print("Script Error:")
        print(result.stderr)
        return 0
    return result.stdout()

def stop():
    esc = 18
    pi.set_servo_pulsewidth(esc, 1500)
    t.sleep(0.01)
    pi.set_servo_pulsewidth(esc, 1300)
    t.sleep(0.01)
    pi.set_servo_pulsewidth(esc, 1500)
    t.sleep(0.01)
    pi.set_servo_pulsewidth(esc, 1300)
    t.sleep(0.01)
    pi.set_servo_pulsewidth(esc, 1500)

def start():
    esc = 18
    pi.set_servo_pulsewidth(esc, 1500)
    pi.set_servo_pulsewidth(esc, 1600)

def foward(dist) -> int:
    return dist # This is the distance to time conv, at 1600 PWM

def back():
    esc = 18
    stop()
    pi.set_servo_pulsewdith(esc, 1300)
    t.sleep(0.2) # Edit this
    pi.set_servo_pulsewdith(esc, 1500)
    pi.set_servo_pulsewidth(esc, 1600)
    pi.set_servo_pulsewdith(esc, 1500)
    pi.set_servo_pulsewdith(esc, 1600)
    t.sleep(0.01)
    pi.set_servo_pulsewdith(esc, 1500)

def checkpos(current, final):
    tolerance = 10
    checkx = np.abs(final[0] - current[0]) < tolerance
    checky = np.abs(final[1] - current[1]) < tolerance
    
    print("Position checks", checkx, checky)
    return checkx and checky


def goto(final):
    tolerance = 10 #car should stop minimum of 10mm ahead of the point, adjustable 
    angRet, lenRet = getData() #gets data from LIDAR
    current = position(angRet,lenRet) #gets current position from data from LIDAR
    ang = getAngle() #gets cars current position
    rs = reedsShep(current,final,ang) #reedsShep() function will give a list of points(tuples), in the format of (x,y,velocity)
    for i in range(0,rs.length()): #for each tuple in rs
        point = rs[i] #the final point for this loop is point
        angRet, lenRet = getData()
        current = position(angRet, lenRet) #gets current pos
        angL = math.atan((point[1] - current[1])/(point[0] - current[0])) # gets the angle of the line from current pos to point
        angL = angL*180/np.pi #converts rad to deg 
        Bservo(angL - ang) #sets the angle to the difference between the angle of the line, and the angle of the current pos
        if point[2] < 0: #if velocity is negative, the car needs to move backwards
            back() #starts moving the car backwards
        else:
            start() #starts moving the car forwards
        check = checkpos()
        while check != True: #until the car gets to point 
            angRet, angLet = getData() 
            current = position(angRet, angLet) #gets current pos
            ang = getAngle(angRet, angLet) #gets current angle
            
            if ang < angL or ang > angL:
                Bservo(angL - ang) #sets the angle to the difference between the angle of the line, and the angle of the current pos
            check = checkpos()
        stop() #stops the car
    stop()
    angRet, lenRet = getData() #gets data from LIDAR
    current = position(angRet,lenRet) #gets current position from data from LIDAR
    if current < final[1]-tolerance or current > final[1]+tolerance:
        print("not there just yet, retrying")
        goto(final)
    else:
        print("reached",final)
    






Bservo(0)
angRet, lenRet = getData()
startingPos = position(angRet,lenRet)
rounds = 0
turns = 0
Carwidth = 190 #Settable value

while rounds <= 3:  
    g = (300,100)
    goto(g)
    g = (500,900)
    goto(g)
    

#while rounds <= 3:
# 	g = (500,2000)
# 	goto(g)
# 	pos = position(*getData())
# 	Bservo(30)
# 	pi.set_servo_pulsewidth(servo,1600)
# 	t.sleep(1)
# 	pi.set_servo_pulsewidth(servo,1500)
# 	turns = turns + 1
# 	if turns == 4:
# 		turns = 0
# 		rounds = rounds + 1

# angRet, angLet = getData()
# current = position(angRet, angLet)
# if startingPos[1] < current[1]:
#     stop()
#     print("overshot lol")

# else:
#     goto(startingPos)


# go88