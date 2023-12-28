import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

xval = []
yval = []
count = 0
repeat = int(input("How many values do you have?"))

while count != repeat:
    x = int(input("Enter x-coordinate:"))
    y = int(input("Enter y-coordinate:"))
    xval.append(x)
    yval.append(y)
    count = count + 1

mfinal = 0
cfinal = 0
m = 0
val = 0
error = float('inf')
errors = []

m_values = np.arange(0, 10, 0.1)
c_values = np.arange(0, 10, 0.1)

for m in m_values:
    m_errors = []
    for c in c_values:
        totalerror = sum((y - (m * x + c))**2 for x, y in zip(xval, yval))
        m_errors.append(totalerror)

        if totalerror < error:
            cfinal = c
            mfinal = m
            error = totalerror

    errors.append(m_errors)

print("The line of best fit is: y =", mfinal, "x +", cfinal)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

m_values, c_values = np.meshgrid(m_values, c_values)

flattened_errors = np.array(errors).flatten()
flattened_errors = flattened_errors.reshape(m_values.shape)

ax.plot_surface(m_values, c_values, flattened_errors, cmap='viridis')

ax.set_xlabel('Gradient')
ax.set_ylabel('Intercept')
ax.set_zlabel('Error')

plt.show()