import matplotlib.pyplot as plt
import object
import time as t
track = object.track()
track.random()
greenX, greenY, redX, redY = track.plot()
plt.scatter(greenX, greenY, c='green')
plt.scatter(redX, redY, c='red')
plt.title("Objects placed on the map")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.xlim(0, 3000)
plt.ylim(0, 3000)
plt.show()
print(greenY)
print(greenX)

t.sleep(2)
for i in range(len(greenX)):
    if (greenY[i] > 2100):
        print(1)
        xVals = [greenX[i], greenX[i]]
        yVals = [greenY[i], 3000]
        plt.plot(xVals, yVals, color='red')
    elif (greenY[i] < 900):
        print(2)
        xVals = [greenX[i], greenX[i]]
        yVals = [greenY[i], 0]
        plt.plot(xVals, yVals, color='black')
    elif (greenX[i] > 2100):
        print(3)
        xVals = [greenX[i], 3000]
        yVals = [greenY[i], greenY[i]]
    elif (greenX[i] < 900):
        print(4)
        xVals = [greenX[i], 1000]
        yVals = [greenY[i], greenY[i]]

plt.xlim(0, 3000)
plt.ylim(0, 3000)
plt.show()