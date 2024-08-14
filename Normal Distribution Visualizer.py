import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def visualize_normal_distribution(data):
    # Calculate mean and standard deviation of the dataset
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)

    # Generate a range of values from the data for plotting the normal distribution curve
    x_values = np.linspace(min(data), max(data), 100)
    y_values = stats.norm.pdf(x_values, mean, std_dev)

    # Plot the histogram of the data
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=10, density=True, alpha=0.6, color='g', edgecolor='black', label='Data Histogram')

    # Plot the normal distribution curve
    plt.plot(x_values, y_values, 'r-', lw=2, label=f'Normal Distribution\n$\mu$={mean:.2f}, $\sigma$={std_dev:.2f}')
    
    # Add labels and title
    plt.xlabel('Data Values')
    plt.ylabel('Density')
    plt.title('Normal Distribution Visualization')
    plt.legend()

    # Show the plot
    plt.show()

def main():
    # User input for dataset
    sample_size = int(input("Enter the sample size: "))
    data = list(map(float, input(f"Enter {sample_size} data values (comma-separated): ").split(',')))

    if len(data) != sample_size:
        print("Error: The number of data values does not match the sample size.")
    else:
        visualize_normal_distribution(data)

if __name__ == "__main__":
    main()
