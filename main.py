from macd_calc import is_macd_crossover, is_macd_crossunder
from alpaca_trading import buy, sell, get_shares
from constants import CRYPTO_SYMBOLS, SYMBOL_MAPPING, INTERVAL, BASE_URL, HISTORICAL_PERIOD, EMA_PERIODS
import pandas as pd
import time
import yfinance as yf

# Create a dictionary to store the price history for each cryptocurrency
price_history = {}

# Retrieve historical price data for each cryptocurrency
for symbol in CRYPTO_SYMBOLS:
    crypto_symbol = SYMBOL_MAPPING[symbol]  # Map the symbol to the one used by yfinance and Alpaca
    crypto = yf.Ticker(crypto_symbol)
    historical_data = crypto.history(period=HISTORICAL_PERIOD, interval=INTERVAL)
    price_history[symbol] = historical_data[['Close']].reset_index().rename(columns={'Datetime': 'Timestamp'})

while True:
    # Fetch the latest data for each cryptocurrency
    for symbol in CRYPTO_SYMBOLS:
        crypto_symbol = SYMBOL_MAPPING[symbol]  # Map the symbol to the one used by yfinance and Alpaca
        crypto_data = yf.download(crypto_symbol, period='1d', interval=INTERVAL)
        latest_price = crypto_data['Close'][-1]
        timestamp = crypto_data.index[-1]

        # Append the latest price to the price history dataframe
        price_history[symbol] = pd.concat([price_history[symbol], pd.DataFrame({'Timestamp': [timestamp], 'Close': [latest_price]})],
                                          ignore_index=True)

        # Calculate MACD line and signal line
        price_history[symbol]['MACD Line'] = price_history[symbol]['Close'].ewm(span=EMA_PERIODS[0], adjust=False).mean() - \
                                             price_history[symbol]['Close'].ewm(span=EMA_PERIODS[1], adjust=False).mean()
        price_history[symbol]['Signal Line'] = price_history[symbol]['MACD Line'].ewm(span=EMA_PERIODS[2], adjust=False).mean()

        # Check if MACD crossover happened and execute a buy order
        if is_macd_crossover(price_history[symbol]):
            if buy(symbol, price_history):
             print('Buy signal detected for', symbol, '. Executing buy order.')

        # Check if MACD crossunder happened and execute a sell order
        if is_macd_crossunder(price_history[symbol]):
            if sell(symbol, price_history):
                print('Sell signal detected for', symbol, '. Executing sell order.')

        # Print the latest values
        latest_macd = price_history[symbol]['MACD Line'].iloc[-1]
        latest_signal = price_history[symbol]['Signal Line'].iloc[-1]
        print('Latest Price for', symbol, ':', latest_price)
        print('MACD Line for', symbol, ':', latest_macd)
        print('Signal Line for', symbol, ':', latest_signal)
        print('Timestamp for', symbol, ':', timestamp)
        print()

    # Wait for the specified interval before fetching the data again
    time.sleep(60)