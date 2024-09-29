from scipy.optimize import linprog

# Input: number of appliances
num_appliances = int(input("Enter number of appliances: "))

# Input: energy consumption and tariffs for each appliance
energy_consumption = []
tariffs = []

for i in range(num_appliances):
    consumption = float(input(f"Enter energy consumption (kWh) for appliance {i+1}: "))
    tariff = float(input(f"Enter cost per kWh for appliance {i+1}: "))
    energy_consumption.append(consumption)
    tariffs.append(tariff)

# Set up the linear programming problem to minimize total energy cost
c = tariffs  # Minimize the cost function (tariffs)
A_eq = [energy_consumption]  # Total energy consumption constraint
b_eq = [sum(energy_consumption)]  # Energy requirement

# Bounds for each appliance's usage (between 0 and max 24 hours in a day)
bounds = [(0, 24) for _ in range(num_appliances)]

# Solve the linear programming problem
result = linprog(c=c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

# Output the optimal usage times if a solution is found
if result.success:
    print("\nOptimal usage times (hours):")
    for i, usage in enumerate(result.x):
        print(f"Appliance {i+1}: {usage:.2f} hours")
else:
    print("No feasible solution found.")
