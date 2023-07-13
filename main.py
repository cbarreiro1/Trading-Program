from strategies import *
from alpaca_trading import buy, sell
from constants import STOCK_SYMBOLS, INTERVAL, HISTORICAL_PERIOD, EMA_PERIODS
import pandas as pd
import time
import yfinance as yf
import datetime

while True:
    now = datetime.datetime.now()
    current_hour = now.hour
    current_minute = now.minute

    # Check if the current time is between 9:30 am and 4 pm
    if (current_hour == 9 and current_minute >= 30) or (current_hour > 9 and current_hour <= 16):
        # Create a dictionary to store the price history for each stock
        price_history = {}

        # Retrieve historical price data for each stock
        for symbol in STOCK_SYMBOLS:
            stock = yf.Ticker(symbol)
            historical_data = stock.history(period=HISTORICAL_PERIOD, interval=INTERVAL)
            price_history[symbol] = historical_data[['Close']].reset_index().rename(columns={'Datetime': 'Timestamp'})

        # Fetch the latest data for each stock
        for symbol in STOCK_SYMBOLS:
            stock_data = yf.download(symbol, period='1mo', interval=INTERVAL)
            latest_price = stock_data['Close'][-1]
            timestamp = stock_data.index[-1]

            # Append the latest price to the price history dataframe
            price_history[symbol] = pd.concat([price_history[symbol], pd.DataFrame({'Timestamp': [timestamp], 'Close': [latest_price]})],
                                              ignore_index=True)

            # Calculate MACD line and signal line
            price_history[symbol]['MACD Line'] = price_history[symbol]['Close'].ewm(span=EMA_PERIODS[0], adjust=False).mean() - \
                                                 price_history[symbol]['Close'].ewm(span=EMA_PERIODS[1], adjust=False).mean()
            latest_macd = price_history[symbol]['MACD Line'].iloc[-1]

            price_history[symbol]['Signal Line'] = price_history[symbol]['MACD Line'].ewm(span=EMA_PERIODS[2], adjust=False).mean()

            # Check if MACD crossover happened and execute a buy order
            if is_macd_crossover(price_history[symbol]) and (latest_macd >= 0):
                if buy(symbol, price_history):
                    print('Buy signal detected for', symbol, '. Executing buy order.')

            # Check if MACD crossunder happened and execute a sell order
            if is_macd_crossunder(price_history[symbol]) or (latest_macd < 0):
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
        time.sleep(900) # 15 minutes

    # Checks if it is currently past 4pm
    elif current_hour > 16:
        print('Market has closed')
        print()
        break
    