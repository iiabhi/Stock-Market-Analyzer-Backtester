# 📈 Stock Market Analyzer & Backtester

This Streamlit web application allows users to analyze historical stock data, apply technical indicators like **SMA**, **EMA**, **RSI**, and **MACD**, and backtest basic trading strategies. It supports **Indian (NSE)** and **US stocks**, and provides useful visualizations and performance metrics.

---

## 🚀 Features

- ✅ Real-time and historical stock data using **Yahoo Finance**
- ✅ Choose from popular tickers (TCS, INFY, RELIANCE, AAPL, TSLA, etc.)
- ✅ Apply technical indicators:
  - SMA (Simple Moving Average)
  - EMA (Exponential Moving Average)
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
- ✅ Visual charts and graphs
- ✅ Backtest a basic crossover strategy
- ✅ Shows ROI, win/loss ratio, and trade log

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Backend:** Python 3.13+
- **Libraries:**
  - `yfinance`
  - `pandas`, `numpy`, `matplotlib`
  - `pandas_ta` (for indicators)
  - `ta-lib` (optional)
  - `streamlit`

---

## 📦 Installation (Local)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stock-market-analyzer-backtester.git
   cd stock-market-analyzer-backtester

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
3. Run the app:
   ```bash
   streamlit run app/streamlit_app.py


💡 Example Workflow
1. Select a stock (e.g., AAPL)
2. Choose the date range
3. Enable technical indicators
4. Analyze price charts and strategy
5. Run backtest to view:
6. ROI
7. Win/loss ratio
8. Trade history

## Screenshots:
### 📌 Dashboard
<img width="1470" height="956" alt="Screenshot 2025-08-07 at 12 46 25 AM" src="https://github.com/user-attachments/assets/29aaad43-5736-4d6c-86ae-48500b0cf88e" />


### 📈 Stock Chart with Indicators
<img width="1470" height="956" alt="Screenshot 2025-08-07 at 12 46 51 AM" src="https://github.com/user-attachments/assets/9f902434-d4ff-479d-9f17-e3df8cbb57ae" />


### 📊 Backtest Result

<img width="1470" height="956" alt="Screenshot 2025-08-07 at 12 46 33 AM" src="https://github.com/user-attachments/assets/034dce5f-ad18-4409-a6b1-9f0c6987a80e" />


📧 Contact
Made with ❤️ by Abhishek Kumar @iiabhi
