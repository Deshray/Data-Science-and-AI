import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Function for Monte Carlo simulation of stock prices
def monte_carlo_simulation(stock, num_simulations=1000, num_days=252):
    # Fetch historical stock price data
    data = yf.download(stock, start="2020-01-01", end="2023-12-31")['Adj Close']
    
    # Get the last price and calculate daily returns
    last_price = data.iloc[-1]  # Using .iloc to avoid future warnings
    daily_returns = data.pct_change().dropna()

    # Calculate mean and standard deviation of daily returns
    mu = daily_returns.mean()
    sigma = daily_returns.std()

    # Create an array to hold simulation results
    simulations = np.zeros((num_simulations, num_days))

    for i in range(num_simulations):
        prices = np.zeros(num_days)
        prices[0] = last_price
        
        for t in range(1, num_days):
            prices[t] = prices[t - 1] * np.exp(np.random.normal(mu, sigma))  # Simulate price using geometric Brownian motion

        simulations[i, :] = prices

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(simulations.T, alpha=0.1)  # Transpose to plot each simulation
    plt.title(f'Monte Carlo Simulations for {stock}')
    plt.xlabel('Days')
    plt.ylabel('Price')
    plt.show()

# User input for stock symbol
stock = input("Enter stock name (e.g., AAPL): ")
monte_carlo_simulation(stock)
