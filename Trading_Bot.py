import pandas as pd
import numpy as np
import ta
import sys
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from ta import add_all_ta_features
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from datetime import datetime, timedelta

import yfinance as yf
ticker = sys.argv[1]
timeframe=sys.argv[2] 



end=datetime.today()
if timeframe=="1d":
    start=end-timedelta(days=30)
elif timeframe=="5d":
    start=end-timedelta(days=30)
elif timeframe=="1mo":
    start=end-timedelta(days=30)
elif timeframe=="3mo":
    start=end-timedelta(days=90)
elif timeframe=="6mo":
    start=end-timedelta(days=180)
elif timeframe=="1y":
    start=end-timedelta(days=365)
else:
    start = end - timedelta(days=30)  # default to 1 month

start_str=start.strftime('%Y-%m-%d')
end_str=end.strftime('%Y-%m-%d')


df = yf.download(ticker,start=start_str,end =end_str, auto_adjust=True)
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

if df.empty:
    raise ValueError("Data download failed. Check ticker symbol or date range.")

# Optional: View available columns
#print("Columns:", df.columns.tolist())

# Ensure 1D input
close_series = df['Close'].squeeze()  # Or df['Close'].iloc[:, 0] if needed
rsi = RSIIndicator(close=close_series, window=14)
df['RSI'] = rsi.rsi()

close_series = df['Close'].squeeze()
sma=SMAIndicator(close=close_series,window=20)
df['SMA']=sma.sma_indicator()

close_series = df['Close'].squeeze()
macd=MACD(close=close_series)
df['MACD_Signal']=macd.macd_signal()
df['MACD']=macd.macd()

close_series = df['Close'].squeeze()
bf=BollingerBands(close=close_series,window=20,window_dev=2)
df['BollingerBands_high']=bf.bollinger_hband()
df['BollingerBands_low']=bf.bollinger_lband()

# Clean before ATR calculation

atr = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close'], window=14)
df['ATR'] = atr.average_true_range()

start_str=start.strftime('%Y-%m-%d')
end_str=end.strftime('%Y-%m-%d')
df['Future_Close'] = df['Close'].shift(-5)
df['Target'] = (df['Future_Close'] > df['Close']).astype(int)


Features=['SMA','RSI','ATR','BollingerBands_high','BollingerBands_low','High','Low','Close','Future_Close','MACD_Signal','MACD']
x=df[Features]
y=df['Target'].loc[x.index]



model=XGBClassifier()
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,shuffle=False)
model.fit(x_train,y_train)
y_pred=model.predict(x_test)

result = "BUY" if y_pred[-1] == 1 else "SELL"
print(result,flush=True)