import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Crypto Dashboard Demo",
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
st.title("💰 Cryptocurrency Dashboard (Demo Mode)")
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

st.sidebar.info("ℹ️ Demo Mode: Displaying mock data for demonstration purposes")

# Mock data generation
def generate_mock_price_data(crypto_name):
    """Generate mock current price data"""
    base_prices = {
        "Bitcoin": 67500.00,
        "Ethereum": 3800.00,
        "Binance Coin": 595.00,
        "Cardano": 0.58,
        "Solana": 165.00,
        "Polkadot": 7.50,
        "Dogecoin": 0.15,
        "Ripple": 0.52
    }
    
    price = base_prices.get(crypto_name, 100.00)
    change_24h = np.random.uniform(-8, 8)
    market_cap = price * np.random.uniform(10_000_000, 100_000_000)
    volume_24h = market_cap * np.random.uniform(0.05, 0.15)
    
    return {
        "price": price,
        "change_24h": change_24h,
        "market_cap": market_cap,
        "volume_24h": volume_24h
    }

def generate_historical_data(crypto_name, days=7):
    """Generate mock historical data"""
    base_prices = {
        "Bitcoin": 67500.00,
        "Ethereum": 3800.00,
        "Binance Coin": 595.00,
        "Cardano": 0.58,
        "Solana": 165.00,
        "Polkadot": 7.50,
        "Dogecoin": 0.15,
        "Ripple": 0.52
    }
    
    base_price = base_prices.get(crypto_name, 100.00)
    
    # Generate time series
    if days <= 1:
        points = 24
        freq = 'H'
    elif days <= 7:
        points = days * 24
        freq = 'H'
    else:
        points = days
        freq = 'D'
    
    dates = pd.date_range(end=datetime.now(), periods=points, freq=freq)
    
    # Generate realistic price movements
    np.random.seed(hash(crypto_name) % 2**32)
    returns = np.random.normal(0.0005, 0.02, points)
    prices = base_price * np.exp(np.cumsum(returns))
    
    df = pd.DataFrame({
        'timestamp': dates,
        'price': prices
    })
    
    return df

# Map time range to days
time_range_map = {
    "24h": 1,
    "7d": 7,
    "30d": 30,
    "90d": 90,
    "1y": 365
}

# Main content
if not selected_cryptos:
    st.warning("Please select at least one cryptocurrency from the sidebar.")
else:
    # Create columns for metrics
    cols = st.columns(len(selected_cryptos))
    
    # Display current prices and metrics
    for idx, crypto_name in enumerate(selected_cryptos):
        with cols[idx]:
            data = generate_mock_price_data(crypto_name)
            
            # Display metric
            st.metric(
                label=crypto_name,
                value=f"{currency.upper()} {data['price']:,.2f}",
                delta=f"{data['change_24h']:.2f}%"
            )
            
            st.caption(f"Market Cap: {currency.upper()} {data['market_cap']:,.0f}")
            st.caption(f"24h Volume: {currency.upper()} {data['volume_24h']:,.0f}")
    
    st.markdown("---")
    
    # Display price charts
    st.subheader(f"Price History ({time_range})")
    
    for crypto_name in selected_cryptos:
        with st.expander(f"{crypto_name} Chart", expanded=True):
            df = generate_historical_data(
                crypto_name, 
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
        data = generate_mock_price_data(crypto_name)
        
        comparison_data.append({
            "Cryptocurrency": crypto_name,
            f"Price ({currency.upper()})": f"{data['price']:,.2f}",
            "24h Change (%)": f"{data['change_24h']:.2f}%",
            f"Market Cap ({currency.upper()})": f"{data['market_cap']:,.0f}",
            f"24h Volume ({currency.upper()})": f"{data['volume_24h']:,.0f}"
        })
    
    if comparison_data:
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Demo Mode with Mock Data")
