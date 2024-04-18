import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 假设我们的分析窗口是过去一年
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

tickers = ['META', 'AAPL', 'NVDA']

# 使用yfinance批量下载数据
data = yf.download(tickers, start=start_date, end=end_date)

# 计算简单的日收益率
daily_returns = data['Adj Close'].pct_change().dropna()

# 假设的市值数据，实际中应该从某处获取
market_values = {'AAPL': 2.68, 'META': 1.27, 'NVDA': 2.21}

# 假设的账目市值比数据，实际中应该从某处获取或计算
book_to_market_ratio = {'AAPL': 26.86, 'META': 32.5, 'NVDA': '73.59'}

# 构建DataFrame以方便操作
stocks_df = pd.DataFrame({
    'MarketValue': market_values,
    'BookToMarketRatio': book_to_market_ratio
})

# 为了与原策略保持一致，这里仅展示如何进行市值加权的收益率计算，不涉及原策略中的分类逻辑
def market_value_weighted_returns(returns, weights):
    """
    计算市值加权的收益率。
    :param returns: pd.DataFrame, 每只股票的日收益率
    :param weights: pd.Series, 每只股票的市值权重
    :return: 加权收益率
    """
    weighted_returns = returns.multiply(weights)
    portfolio_returns = weighted_returns.sum(axis=1) / weights.sum()
    return portfolio_returns

# 计算市值加权的组合收益率
portfolio_returns = market_value_weighted_returns(daily_returns, stocks_df['MarketValue'])

# 假设简单的投资组合表现计算（例如年化收益率）
annualized_portfolio_return = (1 + portfolio_returns).prod() ** (365 / portfolio_returns.shape[0]) - 1
print("年化组合收益率:", annualized_portfolio_return)

