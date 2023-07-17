from strategies import *
from alpaca_trading import buy, sell
from config import CONSTANT_STOCKS, INTERVAL, HISTORICAL_PERIOD, EMA_PERIODS, create_stock_bool_dict, update_macd_dict
import pandas as pd
import time
import yfinance as yf
from streaming import get_top_stocks
from datetime import datetime, time, timedelta

# Set the start and end time for the loop
start_time = time(9, 30)  # 9:30 am
end_time = time(16, 0)  # 4:00 pm

stock_symbols = CONSTANT_STOCKS + get_top_stocks() # We give 5 stocks and benzinga gives 3 more
macd_crossover = create_stock_bool_dict(stock_symbols)
macd_crossed_0 = create_stock_bool_dict(stock_symbols)

while True:
    current_time = datetime.now().time()

    # Check if the current time is between 9:30 am and 4 pm
    if current_time >= start_time and current_time <= end_time:
        # Check if the current minute is divisible by 5
        if current_time.minute % 5 == 0:
            # Create a dictionary to store the price history for each stock
            price_history = {}

            # Retrieve historical price data for each stock
            for symbol in stock_symbols:
                stock = yf.Ticker(symbol)
                historical_data = stock.history(period=HISTORICAL_PERIOD, interval=INTERVAL)
                price_history[symbol] = historical_data[['Close']].reset_index().rename(columns={'Datetime': 'Timestamp'})

            # Fetch the latest data for each stock
            for symbol in stock_symbols:
                stock_data = yf.download(symbol, period='7d', interval=INTERVAL)
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

                # Check if MACD crossover happened
                if is_macd_crossover(price_history[symbol]):
                    macd_crossover[symbol] = True
                
                # Check if MACD has crossed 0
                if latest_macd >= 0:
                    macd_crossed_0[symbol] = True

                # Check if MACD has crossed over and been greater than 0
                if macd_crossover[symbol] and macd_crossed_0[symbol]:
                    if buy(symbol, price_history):
                        print('Buy signal detected for', symbol, '. Executing buy order.')

                # Check if MACD crossunder happened or if MACD < 0 and execute a sell order
                if is_macd_crossunder(price_history[symbol]) or latest_macd < 0:
                    if sell(symbol, price_history):
                        print('Sell signal detected for', symbol, '. Executing sell order.')
                        macd_crossed_0[symbol] = False
                        macd_crossover[symbol] = False

                # Print the latest values
                latest_macd = price_history[symbol]['MACD Line'].iloc[-1]
                latest_signal = price_history[symbol]['Signal Line'].iloc[-1]
                print('Latest Price for', symbol, ':', latest_price)
                print('MACD Line for', symbol, ':', latest_macd)
                print('Signal Line for', symbol, ':', latest_signal)
                print('Timestamp for', symbol, ':', timestamp)
                print()

            # Update 10 minute counter
            if current_time.minute % 10 == 0:
                stock_symbols = CONSTANT_STOCKS + get_top_stocks() 
                update_macd_dict(macd_crossover, stock_symbols)
                update_macd_dict(macd_crossed_0, stock_symbols)

        time.sleep(1)

    # Checks if it is currently past 4pm
    else:
        print('Market has closed')
        print()
        break
    