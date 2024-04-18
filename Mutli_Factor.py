import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

tickers = ['META', 'AAPL', 'NVDA']
data = yf.download(tickers, start=start_date, end=end_date)
daily_returns = data['Adj Close'].pct_change().dropna()
market_values = {'AAPL': 2.68, 'META': 1.27, 'NVDA': 2.21}
book_to_market_ratio = {'AAPL': 26.86, 'META': 32.5, 'NVDA': '73.59'}

stocks_df = pd.DataFrame({
    'MarketValue': market_values,
    'BookToMarketRatio': book_to_market_ratio
})

def market_value_weighted_returns(returns, weights):
    weighted_returns = returns.multiply(weights)
    portfolio_returns = weighted_returns.sum(axis=1) / weights.sum()
    return portfolio_returns

portfolio_returns = market_value_weighted_returns(daily_returns, stocks_df['MarketValue'])

annualized_portfolio_return = (1 + portfolio_returns).prod() ** (365 / portfolio_returns.shape[0]) - 1
print("Annualized portfolio return", annualized_portfolio_return)

