import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from collections import Counter

def calculate_descriptive_statistics(data):
    # Convert data to a NumPy array for easier calculations
    data = np.array(data)
    
    # Calculate the required descriptive statistics
    mean = np.mean(data)
    median = np.median(data)
    mode = stats.mode(data)[0][0]
    variance = np.var(data, ddof=1)
    std_dev = np.std(data, ddof=1)
    data_range = np.ptp(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    
    # Display the results
    print("Descriptive Statistics:")
    print(f"Mean: {mean}")
    print(f"Median: {median}")
    print(f"Mode: {mode}")
    print(f"Variance: {variance}")
    print(f"Standard Deviation: {std_dev}")
    print(f"Range: {data_range}")
    print(f"Q1 (25th percentile): {q1}")
    print(f"Q3 (75th percentile): {q3}")
    print(f"Interquartile Range (IQR): {iqr}")
    
    return mean, median, mode, variance, std_dev, data_range, q1, q3, iqr

def plot_histogram(data):
    plt.figure(figsize=(10, 6))
    sns.histplot(data, bins=10, kde=True, color='blue', edgecolor='black')
    plt.title('Histogram')
    plt.xlabel('Data Values')
    plt.ylabel('Frequency')
    plt.show()

def plot_boxplot(data):
    plt.figure(figsize=(8, 6))
    sns.boxplot(data, color='orange')
    plt.title('Box Plot')
    plt.xlabel('Data Values')
    plt.show()

def main():
    # User input for dataset
    sample_size = int(input("Enter the number of data points: "))
    data = list(map(float, input(f"Enter {sample_size} data values (comma-separated): ").split(',')))
    
    if len(data) != sample_size:
        print("Error: The number of data values does not match the specified sample size.")
        return
    
    # Calculate descriptive statistics
    stats = calculate_descriptive_statistics(data)
    
    # Visualize the data
    plot_histogram(data)
    plot_boxplot(data)

if __name__ == "__main__":
    main()
