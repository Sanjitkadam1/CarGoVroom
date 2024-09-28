import serial
import numpy as np
import SciPy
import matplotlib.pyplot as plt
from filterpy.kalman import KalmanFilter
import kf_book.book_plots as book_plots
from kf_book.book_plots import plot_errorbars


port = "/dev/serial0" # Put in the port
baud_rate = 230400

ser = serial.Serial(port=port, baudrate=baud_rate, parity="N")

def readData():
    while True:
        data = ser.read(1)
        if data:
            if data[0] == 0x54 and ser.read(1) == 0x2C:
                break

    packet = b''
    packet = bytes([0x2C])
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

# Add the filter over

# Define the smoothing factor (between 0 and 1), smaller means more smoothing
alpha = 0.2

# Apply exponential moving average filter
ema_data = []
ema = lenRet[0]  # Initialize with the first data point
for data in lenRet:
    ema = alpha * data + (1 - alpha) * ema
    ema_data.append(ema)

print("Smoothed Data (EMA):", ema_data)



x = np.sin(ang_rad)*lenRet
y = np.cos(ang_rad)*lenRet

y = -y
ax = plt.scatter(x, y)
plt.show()






