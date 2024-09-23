import numpy as np
import yfinance as yf

# Function to calculate European Call Option price using Binomial Tree
def european_call_option_binomial():
    # User input for stock symbol
    stock_symbol = input("Enter stock name (e.g., AAPL): ")
    
    # Fetch historical stock price data
    data = yf.download(stock_symbol, start="2023-01-01", end="2023-12-31")['Adj Close']
    
    # Get the last price as S0
    S0 = data.iloc[-1]
    print(f"Initial stock price (S0) is: ${S0:.2f}")

    # Parameters
    K = float(input("Enter the strike price (K): "))  # Strike price
    T = float(input("Enter the time to maturity (in years, e.g., 1 for 1 year): "))  # Time to maturity
    r = float(input("Enter the risk-free rate (as a decimal, e.g., 0.05 for 5%): "))  # Risk-free rate
    sigma = float(input("Enter the volatility (as a decimal, e.g., 0.2 for 20%): "))  # Volatility
    n_steps = int(input("Enter the number of time steps (e.g., 3): "))  # Number of time steps

    # Calculate time step size
    dt = T / n_steps

    # Calculate up and down factors
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u

    # Calculate risk-neutral probabilities
    p = (np.exp(r * dt) - d) / (u - d)

    # Initialize stock price tree
    stock_tree = np.zeros((n_steps + 1, n_steps + 1))
    stock_tree[0, 0] = S0

    # Build the stock price tree
    for i in range(1, n_steps + 1):
        stock_tree[i, 0] = stock_tree[i - 1, 0] * u
        for j in range(1, i + 1):
            stock_tree[i, j] = stock_tree[i - 1, j - 1] * d

    # Calculate the option payoff at maturity
    option_tree = np.maximum(0, stock_tree[-1, :] - K)

    # Backward induction to calculate option price
    for i in range(n_steps - 1, -1, -1):
        for j in range(i + 1):
            option_tree[j] = np.exp(-r * dt) * (p * option_tree[j] + (1 - p) * option_tree[j + 1])

    print(f"European Call Option Price using Binomial Tree: ${option_tree[0]:.2f}")

# Run the function
european_call_option_binomial()
