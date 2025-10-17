import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Crypto Streamlit Dashboard", layout="wide")
st.title("📈 Crypto Market Dashboard (Binance, Live)")

@st.cache_data(ttl=60)
def fetch_binance_data(symbol="BTCUSDT", interval="1m", limit=100):
    url = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    resp = requests.get(url, params=params)
    data = resp.json()
    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close"] = df["close"].astype(float)
    return df

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
symbol = st.sidebar.selectbox("Select Symbol", symbols)
interval = st.sidebar.selectbox("Interval", ["1m", "5m", "15m", "1h", "4h", "1d"])
limit = st.sidebar.slider("Data Points", min_value=20, max_value=500, value=100)

df = fetch_binance_data(symbol, interval, limit)

st.subheader(f"{symbol} Price Chart")
st.line_chart(df.set_index("open_time")["close"])

st.write("Latest Prices:")
st.dataframe(df.tail(10)[["open_time", "close"]].rename(columns={"open_time": "Time", "close": "Close Price"}))

st.caption("Data from Binance. Updates every 60 seconds.")
