import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Logistic growth differential equation
def logistic_growth(P, t, r, K):
    return r * P * (1 - P / K)

# Solve the differential equation
def solve_logistic_growth(P0, r, K, t):
    P = odeint(logistic_growth, P0, t, args=(r, K))
    return P

# Plot the population growth
def plot_population_growth(t, P):
    plt.figure(figsize=(10, 6))
    plt.plot(t, P, label='Population Size')
    plt.title('Logistic Growth Model')
    plt.xlabel('Time')
    plt.ylabel('Population Size')
    plt.legend()
    plt.grid(True)
    plt.show()

# Main function to run the model
def main():
    # Initial population size
    P0 = float(input("Enter the initial population size (P0): "))
    
    # Intrinsic growth rate
    r = float(input("Enter the intrinsic growth rate (r): "))
    
    # Carrying capacity
    K = float(input("Enter the carrying capacity (K): "))
    
    # Time points where solution is computed
    t = np.linspace(0, 50, 500)
    
    # Solve the logistic growth differential equation
    P = solve_logistic_growth(P0, r, K, t)
    
    # Plot the population growth
    plot_population_growth(t, P)

if __name__ == "__main__":
    main()
