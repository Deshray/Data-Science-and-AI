import matplotlib.pyplot as plt

# Arithmetic sequence functions
def arithmetic_nth_term(a, d, n):
    return a + (n - 1) * d

def arithmetic_sum(a, d, n):
    return (n / 2) * (2 * a + (n - 1) * d)

# Geometric sequence functions
def geometric_nth_term(a, r, n):
    return a * (r ** (n - 1))

def geometric_sum(a, r, n):
    if r == 1:
        return a * n
    else:
        return a * (1 - r ** n) / (1 - r)

# Function to plot sequences
def plot_sequence(sequence, title):
    plt.figure(figsize=(10, 6))
    plt.plot(sequence, marker='o')
    plt.title(title)
    plt.xlabel('n (Term number)')
    plt.ylabel('Value')
    plt.grid(True)
    plt.show()

# Main function to run the analyzer
def main():
    print("Sequence and Series Analyzer")
    print("1. Arithmetic Sequence")
    print("2. Geometric Sequence")
    choice = input("Choose the type of sequence: ")

    if choice == '1':
        a = float(input("Enter the first term (a): "))
        d = float(input("Enter the common difference (d): "))
        n = int(input("Enter the number of terms (n): "))

        # Calculate nth term and sum of the first n terms
        nth_term = arithmetic_nth_term(a, d, n)
        series_sum = arithmetic_sum(a, d, n)

        # Generate and plot the sequence
        sequence = [arithmetic_nth_term(a, d, i) for i in range(1, n + 1)]
        plot_sequence(sequence, "Arithmetic Sequence")

        print(f"The {n}th term of the arithmetic sequence is: {nth_term}")
        print(f"The sum of the first {n} terms of the arithmetic sequence is: {series_sum}")

    elif choice == '2':
        a = float(input("Enter the first term (a): "))
        r = float(input("Enter the common ratio (r): "))
        n = int(input("Enter the number of terms (n): "))

        # Calculate nth term and sum of the first n terms
        nth_term = geometric_nth_term(a, r, n)
        series_sum = geometric_sum(a, r, n)

        # Generate and plot the sequence
        sequence = [geometric_nth_term(a, r, i) for i in range(1, n + 1)]
        plot_sequence(sequence, "Geometric Sequence")

        print(f"The {n}th term of the geometric sequence is: {nth_term}")
        print(f"The sum of the first {n} terms of the geometric sequence is: {series_sum}")

    else:
        print("Invalid choice! Please select either 1 or 2.")

if __name__ == "__main__":
    main()
