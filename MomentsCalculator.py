import matplotlib.pyplot as plt
import numpy as np

def calculate_moment(force, distance):
    return force * distance

def plot_seesaw(force1, distance1, force2, distance2):
    fig, ax = plt.subplots(figsize=(15, 10))  
    moment1 = calculate_moment(force1, distance1)
    moment2 = calculate_moment(force2, distance2)
    total_moment = moment1 - moment2
    angle = np.arctan(total_moment / 100) 
    seesaw_length = 30  
    pivot_height = 2  
    x = np.linspace(-seesaw_length/2, seesaw_length/2, 100)
    y = np.tan(angle) * x
    plt.plot(x, y, 'saddlebrown', lw=8, label='See-saw')
    plt.plot([0], [0], 'k^', markersize=15, label='Pivot')
    rect_width = 0.5
    rect_height1 = force1 / 5
    rect_height2 = force2 / 5
    y1 = np.tan(angle) * (-distance1)
    y2 = np.tan(angle) * distance2
    ax.add_patch(plt.Rectangle((-distance1 - rect_width / 2, y1), rect_width, rect_height1, color='blue'))
    ax.add_patch(plt.Rectangle((distance2 - rect_width / 2, y2), rect_width, rect_height2, color='orange'))
    plt.text(-distance1, y1 + rect_height1 + 0.5, f'{force1} N\n{distance1} m', ha='center', color='blue')
    plt.text(distance2, y2 + rect_height2 + 0.5, f'{force2} N\n{distance2} m', ha='center', color='orange')
    plt.text(-distance1, y1 - 2, f'Moment: {moment1} Nm', ha='center', color='blue')
    plt.text(distance2, y2 - 2, f'Moment: {moment2} Nm', ha='center', color='orange')
    ax.arrow(-distance1, y1 - 1.5, 0, -1, head_width=0.3, head_length=0.3, fc='blue', ec='blue')
    ax.arrow(distance2, y2 - 1.5, 0, -1, head_width=0.3, head_length=0.3, fc='orange', ec='orange')
    y_range = max(abs(np.tan(angle) * seesaw_length / 2), rect_height1, rect_height2) + 3
    ax.set_xlim([-seesaw_length/2 - 1, seesaw_length/2 + 1])
    ax.set_ylim([-y_range, y_range])
    plt.xlabel('Distance from pivot (m)')
    plt.ylabel('Force (scaled)')
    plt.title('See-saw Representation of Moments')
    plt.legend()
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.show()

def main():
    print("Welcome to the See-saw Moment Calculator!")
    forces = []
    distances = []
    for i in range(1, 3):
        while True:
            try:
                print(f"\nInput for Force {i}:")
                force = float(input("  Enter the force applied (in Newtons): "))
                distance = float(input("  Enter the distance from the pivot point (in meters): "))
                forces.append(force)
                distances.append(distance)
                break
            except ValueError:
                print("  Invalid input. Please enter numeric values for force and distance.\n")
    
    plot_seesaw(forces[0], distances[0], forces[1], distances[1])
    print("Thank you for using the See-saw Moment Calculator. Goodbye!")

if __name__ == "__main__":
    main()