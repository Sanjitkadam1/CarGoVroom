import time 
import smbus

sm = smbus.SMBus(1)

gyroCalibX = 0
gyroCalibY = 0
gyroCalibZ = 0
accelCalibX = 0
accelCalibY = 0
accelCalibZ = 0

def config ():
	sm.write_byte_data(0x68, 0x6B, 0x00)
	sm.write_byte_data(0x68, 0x1A, 0x06)
	sm.write_byte_data(0x68, 0x1B, 0x70)
	sm.write_byte_data(0x68, 0x1C, 0x1F)


		
def gyroVals (): 
	
	rawDataX = sm.read_i2c_block_data(0x68, 0x43, 2)
	rawDataY = sm.read_i2c_block_data(0x68, 0x45, 2)
	rawDataZ = sm.read_i2c_block_data(0x68, 0x47, 2)
	
	rawX = (rawDataX[0] << 8) | rawDataX[1]
	rawY = (rawDataY[0] << 8) | rawDataY[1]
	rawZ = (rawDataZ[0] << 8) | rawDataZ[1]

	# 16 bit negative
	if rawX > 32767:
		rawX -= 65536
	if rawY > 32767:
		rawY -= 65536
	if rawZ > 32767:
		rawZ -= 65536
		
	return rawX, rawY, rawZ


def accelVals (): 
	rawDataX = sm.read_i2c_block_data(0x68, 0x3B, 2)
	rawDataY = sm.read_i2c_block_data(0x68, 0x3D, 2)
	rawDataZ = sm.read_i2c_block_data(0x68, 0x3F, 2)

	rawX = (rawDataX[0] << 8) | rawDataX[1]
	rawY = (rawDataY[0] << 8) | rawDataY[1]
	rawZ = (rawDataZ[0] << 8) | rawDataZ[1]

	# 16 bit negative
	if rawX > 32767:
		rawX -= 65536
	if rawY > 32767:
		rawY -= 65536
	if rawZ > 32767:
		rawZ -= 65536

	return rawX, rawY, rawZ

config()
for i in range(2000):
	sampleX, sampleY, sampleZ = gyroVals()
	gyroCalibX += sampleX
	gyroCalibY += sampleY
	gyroCalibZ += sampleZ
	
gyroCalibX/=2000
gyroCalibY/=2000
gyroCalibZ/=2000

gyroCalibX = round(gyroCalibX)
gyroCalibY = round(gyroCalibY)
gyroCalibZ = round(gyroCalibZ)
		
print(f"Gyro Calibration Values: X={gyroCalibX}, Y={gyroCalibY}, Z={gyroCalibZ}")

for i in range(2000):
	sampleX, sampleY, sampleZ = accelVals()
	accelCalibX += sampleX
	accelCalibY += sampleY
	accelCalibZ += sampleZ

accelCalibX/=2000
accelCalibY/=2000
accelCalibZ/=2000

accelCalibX = round(accelCalibX)
accelCalibY = round(accelCalibY)
accelCalibZ = round(accelCalibZ)

print(f"Accel Calibration Values: X={accelCalibX}, Y={accelCalibY}, Z={accelCalibZ}")

while True:
	try:
		gyroX, gyroY, gyroZ = gyroVals()
		gyroY -= gyroCalibY
		gyroZ -= gyroCalibZ
		gyroX -= gyroCalibX

		print(f"{gyroX}, {gyroY}, {gyroZ}")
	except KeyboardInterrupt:
		print ("Interrupt")
		break

sm.close()
