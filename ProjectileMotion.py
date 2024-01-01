import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def projectile_motion(t, v0, theta, air_resistance=False):
    g = 9.8  
    if air_resistance:
        k = 0.1 
        x = (v0 * np.cos(theta) / k) * (1 - np.exp(-k * t))
        y = ((v0 * np.sin(theta) + g / k) * (1 - np.exp(-k * t)) - g * t) / k
    else:
        x = v0 * np.cos(theta) * t
        y = v0 * np.sin(theta) * t - 0.5 * g * t**2
    return x, y

def update(frame):
    t = np.linspace(0, frame / 10, num=1000)  
    x, y = projectile_motion(t, v0, theta, air_resistance)
    line.set_data(x, y)
    return line,

theta = np.radians(float(input("Enter launch angle (degrees): ")))
v0 = float(input("Enter initial velocity (m/s): "))
air_resistance_input = input("Include air resistance? (yes/no): ").lower()
air_resistance = air_resistance_input == 'yes'

t_total_no_air_resistance = (2 * v0 * np.sin(theta)) / 9.8
max_height_no_air_resistance = (v0**2 * np.sin(theta)**2) / (2 * 9.8)
range_value_no_air_resistance = v0**2 * np.sin(2 * theta) / 9.8

print(f"Maximum Height (without air resistance): {max_height_no_air_resistance:.2f} meters")
print(f"Range (without air resistance): {range_value_no_air_resistance:.2f} meters")

fig, ax = plt.subplots()
ax.set_xlim(0, max(range_value_no_air_resistance, range_value_no_air_resistance) + 10)
ax.set_ylim(0, max(max_height_no_air_resistance, max_height_no_air_resistance) + 10)
ax.set_xlabel('Horizontal Distance (m)')
ax.set_ylabel('Vertical Distance (m)')
line, = ax.plot([], [], 'o-', label='Projectile Motion')
animation = FuncAnimation(fig, update, frames=range(1, int(t_total_no_air_resistance * 10)), blit=True)
plt.legend()
plt.show()
