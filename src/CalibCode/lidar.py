import serial
import numpy as np
import matplotlib.pyplot as plt



port = "/dev/serial0" # Put in the port
baud_rate = 230400

ser = serial.Serial(port=port, baudrate=baud_rate, parity="N")

def position(ang, lens):
    tolerance = 10                                                                                          
    offcenter = getAngle(ang, lens)
    ang = np.array(ang)
    ang = ang + offcenter
    dist = 0
    count = 0
    for i in range(0, ang):
        if ang[i] > 360 - tolerance or ang[i] < tolerance:
            count+=1
            dist+= np.sin(ang[i])*lens
    xcoord = dist/count
    dist = 0
    count = 0
    for i in range(0, ang):
        if ang[i] > 90 - tolerance and ang[i] < 90 + tolerance:
            count+=1
            dist+= np.cos(ang[i])*lens
    ycoord = dist/count

    return xcoord, ycoord

def getAngle(ang, lens):
    tolerance = 10

            

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

    if not len(packet) > 31:
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

angRet = np.array(angRet)
angRet = angRet - 180

ang_rad = np.deg2rad(angRet)

ax = plt.scatter(angRet, lenRet)

# x = np.sin(ang_rad)*lenRet
# y = np.cos(ang_rad)*lenRet

# y = -y
# ax = plt.scatter(x, y)
plt.show()






