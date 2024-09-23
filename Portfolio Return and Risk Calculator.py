import yfinance as yf
import numpy as np

# Function to calculate portfolio return and risk
def portfolio_return_risk():
    # User input for stock symbols
    stocks = input("Enter the stock symbols (comma-separated, e.g., 'AAPL, MSFT, TSLA'): ").split(',')
    stocks = [stock.strip().upper() for stock in stocks]

    # User input for portfolio weights
    weights_input = input(f"Enter the portfolio weights for {len(stocks)} stocks (comma-separated, e.g., '0.5, 0.3, 0.2'): ")
    weights = list(map(float, weights_input.split(',')))

    if len(weights) != len(stocks):
        print("Error: The number of weights must match the number of stocks.")
        return

    # Normalize weights if they don't add up to 1
    if sum(weights) != 1:
        print("Note: Your weights don't add up to 1. They will be normalized.")
        weights = [w / sum(weights) for w in weights]

    # User input for date range
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    # Fetch stock data from Yahoo Finance
    data = yf.download(stocks, start=start_date, end=end_date)['Adj Close']

    # Calculate daily returns and annualize them
    returns = data.pct_change().mean() * 252  # Annualized average returns

    # Calculate covariance matrix of the stocks' returns
    cov_matrix = data.pct_change().cov() * 252  # Annualized covariance

    # Convert weights to numpy array
    weights = np.array(weights)

    # Calculate the portfolio's expected return
    portfolio_return = np.dot(weights, returns)

    # Calculate the portfolio's variance and risk (standard deviation)
    portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
    portfolio_std_dev = np.sqrt(portfolio_variance)

    # Display results
    print(f"\nExpected Portfolio Return: {portfolio_return * 100:.2f}%")
    print(f"Portfolio Risk (Standard Deviation): {portfolio_std_dev * 100:.2f}%")

# Run the function
portfolio_return_risk()
