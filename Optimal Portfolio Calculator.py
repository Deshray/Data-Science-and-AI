import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate the efficient frontier
def efficient_frontier():
    # User input for stock symbols
    stocks = input("Enter the stock symbols (comma-separated, e.g., 'AAPL, MSFT, TSLA'): ").split(',')
    stocks = [stock.strip().upper() for stock in stocks]

    # User input for the number of portfolios to simulate
    num_portfolios = int(input("Enter the number of portfolios to simulate (e.g., 10000): "))

    # Fetch stock data from Yahoo Finance
    data = yf.download(stocks, start="2020-01-01", end="2023-12-31")['Adj Close']

    # Calculate daily returns
    returns = data.pct_change().mean() * 252  # Annualized average returns

    # Calculate covariance matrix of stock returns
    cov_matrix = data.pct_change().cov() * 252

    # Initialize variables
    num_assets = len(stocks)
    results = np.zeros((3, num_portfolios))

    # Simulate random portfolios
    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)

        portfolio_return = np.dot(weights, returns)
        portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
        portfolio_std_dev = np.sqrt(portfolio_variance)

        results[0,i] = portfolio_return
        results[1,i] = portfolio_std_dev
        results[2,i] = portfolio_return / portfolio_std_dev  # Sharpe ratio

    # Plot efficient frontier
    plt.scatter(results[1,:], results[0,:], c=results[2,:], cmap='viridis')
    plt.title('Efficient Frontier')
    plt.xlabel('Risk (Standard Deviation)')
    plt.ylabel('Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.show()

# Run the function
efficient_frontier()
