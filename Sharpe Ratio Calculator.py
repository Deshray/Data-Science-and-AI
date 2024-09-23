import yfinance as yf
import numpy as np

# Sharpe Ratio calculation
def sharpe_ratio():
    stock = input("Enter the stock symbol (e.g., AAPL, MSFT): ")
    risk_free_rate = float(input("Enter the risk-free rate (as a decimal, e.g., 0.05 for 5%): "))

    # Fetch stock data
    data = yf.download(stock, start="2020-01-01", end="2023-12-31")['Adj Close']

    # Calculate daily returns
    daily_returns = data.pct_change().dropna()

    # Calculate excess returns (returns - risk-free rate)
    excess_returns = daily_returns.mean() - risk_free_rate / 252  # Adjust for daily return

    # Calculate Sharpe ratio
    sharpe_ratio_value = excess_returns / daily_returns.std()

    print(f"Sharpe Ratio for {stock}: {sharpe_ratio_value:.2f}")

# Call the function to execute
sharpe_ratio()
