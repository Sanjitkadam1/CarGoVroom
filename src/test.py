import matplotlib.pyplot as plt
import object
track = object.track()
track.random()
greenX, greenY, redX, redY, count = track.plot()
print(count)
plt.scatter(greenX, greenY, c='green')
plt.scatter(redX, redY, c='red')
plt.title("Objects placed on the map")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.xlim(0, 3000)
plt.ylim(0, 3000)
plt.show()