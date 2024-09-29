import serial
import numpy as np
import matplotlib.pyplot as plt

port = "/dev/serial0"
baud_rate = 230400

ser = serial.Serial(port=port, baudrate=baud_rate, parity="N")

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
    graph(ang, lens)
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
    print("lenx: ", lenx)
    print("leny: ", leny)

    if not (2950 > leny) and (3050 < leny):
        print("unreliable y")
    if not (950 > lenx) and (1050 < lenx):
        print("unreliable x")

    return xl, yb

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
    plt.scatter(x, y)

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

    print("Computed slope (m):", m)
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