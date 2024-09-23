import numpy as np
import matplotlib.pyplot as plt
import math

fig = plt.figure()
ax = plt.axes(projection='3d')

# Data for a three-dimensional line
zline = np.linspace(0, 15, 1000)
xline = np.sin(zline)
yline = np.cos(zline)
ax.plot3D(xline, yline, zline, 'gray')

length = 150
width = 100
cityCenter_x, cityCenter_y = 50, 50
# Data for three-dimensional scattered points
xdata = []
ydata = []
zdata = []
for x in range(0, length):
    for y in range(0, width):
        xdata.append(x)
        ydata.append(y)
        distance = math.sqrt((abs(x - cityCenter_x) ** 2) + (abs(y - cityCenter_y) ** 2))
        lratio = (length - distance) / length
        wratio = (width - distance) / width
        zdata.append(10*lratio * wratio)
print(max(zdata), min(zdata))
print(len(xdata), len(ydata), len(zdata))

ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens')


plt.show()