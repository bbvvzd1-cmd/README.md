import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="Crypto Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("💰 Cryptocurrency Dashboard")
st.markdown("---")

# Sidebar
st.sidebar.header("Settings")

# Cryptocurrency selection
crypto_options = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Binance Coin": "binancecoin",
    "Cardano": "cardano",
    "Solana": "solana",
    "Polkadot": "polkadot",
    "Dogecoin": "dogecoin",
    "Ripple": "ripple"
}

selected_cryptos = st.sidebar.multiselect(
    "Select Cryptocurrencies",
    options=list(crypto_options.keys()),
    default=["Bitcoin", "Ethereum"]
)

# Time range selection
time_range = st.sidebar.selectbox(
    "Time Range",
    options=["24h", "7d", "30d", "90d", "1y"],
    index=1
)

# Currency selection
currency = st.sidebar.selectbox(
    "Currency",
    options=["usd", "eur", "gbp", "jpy"],
    index=0
)

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)", value=False)

# Helper function to fetch crypto data
@st.cache_data(ttl=30)
def fetch_crypto_price(crypto_id, currency="usd"):
    """Fetch current cryptocurrency price and data"""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": crypto_id,
            "vs_currencies": currency,
            "include_24hr_change": "true",
            "include_24hr_vol": "true",
            "include_market_cap": "true"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching data for {crypto_id}: {str(e)}")
        return None

@st.cache_data(ttl=300)
def fetch_historical_data(crypto_id, currency="usd", days="7"):
    """Fetch historical cryptocurrency data"""
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
        params = {
            "vs_currency": currency,
            "days": days,
            "interval": "hourly" if days in ["1", "7"] else "daily"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Convert to DataFrame
        df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        st.error(f"Error fetching historical data for {crypto_id}: {str(e)}")
        return None

# Map time range to days
time_range_map = {
    "24h": "1",
    "7d": "7",
    "30d": "30",
    "90d": "90",
    "1y": "365"
}

# Main content
if not selected_cryptos:
    st.warning("Please select at least one cryptocurrency from the sidebar.")
else:
    # Create columns for metrics
    cols = st.columns(len(selected_cryptos))
    
    # Display current prices and metrics
    for idx, crypto_name in enumerate(selected_cryptos):
        crypto_id = crypto_options[crypto_name]
        
        with cols[idx]:
            data = fetch_crypto_price(crypto_id, currency)
            
            if data and crypto_id in data:
                price = data[crypto_id].get(currency, 0)
                change_24h = data[crypto_id].get(f"{currency}_24h_change", 0)
                market_cap = data[crypto_id].get(f"{currency}_market_cap", 0)
                volume_24h = data[crypto_id].get(f"{currency}_24h_vol", 0)
                
                # Display metric
                st.metric(
                    label=crypto_name,
                    value=f"{currency.upper()} {price:,.2f}",
                    delta=f"{change_24h:.2f}%"
                )
                
                st.caption(f"Market Cap: {currency.upper()} {market_cap:,.0f}")
                st.caption(f"24h Volume: {currency.upper()} {volume_24h:,.0f}")
    
    st.markdown("---")
    
    # Display price charts
    st.subheader(f"Price History ({time_range})")
    
    for crypto_name in selected_cryptos:
        crypto_id = crypto_options[crypto_name]
        
        with st.expander(f"{crypto_name} Chart", expanded=True):
            df = fetch_historical_data(
                crypto_id, 
                currency, 
                time_range_map[time_range]
            )
            
            if df is not None and not df.empty:
                # Create interactive chart with Plotly
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df['price'],
                    mode='lines',
                    name=crypto_name,
                    line=dict(color='#1f77b4', width=2),
                    fill='tonexty',
                    fillcolor='rgba(31, 119, 180, 0.1)'
                ))
                
                fig.update_layout(
                    title=f"{crypto_name} Price Chart",
                    xaxis_title="Date",
                    yaxis_title=f"Price ({currency.upper()})",
                    hovermode='x unified',
                    template='plotly_white',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display statistics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Current", f"{df['price'].iloc[-1]:,.2f}")
                with col2:
                    st.metric("High", f"{df['price'].max():,.2f}")
                with col3:
                    st.metric("Low", f"{df['price'].min():,.2f}")
                with col4:
                    change = ((df['price'].iloc[-1] - df['price'].iloc[0]) / df['price'].iloc[0]) * 100
                    st.metric("Change", f"{change:.2f}%")
    
    # Comparison table
    st.markdown("---")
    st.subheader("Comparison Table")
    
    comparison_data = []
    for crypto_name in selected_cryptos:
        crypto_id = crypto_options[crypto_name]
        data = fetch_crypto_price(crypto_id, currency)
        
        if data and crypto_id in data:
            comparison_data.append({
                "Cryptocurrency": crypto_name,
                f"Price ({currency.upper()})": f"{data[crypto_id].get(currency, 0):,.2f}",
                "24h Change (%)": f"{data[crypto_id].get(f'{currency}_24h_change', 0):.2f}%",
                f"Market Cap ({currency.upper()})": f"{data[crypto_id].get(f'{currency}_market_cap', 0):,.0f}",
                f"24h Volume ({currency.upper()})": f"{data[crypto_id].get(f'{currency}_24h_vol', 0):,.0f}"
            })
    
    if comparison_data:
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Data provided by CoinGecko API")

# Auto-refresh functionality
if auto_refresh:
    time.sleep(30)
    st.rerun()
