import pandas as pd
import yfinance as yf
from time import sleep
from streaming import get_top_stocks
from datetime import datetime, time
from strategies import *
from alpaca_trading import buy, sell, get_held_stocks
from config import CONSTANT_STOCKS, INTERVAL, HISTORICAL_PERIOD, EMA_PERIODS, NUMBER_OF_STOCKS, update_macd_dict
from database import *

# Set the start and end time for the loop
start_time = time(9, 30)  # 9:30 am
end_time = time(16, 0)  # 4:00 pm

# Get the symbols of stocks that are already held
held_stocks = get_held_stocks()

# Stocks that have been bought not in CONSTANT_STOCKS
added_stocks = []
for stock in held_stocks:
    if stock not in CONSTANT_STOCKS:
        added_stocks.append(stock)

print(f'Starting the day holding {held_stocks}') 

# If it's earlier than 9:30 am
if datetime.now().time() < start_time:
    delete_all_tables_in_database('database.db')

# Searches for top stocks not in the constant list and adds them to search for  a number of stocks stocks at once
stock_symbols = CONSTANT_STOCKS + get_top_stocks(NUMBER_OF_STOCKS - len(CONSTANT_STOCKS) - len(added_stocks), excluded_stocks=added_stocks) + get_held_stocks()

update_macd_database(stocks=stock_symbols)
macd_crossover = get_macd_crossover_from_database()

# Create dictionaries to store MACD-related information for each stock
signal_dict = {symbol: [] for symbol in stock_symbols}
zero_dict = {symbol: [] for symbol in stock_symbols}


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
                historical_data = stock.history(period=HISTORICAL_PERIOD, interval=INTERVAL, prepost=True)
                price_history[symbol] = historical_data[['Close']].reset_index().rename(columns={'Datetime': 'Timestamp'})

            # Fetch the latest data for each stock
            for symbol in stock_symbols:
                try:
                    stock_data = yf.download(symbol, period='60d', interval=INTERVAL)
                    latest_price = stock_data['Close'][-1]
                    timestamp = current_time

                    # Append the latest price to the price history dataframe
                    price_history[symbol] = pd.concat([price_history[symbol], pd.DataFrame({'Timestamp': [timestamp], 'Close': [latest_price]})],
                                                    ignore_index=True)

                    # Append the latest price to the price history dataframe
                    price_history[symbol] = pd.concat([price_history[symbol], pd.DataFrame({'Timestamp': [timestamp], 'Close': [latest_price]})],
                                                    ignore_index=True)

                    # Calculate MACD line and signal line
                    price_history[symbol]['MACD Line'] = price_history[symbol]['Close'].ewm(span=EMA_PERIODS[0], adjust=False).mean() - \
                                                        price_history[symbol]['Close'].ewm(span=EMA_PERIODS[1], adjust=False).mean()
                    latest_macd = price_history[symbol]['MACD Line'].iloc[-1]

                    price_history[symbol]['Signal Line'] = price_history[symbol]['MACD Line'].ewm(span=EMA_PERIODS[2], adjust=False).mean()
                    latest_signal = price_history[symbol]['Signal Line'].iloc[-1]

                    # Add the symbol to the dictionaries if it's a new stock being searched for
                    if symbol not in signal_dict:
                        signal_dict[symbol] = []
                        zero_dict[symbol] = []

                    #Defines True or False
                    macd_over_signal = False
                    macd_over_zero = False
                    macd_crossed_over_signal = False
                    macd_crossed_over_zero = False
                    
                    #Stores data for each stock
                    macd_over_signal = is_macd_line_over_signal(price_history, symbol)
                    macd_over_zero = is_macd_line_over_zero(price_history, symbol)
                    # macd_crossed_over_signal = has_macd_crossed_over_signal(price_history, symbol)
                    # macd_crossed_over_zero = has_macd_crossed_over_zero(price_history, symbol)
                    signal_dict[symbol].append(macd_over_signal)
                    zero_dict[symbol].append(macd_over_zero)
                    if (len(signal_dict[symbol]) >= 2 and len(zero_dict[symbol]) >= 2):
                        macd_crossed_over_signal = has_macd_crossed_over_signal(signal_dict[symbol])
                        macd_crossed_over_zero = has_macd_crossed_over_zero(zero_dict[symbol])
                        
 

                    # Check if the stock meets the criteria to buy or sell
                    true_count = sum([macd_over_signal, macd_over_zero, macd_crossed_over_signal, macd_crossed_over_zero])
                    if true_count >= 3:
                         if buy(symbol, price_history):
                          print('Buy signal detected for', symbol, '. Executing buy order.')
                         if symbol not in CONSTANT_STOCKS and symbol not in added_stocks:
                           added_stocks.append(symbol)
                    else:  # Otherwise, sell the stock only if it has 3 false values
                         false_count = 4 - true_count
                         if false_count >= 3:
                            if sell(symbol, price_history):
                               print('Sell signal detected for', symbol, '. Executing sell order.')
                               if symbol in added_stocks:
                                  added_stocks.remove(symbol)

                    # Print the latest values
                    latest_macd = price_history[symbol]['MACD Line'].iloc[-1]
                    latest_signal = price_history[symbol]['Signal Line'].iloc[-1]
                    print('Latest Price for', symbol, ':', latest_price)
                    print('MACD Line for', symbol, ':', latest_macd)
                    print('Signal Line for', symbol, ':', latest_signal)
                    print('MACD Over Signal:', macd_over_signal)
                    print('MACD Over Zero:', macd_over_zero)
                    print('MACD Crossover Signal:', macd_crossed_over_signal)
                    print('MACD Crossover Zero:', macd_crossed_over_zero)
                    print('Timestamp for', symbol, ':', timestamp)
                    print()

                    # Add the information to the database
                    update_stock_data_table(symbol, latest_price, latest_macd, latest_signal, macd_crossover[symbol], macd_over_signal, macd_over_zero, macd_crossed_over_signal, macd_crossed_over_zero)

                except Exception as e:
                    # Handle the exception (e.g., stock data not available)
                    print(f"Failed download: {symbol}: {e}")

            # Checks top stocks every 10 minutes and updates stock database
            if current_time.minute % 10 == 0 and (len(CONSTANT_STOCKS) + len(added_stocks)) < NUMBER_OF_STOCKS:
                stock_symbols = CONSTANT_STOCKS + added_stocks + get_top_stocks(NUMBER_OF_STOCKS - len(CONSTANT_STOCKS) - len(added_stocks), added_stocks)
                update_macd_dict(macd_crossover, stock_symbols)
            
            update_macd_database(stocks=stock_symbols)
            sleep(60)

    # Checks if it is currently past 4 pm
    elif current_time > end_time:
        print('Market has closed')
        print()
        break
    