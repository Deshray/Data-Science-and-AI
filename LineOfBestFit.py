import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

repeat = int(input("How many values do you have? "))
xval = []
yval = []

for i in range(repeat):
    x = float(input(f"Enter x-coordinate {i+1}: "))
    y = float(input(f"Enter y-coordinate {i+1}: "))
    xval.append(x)
    yval.append(y)

xval = np.array(xval)
yval = np.array(yval)

# Using numpy's efficient least squares method
coefficients = np.polyfit(xval, yval, 1)
mfinal, cfinal = coefficients

print(f"The line of best fit is: y = {mfinal:.4f}x + {cfinal:.4f}")

# Plot the data and line
plt.figure(figsize=(10, 6))
plt.scatter(xval, yval, color='blue', label='Data points')
plt.plot(xval, mfinal * xval + cfinal, color='red', label=f'y = {mfinal:.4f}x + {cfinal:.4f}')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Line of Best Fit')
plt.legend()
plt.grid(True)
plt.show()

# Optional: Show 3D error surface
show_3d = input("Would you like to see the 3D error surface? (yes/no): ").lower()
if show_3d == 'yes':
    # Search around the optimal values
    m_range = np.linspace(mfinal - 2, mfinal + 2, 50)
    c_range = np.linspace(cfinal - 2, cfinal + 2, 50)
    m_grid, c_grid = np.meshgrid(m_range, c_range)
    
    errors = np.zeros_like(m_grid)
    for i in range(len(m_range)):
        for j in range(len(c_range)):
            m = m_grid[j, i]
            c = c_grid[j, i]
            errors[j, i] = np.sum((yval - (m * xval + c))**2)
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(m_grid, c_grid, errors, cmap='viridis', alpha=0.8)
    ax.scatter([mfinal], [cfinal], [np.sum((yval - (mfinal * xval + cfinal))**2)], 
               color='red', s=100, label='Optimal')
    ax.set_xlabel('Gradient (m)')
    ax.set_ylabel('Intercept (c)')
    ax.set_zlabel('Sum of Squared Errors')
    ax.set_title('Error Surface')
    plt.show()
