import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import threading


port = "/dev/serial0" # Put in the port
baud_rate = 230400

ser = serial.Serial(port=port, baudrate=baud_rate, parity="N")

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

    if not len(packet) > 16:
        return readData()
    
    if not (packet[0] == 0x2C):
        print("Woah")
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

    step = (endAngle-startAngle)/(len(lengths)-1)
    angles = []
    for i in range(0, len(lengths)):
        angles.append(startAngle + (step*i))
    
    return np.round(angles), np.round(lengths)
    

def get360():
    angRet = np.array()
    lenRet = np.array()
    for _ in range(30):
        ang, lens = readData()
        angRet = np.concatenate((angRet, np.array(ang)))
        lenRet = np.concatenate((lenRet, np.array(lens)))
    return angRet, lenRet

def plotfunc(ang, lens):
    ang_rad = np.deg2rad(ang)
    ax = plt.polar(ang_rad, lens)
    plt.show()
    plt.show(block=False)
    plt.pause(0.5)

plt.ion()

ang, lens = get360()
plotfunc(ang, lens)