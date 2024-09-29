# Get number of items from the user
num_items = int(input("Enter number of items: "))

# Input weight and value of each item
weights = []
values = []
for i in range(num_items):
    weight = int(input(f"Enter weight of item {i+1}: "))
    value = int(input(f"Enter value of item {i+1}: "))
    weights.append(weight)
    values.append(value)

# Input maximum capacity of the knapsack
capacity = int(input("Enter the maximum weight capacity of the knapsack: "))

# Create a DP table to solve the knapsack problem
dp = [[0 for _ in range(capacity + 1)] for _ in range(num_items + 1)]

# Fill the DP table
for i in range(1, num_items + 1):
    for w in range(1, capacity + 1):
        if weights[i - 1] <= w:
            dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
        else:
            dp[i][w] = dp[i - 1][w]

# Output the maximum value that can be placed in the knapsack
print(f"\nMaximum value in knapsack: {dp[num_items][capacity]}")
