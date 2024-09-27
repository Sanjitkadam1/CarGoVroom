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
        print("going")
        if data:
            print(data)
            if data[0] == 0x54:
                break

    packet = b''
    while True:
        data = ser.read(1)
        print("going")
        if data:
            packet = packet + data
            print(hex(packet))
            if data[0] == 0x54:
                break
    
    if not len(packet) > 16:
        return readData()
    
    if not (packet[0] == 0x2C):
        print("Something goofed up")
        raise Exception

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
    return angles, lengths, intens
    

def graphfunc(ang, lens):
    return plt.polar(ang, lens)


def add2global(ang, lens, gang, glen):
    startang = ang[0]
    endang = ang[len(ang)-1]
    for x in range(0, len(gang)):
        if gang[x] < startang < gang[x+1]:
            while (gang[x+1] < endang):
                glen.remove(x+1)
                gang.remove(x+1)
            for i in range(0, len(ang)):
                glen.insert(x+1, lens[i])
                gang.insert(x+1, ang[i])
            break
    return gang, glen


globalang = []
globallen = []
while True:
    ang, lens, ints = readData()
    add2global(ang, lens, globalang, globallen)
    