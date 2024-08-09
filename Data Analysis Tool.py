import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to read the CSV file
def read_csv(file_path):
    return pd.read_csv(file_path)

# Function to perform basic statistical analysis
def basic_statistics(data):
    print("Basic Statistics:")
    print(data.describe())
    print("\nCorrelation Matrix:")
    print(data.corr())

# Function to plot histograms
def plot_histogram(data, column):
    plt.figure(figsize=(10, 6))
    sns.histplot(data[column], kde=True)
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()

# Function to plot scatter plot
def plot_scatter(data, column1, column2):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=data[column1], y=data[column2])
    plt.title(f'Scatter Plot of {column1} vs {column2}')
    plt.xlabel(column1)
    plt.ylabel(column2)
    plt.show()

# Function to plot box plot
def plot_boxplot(data, column):
    plt.figure(figsize=(10, 6))
    sns.boxplot(y=data[column])
    plt.title(f'Box Plot of {column}')
    plt.ylabel(column)
    plt.show()

# Main function to run the tool
def main():
    file_path = input("Enter the path to the CSV file: ")
    data = read_csv(file_path)
    
    print("\nColumns in the dataset:")
    print(data.columns.tolist())

    basic_statistics(data)
    
    while True:
        print("\nChoose a plot type:")
        print("1. Histogram")
        print("2. Scatter Plot")
        print("3. Box Plot")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            column = input("Enter the column name for histogram: ")
            if column in data.columns:
                plot_histogram(data, column)
            else:
                print("Column not found!")
                
        elif choice == '2':
            column1 = input("Enter the first column name for scatter plot: ")
            column2 = input("Enter the second column name for scatter plot: ")
            if column1 in data.columns and column2 in data.columns:
                plot_scatter(data, column1, column2)
            else:
                print("One or both columns not found!")
                
        elif choice == '3':
            column = input("Enter the column name for box plot: ")
            if column in data.columns:
                plot_boxplot(data, column)
            else:
                print("Column not found!")
                
        elif choice == '4':
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
