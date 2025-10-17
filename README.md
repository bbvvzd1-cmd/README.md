# 💰 Streamlit Crypto Dashboard

A real-time cryptocurrency dashboard built with Streamlit that displays live prices, historical charts, and market data for multiple cryptocurrencies.

## Features

- 📊 **Real-time Price Data**: Live cryptocurrency prices with 24-hour changes
- 📈 **Interactive Charts**: Historical price charts with Plotly visualization
- 🔄 **Auto-refresh**: Optional 30-second auto-refresh for live updates
- 💹 **Multiple Cryptocurrencies**: Support for Bitcoin, Ethereum, BNB, Cardano, Solana, Polkadot, Dogecoin, and Ripple
- 🌍 **Multi-currency Support**: View prices in USD, EUR, GBP, or JPY
- 📉 **Historical Data**: View price trends for 24h, 7d, 30d, 90d, or 1 year
- 📊 **Market Metrics**: Market cap and 24-hour volume information
- 📋 **Comparison Table**: Side-by-side comparison of selected cryptocurrencies

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bbvvzd1-cmd/README.md.git
cd README.md
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`.

## Dashboard Overview

### Sidebar Controls
- **Select Cryptocurrencies**: Choose which cryptocurrencies to display
- **Time Range**: Select historical data period (24h to 1 year)
- **Currency**: Choose display currency (USD, EUR, GBP, JPY)
- **Auto Refresh**: Enable automatic 30-second refresh

### Main Dashboard
- **Price Metrics**: Current price, 24h change, market cap, and volume
- **Price History Charts**: Interactive Plotly charts showing price trends
- **Statistics**: Current price, high, low, and percentage change
- **Comparison Table**: Tabular view of all selected cryptocurrencies

## Data Source

This dashboard uses the [CoinGecko API](https://www.coingecko.com/en/api) to fetch cryptocurrency data. The API is free and doesn't require authentication for basic usage.

## Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive charting library
- **Requests**: HTTP library for API calls
- **CoinGecko API**: Cryptocurrency data provider

## Screenshots

The dashboard displays:
- Real-time cryptocurrency prices with percentage changes
- Interactive price charts with zoom and pan capabilities
- Market statistics including market cap and trading volume
- Responsive layout that works on different screen sizes

## Requirements

- Python 3.8+
- streamlit >= 1.28.0
- pandas >= 2.0.0
- requests >= 2.31.0
- plotly >= 5.17.0

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is open source and available under the MIT License.

## Disclaimer

This dashboard is for informational purposes only. Cryptocurrency investments are subject to high market risk. Always do your own research before making investment decisions.