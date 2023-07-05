import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import time

STOCK_SYMBOL = 'AAPL'
EMA_PERIODS = [12, 26, 9]
INTERVAL = '1m'  # Interval for price data
HISTORICAL_PERIOD = '7d'

# Retrieve historical price data for the past 7 trading days
stock = yf.Ticker(STOCK_SYMBOL)
historical_data = stock.history(period=HISTORICAL_PERIOD, interval=INTERVAL)

# Initialize the price history dataframe with historical data
price_history = historical_data[['Close']].reset_index().rename(columns={'Datetime': 'Timestamp'})

# Calculate MACD line and signal line
price_history['MACD Line'] = price_history['Close'].ewm(span=EMA_PERIODS[0], adjust=False).mean() - \
                             price_history['Close'].ewm(span=EMA_PERIODS[1], adjust=False).mean()
price_history['Signal Line'] = price_history['MACD Line'].ewm(span=EMA_PERIODS[2], adjust=False).mean()

# Plot the graph
plt.xlabel('Timestamp')
plt.ylabel('Price')
plt.title('MACD Indicator')
plt.legend()

while True:
    # Retrieve live price data for Apple
    data = stock.history(period='1d', interval=INTERVAL)

    # Get the latest price
    latest_price = data['Close'][-1]
    timestamp = data.index[-1]

    # Append the latest price to the price history dataframe
    price_history = pd.concat([price_history, pd.DataFrame({'Timestamp': [timestamp], 'Close': [latest_price]})],
                              ignore_index=True)

    # Calculate MACD line and signal line
    price_history['MACD Line'] = price_history['Close'].ewm(span=EMA_PERIODS[0], adjust=False).mean() - \
                                 price_history['Close'].ewm(span=EMA_PERIODS[1], adjust=False).mean()
    price_history['Signal Line'] = price_history['MACD Line'].ewm(span=EMA_PERIODS[2], adjust=False).mean()

    # Print the latest values
    latest_macd = price_history['MACD Line'].iloc[-1]
    latest_signal = price_history['Signal Line'].iloc[-1]
    print('Latest Price:', latest_price)
    print('MACD Line:', latest_macd)
    print('Signal Line:', latest_signal)
    print('Timestamp:', timestamp)
    print()

    # Plot the graph
    plt.plot(price_history['Timestamp'], price_history['MACD Line'], label='MACD Line')
    plt.plot(price_history['Timestamp'], price_history['Signal Line'], label='Signal Line')

    # Show the updated plot
    plt.pause(0.01)  # Display the plot for a short duration without blocking

    # Wait for the specified interval before fetching the data again
    time.sleep(60)
    