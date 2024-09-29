import itertools
import numpy as np

# Calculate total distance of a route
def calculate_total_distance(route, distance_matrix):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i+1]]
    total_distance += distance_matrix[route[-1]][route[0]]  # Returning to the start
    return total_distance

# Get number of cities and distance matrix from the user
num_cities = int(input("Enter number of cities: "))
distance_matrix = np.zeros((num_cities, num_cities))

for i in range(num_cities):
    for j in range(i + 1, num_cities):
        distance = float(input(f"Enter distance between city {i+1} and city {j+1}: "))
        distance_matrix[i][j] = distance_matrix[j][i] = distance

# Generate all possible routes
cities = list(range(num_cities))
all_routes = itertools.permutations(cities)

# Find the shortest route
best_route = None
min_distance = float('inf')

for route in all_routes:
    distance = calculate_total_distance(route, distance_matrix)
    if distance < min_distance:
        min_distance = distance
        best_route = route

# Output the optimal route and minimum distance
print(f"\nThe optimal route is: {best_route}")
print(f"Minimum distance traveled: {min_distance}")
