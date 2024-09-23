import yfinance as yf
import numpy as np

# Function to calculate historical VaR
def calculate_var():
    stock = input("Enter the stock symbol (e.g., AAPL, MSFT): ")
    confidence_level = float(input("Enter the confidence level (e.g., 0.95 for 95%): "))

    # Fetch stock data
    data = yf.download(stock, start="2020-01-01", end="2023-12-31")['Adj Close']

    # Calculate daily returns
    daily_returns = data.pct_change().dropna()

    # Calculate the portfolio's VaR
    var = np.percentile(daily_returns, (1 - confidence_level) * 100)

    print(f"VaR at {confidence_level * 100}% confidence level for {stock}: {var * 100:.2f}%")

# Call the function to execute
calculate_var()
