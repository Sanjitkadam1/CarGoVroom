import serial
import numpy as np
import matplotlib.pyplot as plt


port = "/dev/serial0" # Put in the port
baud_rate = 230400

ser = serial.Serial(port=port, baudrate=baud_rate, parity="N")


def getAngle(ang, lens):
    x = []
    y = []
    for i in range(0, len(ang)):
        if (ang[i] > 80) and (ang[i] < 100):
          print(lens[i])
          rad = ang[i]*np.pi/180
          x.append(np.cos(rad)*lens[i])
          y.append(np.sin(rad)*lens[i])
    
    #REMOVES OUTLIERS -------

    # Convert x and y to numpy arrays for easier manipulation
    x = np.array(x)
    y = np.array(y)
    n = len(x)
	# Calculate IQR (Interquartile Range)
    q1 = np.percentile(y, 25)
    q3 = np.percentile(y, 75)
    iqr = q3 - q1

    # Define the bounds for outliers
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    for i in range(0, len(y)):
        if y[i] > upper_bound:
            y[i] = y[i-1]
            x[i] = x[i-1]
        elif y[i] < lower_bound:
            y[i] = y[i+1]
            x[i] = x[i+1]

    #REMOVES OUTLIERS -------

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

    print([hex(b) for b in packet])
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
    
    return angles, lengths, intens

angRet = []
lenRet = []

for _ in range(0, 30):
    ang, lens, ints = readData()
    print(len(lens))
    print(len(ang))
    
    for i in range(0, len(ang)):
        print("angle", ang[i], "measurement - ", lens[i])
        angRet = np.concatenate((angRet, np.array(ang)))
        lenRet = np.concatenate((lenRet, np.array(lens)))
    print("data packet end")
    print()

a = getAngle(angRet, lenRet)

angRet = np.array(angRet)

ang_rad = np.deg2rad(angRet)

x = np.cos(ang_rad)*lenRet
y = np.sin(ang_rad)*lenRet

# ax = plt.scatter(x, y)
print(a)
plt.show()
