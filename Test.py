import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_stock_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)
    return data['Adj Close']


end_date = datetime.now()
start_date = end_date - timedelta(days=365)
tickers = ['META', 'NVDA', 'AAPL']
stock_data = get_stock_data(tickers, start_date, end_date)
prices = stock_data['AAPL']

def moving_average_crossover_strategy(prices, short_window, long_window):
    signals = pd.DataFrame(index=prices.index)
    signals['signal'] = 0.0
    signals['short_mavg'] = prices.rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = prices.rolling(window=long_window, min_periods=1, center=False).mean()
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
    signals['positions'] = signals['signal'].diff()
    return signals


short_window = 40
long_window = 100
signals = moving_average_crossover_strategy(prices, short_window, long_window)
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(prices.index, prices, label='NVDA Price')
ax.plot(signals.index, signals['short_mavg'], label=f'Short {short_window} days Mavg')
ax.plot(signals.index, signals['long_mavg'], label=f'Long {long_window} days Mavg')
ax.plot(signals.loc[signals.positions == 1.0].index, signals.short_mavg[signals.positions == 1.0], '^', markersize=10, color='g', label='Buy Signal')
ax.plot(signals.loc[signals.positions == -1.0].index, signals.short_mavg[signals.positions == -1.0], 'v', markersize=10, color='r', label='Sell Signal')
plt.title('AAPL Moving Average Crossover Strategy')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
