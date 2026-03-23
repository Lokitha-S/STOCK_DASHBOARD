import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

ticker_symbol = input("Enter Stock Ticker (e.g., TSLA): ").upper()
# Fetching 1 year of daily data
data = yf.download(ticker_symbol, period="1y", interval="1d")

if data.empty:
    print("No data found. Check the ticker symbol.")
    exit()

# SMA 20
data['SMA_20'] = data['Close'].rolling(window=20).mean()

# EMA 20
data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()

# RSI (14-day)
delta = data['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
data['RSI'] = 100 - (100 / (1 + rs))

# Create a figure with two subplots (Price and RSI)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1]})

# Plot 1: Price, SMA, and EMA
ax1.plot(data.index, data['Close'], label='Close Price', alpha=0.5)
ax1.plot(data.index, data['SMA_20'], label='SMA 20', color='orange')
ax1.plot(data.index, data['EMA_20'], label='EMA 20', color='green')
ax1.set_title(f"{ticker_symbol} Technical Analysis")
ax1.legend()

# Plot 2: RSI
ax2.plot(data.index, data['RSI'], color='purple', label='RSI')
ax2.axhline(70, color='red', linestyle='--') # Overbought line
ax2.axhline(30, color='blue', linestyle='--') # Oversold line
ax2.set_ylim(0, 100)
ax2.set_ylabel("RSI")

plt.show()

output_file = f"{ticker_symbol}_analysis.csv"
data.to_csv(output_file)
print(f"Analysis saved to {output_file}")