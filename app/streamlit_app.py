import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from modules.strategy import compute_indicators, apply_signals, backtest_strategy
import datetime

st.set_page_config(page_title="📊 Stock Market Analyzer", layout="wide")
st.title("📈 Stock Market Analyzer & Backtester")

# --- Inputs ---
ticker_list = [
    # 🇮🇳 Indian Stocks (NSE)
    'TCS.NS', 'INFY.NS', 'RELIANCE.NS', 'HDFCBANK.NS', 'ICICIBANK.NS',
    'KOTAKBANK.NS', 'SBIN.NS', 'AXISBANK.NS', 'ITC.NS', 'LT.NS',
    'BAJFINANCE.NS', 'BHARTIARTL.NS', 'HINDUNILVR.NS', 'ASIANPAINT.NS', 'ULTRACEMCO.NS',
    'MARUTI.NS', 'TITAN.NS', 'SUNPHARMA.NS', 'WIPRO.NS', 'DRREDDY.NS',
    'ADANIENT.NS', 'ADANIGREEN.NS', 'ONGC.NS', 'POWERGRID.NS', 'HCLTECH.NS',

    # 🇺🇸 US Stocks
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
    'META', 'NVDA', 'NFLX', 'INTC', 'AMD',
    'BABA', 'PYPL', 'BRK-B', 'JPM', 'V',
    'MA', 'WMT', 'COST', 'PEP', 'KO',
    'XOM', 'CVX', 'BA', 'PFE', 'JNJ'
]

ticker = st.selectbox("Select Stock Ticker", ticker_list)

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.date(2022, 1, 1))
with col2:
    end_date = st.date_input("End Date", datetime.date(2024, 1, 1))

indicators = st.multiselect("Select Indicators", ['SMA','EMA','RSI'], default=['SMA','EMA','RSI'])

if st.button("🔍 Run Strategy Backtest"):
    st.info("Fetching data and running backtest...")
    df = yf.download(ticker, start=start_date, end=end_date)
    if df.empty:
        st.error("No data found for the given ticker and date range.")
        st.stop()

    # Compute and apply
    df = compute_indicators(df)
    if 'RSI' in indicators:
        import pandas_ta as ta
        df['RSI'] = ta.rsi(df['Close'], length=14)
    df = apply_signals(df)
    results = backtest_strategy(df)

    # Ensure numeric types
    roi = float(results.get('ROI', 0))
    win_rate = float(results.get('Win Rate', 0))
    trade_count = int(results.get('Count', 0))

    # Display metrics
    st.subheader("📊 Strategy Performance")
    st.metric("ROI", f"{roi:.2f}%")
    st.metric("Win Rate", f"{win_rate:.2f}%")
    st.metric("Number of Trades", trade_count)

    # Trade history
    st.subheader("📜 Trade History")
    trades = results.get('Trades', [])
    if trades:
        for action, date, price, qty in trades:
            st.markdown(f"- **{action}** {qty} shares @ ₹{price:.2f} on {date.date()}")
    else:
        st.info("No trades executed in this strategy.")

    # Price chart
    st.subheader("📈 Price Chart with Indicators")
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(df['Close'], label='Close')
    if 'SMA' in indicators: ax.plot(df['SMA_20'], label='SMA 20')
    if 'EMA' in indicators: ax.plot(df['EMA_20'], label='EMA 20')
    ax.legend(); ax.grid(); st.pyplot(fig)

    # RSI chart
    if 'RSI' in indicators:
        st.subheader("📉 RSI Chart")
        fig2, ax2 = plt.subplots(figsize=(12,4))
        ax2.plot(df['RSI'], label='RSI', color='orange')
        ax2.axhline(70, color='red', linestyle='--'); ax2.axhline(30, color='green', linestyle='--')
        ax2.legend(); ax2.grid(); st.pyplot(fig2)
