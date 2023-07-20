import pandas as pd
import yfinance as yf
from time import sleep
from streaming import get_top_stocks
from datetime import datetime, time
from strategies import *
from alpaca_trading import buy, sell, get_held_stocks
from config import CONSTANT_STOCKS, INTERVAL, HISTORICAL_PERIOD, EMA_PERIODS, create_stock_bool_dict, update_macd_dict
from database import *

# Set the start and end time for the loop
start_time = time(9, 30)  # 9:30 am
end_time = time(16, 0)  # 4:00 pm

# Get the symbols of stocks that are already held
held_stocks = get_held_stocks()
added_stocks = [] # Stocks that have been bought not in CONSTANT_STOCKS
for stock in held_stocks:
    if stock not in CONSTANT_STOCKS:
        added_stocks.append(stock)

print(f'Starting the day holding {held_stocks}') 

if datetime.now().time() < start_time:
    delete_table('stock_status')
    delete_table('stock_data')

stock_symbols = CONSTANT_STOCKS + get_top_stocks(8 - len(CONSTANT_STOCKS) - len(added_stocks)) # We give stocks and it fills more in to make 8
update_stock_database(stock_symbols)

update_macd_database(stocks=stock_symbols)
macd_crossover = get_macd_crossover_from_database()

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

<<<<<<< HEAD
        # Fetch the latest data for each stock
        for symbol in STOCK_SYMBOLS:
            stock_data = yf.download(symbol, period='7d', interval=INTERVAL)
            latest_price = stock_data['Close'][-1]
            timestamp = stock_data.index[-1]
=======
            # Fetch the latest data for each stock
            for symbol in stock_symbols:
                stock_data = yf.download(symbol, period='7d', interval=INTERVAL)
                latest_price = stock_data['Close'][-1]
                timestamp = stock_data.index[-1]
>>>>>>> ab0a123d15982a013d40d2e069b283ee49a00fa7

                # Append the latest price to the price history dataframe
                price_history[symbol] = pd.concat([price_history[symbol], pd.DataFrame({'Timestamp': [timestamp], 'Close': [latest_price]})],
                                                ignore_index=True)

                # Calculate MACD line and signal line
                price_history[symbol]['MACD Line'] = price_history[symbol]['Close'].ewm(span=EMA_PERIODS[0], adjust=False).mean() - \
                                                    price_history[symbol]['Close'].ewm(span=EMA_PERIODS[1], adjust=False).mean()
                latest_macd = price_history[symbol]['MACD Line'].iloc[-1]

                price_history[symbol]['Signal Line'] = price_history[symbol]['MACD Line'].ewm(span=EMA_PERIODS[2], adjust=False).mean()
                latest_signal = price_history[symbol]['Signal Line'].iloc[-1]

                # Check if MACD crossover happened
                if is_macd_crossover(price_history, symbol):
                    update_macd_database(stock=symbol, crossover=True)
                    macd_crossover[symbol] = True

                # Check if MACD has had a crossover and been greater than 0
                if macd_crossover[symbol]:
                    print(f'MACD has crossed over the Signal Line for {symbol}.')
                    if latest_macd > 0 and latest_macd > latest_signal:
                        if buy(symbol, price_history):
                            print('Buy signal detected for', symbol, '. Executing buy order.')
                            if symbol not in CONSTANT_STOCKS and symbol not in added_stocks:
                                added_stocks.append(symbol)

                # Check if MACD crossunder happened or if MACD < 0 and execute a sell order
                if is_macd_crossunder(price_history, symbol) or latest_macd < 0:
                    if sell(symbol, price_history):
                        print('Sell signal detected for', symbol, '. Executing sell order.')
                        update_macd_database(stock=symbol)
                        macd_crossover[symbol] = False
                        if symbol in added_stocks:
                            added_stocks.remove(symbol)

<<<<<<< HEAD
        # Wait for the specified interval before fetching the data again
        time.sleep(300) # 5 minutes
=======
                # Print the latest values
                latest_macd = price_history[symbol]['MACD Line'].iloc[-1]
                latest_signal = price_history[symbol]['Signal Line'].iloc[-1]
                print('Latest Price for', symbol, ':', latest_price)
                print('MACD Line for', symbol, ':', latest_macd)
                print('Signal Line for', symbol, ':', latest_signal)
                print('Timestamp for', symbol, ':', timestamp)
                print()
>>>>>>> ab0a123d15982a013d40d2e069b283ee49a00fa7

                # Add the information to the database
                update_stock_data_to_database(symbol, latest_price, latest_macd, latest_signal, timestamp)

            # Checks top stocks every 10 minutes and updates stock database
            if current_time.minute % 10 == 0 and (len(CONSTANT_STOCKS) + len(added_stocks)) < 8:
                stock_symbols = CONSTANT_STOCKS + added_stocks + get_top_stocks(8 - len(CONSTANT_STOCKS) - len(added_stocks), added_stocks)
                update_stock_database(stock_symbols)
                update_macd_dict(macd_crossover, stock_symbols)
            
            update_macd_database(stocks=stock_symbols)
            sleep(60)

    # Checks if it is currently past 4 pm
    elif current_time > end_time:
        print('Market has closed')
        print()
        sort_stock_status_table()
        sort_stock_data_table()
        break
    