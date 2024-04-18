import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import yfinance as yf

meta = yf.Ticker("META")
meta_hist = meta.history(period="1mo")
print(meta_hist)


def calculate_RMSE(y_pred, y_true):
    return np.sqrt(np.mean(y_pred - y_true) ** 2)

