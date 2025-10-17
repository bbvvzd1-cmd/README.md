import pandas as pd
import ta

data = [1,2,3,4,5,6,7,8,9,10]
series = pd.Series(data)
rsi = ta.momentum.RSIIndicator(series, window=3).rsi()
print("RSI:", rsi.tolist())
