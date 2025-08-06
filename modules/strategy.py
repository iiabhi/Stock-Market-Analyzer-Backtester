# modules/strategy.py

import pandas as pd
import numpy as np


def compute_indicators(df: pd.DataFrame, fast: int = 20, slow: int = 50, trend: int = 100) -> pd.DataFrame:
    """
    Compute moving averages for given windows and a longer trend filter.
    - fast, slow: for crossover strategy
    - trend: long-term SMA to filter trades
    """
    df = df.copy()
    df[f'SMA_{fast}'] = df['Close'].rolling(window=fast, min_periods=1).mean()
    df[f'SMA_{slow}'] = df['Close'].rolling(window=slow, min_periods=1).mean()
    df[f'SMA_{trend}'] = df['Close'].rolling(window=trend, min_periods=1).mean()
    df[f'EMA_{fast}'] = df['Close'].ewm(span=fast, adjust=False).mean()
    # RSI manually
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14, min_periods=1).mean()
    avg_loss = loss.rolling(window=14, min_periods=1).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    df['RSI'] = 100 - (100 / (1 + rs))
    return df


def apply_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate simple buy/sell signals based solely on SMA crossovers:
      - BUY when 20-day SMA crosses above 50-day SMA
      - SELL when 20-day SMA crosses below 50-day SMA
    """
    df = df.copy()
    df['Signal'] = 0
    # Identify crossovers
    buy = (df['SMA_20'] > df['SMA_50']) & (df['SMA_20'].shift(1) <= df['SMA_50'].shift(1))
    sell = (df['SMA_20'] < df['SMA_50']) & (df['SMA_20'].shift(1) >= df['SMA_50'].shift(1))
    df.loc[buy, 'Signal'] = 1
    df.loc[sell,'Signal'] = -1
    return df


def backtest_strategy(
    df: pd.DataFrame,
    initial_cash: float = 100_000,
    stop_loss_pct: float = 0.05,
    take_profit_pct: float = 0.10
) -> dict:
    """
    Backtest with optional stop-loss and take-profit:
    - Buys full position on Signal==1
    - Sells on Signal==-1 OR stop-loss/take-profit reached
    """
    cash = initial_cash
    position = 0
    entry_price = 0
    trades = []
    returns = []

    for i in range(1, len(df)):
        signal = int(df['Signal'].iloc[i])
        price = float(df['Close'].iloc[i])
        date = df.index[i]

        # Check stop-loss/take-profit
        if position > 0:
            pl = (price - entry_price) / entry_price
            if pl <= -stop_loss_pct or pl >= take_profit_pct:
                cash += position * price
                trades.append(('SELL_SLTP' if pl<=-stop_loss_pct else 'SELL_TP', date, price, position))
                returns.append(pl)
                position = 0
                entry_price = 0
                continue

        # BUY
        if signal == 1 and position == 0:
            position = int(cash // price)
            entry_price = price
            cash -= position * price
            trades.append(('BUY', date, price, position))

        # SELL on signal
        elif signal == -1 and position > 0:
            cash += position * price
            trades.append(('SELL', date, price, position))
            returns.append((price - entry_price) / entry_price)
            position = 0
            entry_price = 0

    # Final value
    final_value = cash + position * df['Close'].iloc[-1]
    roi = (final_value - initial_cash) / initial_cash * 100

    # Win rate
    wins = sum(1 for r in returns if r > 0)
    total_trades = len(returns)
    win_rate = wins / total_trades * 100 if total_trades > 0 else 0

    return {
        'ROI': round(roi, 2),
        'Win Rate': round(win_rate, 2),
        'Count': total_trades,
        'Trades': trades
    }
