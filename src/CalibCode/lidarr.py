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

    print([hex(b) for b in packet])
    if not (packet[0] == 0x2C):
        print("Woah", hex(packet[0]))
    
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

def graphfunc(ang, lens):
    return plt.polar(ang, lens)

def add2global(ang, lens, gang: list, glen: list):
    if (len(gang)<len(ang)-5):
        print("first")
        return ang, lens
    elif (ang[0]>ang[len(ang)-1]):
        print("overflow")
    else:
        for i in range(0, len(gang)): #This removes all the old values
            if (ang[0] <= gang[i] <= ang[len(ang)-1]):
                gang.remove(i)
                glen.remove(i)
        if (gang[len(gang)-1]<ang[len(ang)-1]): # If values are over the global
            print("above")
            gang = gang + ang
            glen = glen + lens
        elif (gang[0]>ang[0]): # if values are below the global
            print("below")
            ang = ang + gang
            glen = lens + glen
        else:
            print("normal")
            for i in range(0, len(gang)-1):
                if (gang[i] < ang[0] < gang[i+1]):
                    half1 = gang[:i+1]
                    haf1 = glen[:i+1]
                    half2 = gang[i+1:]
                    haf2 = glen[i+1]
                    gang = half1 + ang + half2
                    glen = haf1 + lens + haf2
                    break

    return gang, glen

def get360():
    angRet, lenRet = readData()
    startang = angRet[0]
    ang, lens = readData()
    angRet.extend(ang)
    lenRet.extend(lens) 
    while (ang[-1] < 360):
        ang, lens = readData()
        angRet.extend(ang)
        lenRet.extend(lens)
    while (ang[-1] < startang):
        ang, lens = readData()
        angRet.extend(ang)
        lenRet.extend(lens)

    return angRet, lenRet

globalang = []
globallen = []

while True:
    ang, lens = get360()
    for i in range(0, len(ang)):
        print("angle", ang, "len", lens)
