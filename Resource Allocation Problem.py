import numpy as np
from scipy.optimize import linprog

# Get number of tasks and resources from the user
num_tasks = int(input("Enter number of tasks to allocate resources to: "))
num_resources = int(input("Enter number of available resources: "))

# Input productivity for each task
productivity = []
for i in range(num_tasks):
    value = float(input(f"Enter productivity for task {i+1}: "))
    productivity.append(value)

# Input resource usage for each task
resource_constraints = []
for i in range(num_resources):
    resource = []
    for j in range(num_tasks):
        amount = float(input(f"Enter resource {i+1} required for task {j+1}: "))
        resource.append(amount)
    resource_constraints.append(resource)

# Input available resources
available_resources = []
for i in range(num_resources):
    available = float(input(f"Enter available amount of resource {i+1}: "))
    available_resources.append(available)

# Solve the optimization problem using linprog
result = linprog(c=-np.array(productivity), A_ub=resource_constraints, b_ub=available_resources, method='highs')

# Output the optimal allocation if a solution exists
if result.success:
    print("\nOptimal resource allocation:")
    for i, allocation in enumerate(result.x):
        print(f"Task {i+1}: {allocation} units")
    print(f"Maximized Productivity: {-result.fun}")
else:
    print("No feasible solution found.")
