import yfinance as yf
import alpaca_trade_api as tradeapi
import pandas as pd
import time
from message import send_text

STOCK_SYMBOL = 'CRBU'
EMA_PERIODS = [12, 26, 9]
INTERVAL = '5m'  # Interval for price data
HISTORICAL_PERIOD = '7d'
BASE_URL = 'https://paper-api.alpaca.markets'  # Paper trading API base URL

# Alpaca API credentials (replace these with your own)
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'
APCA_API_KEY_ID = 'PKD2SNVTL4MK3CWY0Z3F'
APCA_API_SECRET_KEY = 'ImchqiPGdvb2PKXNaxZhIKIjbEpnuiauTl1R0eVl'

# Initialize the Alpaca API client
api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL, api_version='v2')

# Function to check if the MACD crossover happened
def is_macd_crossover(price_history):
    return price_history['MACD Line'].iloc[-2] < price_history['Signal Line'].iloc[-2] and \
           price_history['MACD Line'].iloc[-1] > price_history['Signal Line'].iloc[-1]

# Function to check if the MACD crossunder happened
def is_macd_crossunder(price_history):
    return price_history['MACD Line'].iloc[-2] > price_history['Signal Line'].iloc[-2] and \
           price_history['MACD Line'].iloc[-1] < price_history['Signal Line'].iloc[-1]

# Function to execute a buy order
def buy(symbol, quantity):
    api.submit_order(
        symbol=symbol,
        qty=quantity,
        side='buy',
        type='market',
        time_in_force='gtc'

        send_text(text)
    )

# Function to execute a sell order
def sell(symbol, quantity):
    api.submit_order(
        symbol=symbol,
        qty=quantity,
        side='sell',
        type='market',
        time_in_force='gtc'

        send_text(text)
    )
    
# Retrieve historical price data for the past 7 trading days
stock = yf.Ticker(STOCK_SYMBOL)
historical_data = stock.history(period=HISTORICAL_PERIOD, interval=INTERVAL)

# Initialize the price history dataframe with historical data
price_history = historical_data[['Close']].reset_index().rename(columns={'Datetime': 'Timestamp'})

# Calculate MACD line and signal line
price_history['MACD Line'] = price_history['Close'].ewm(span=EMA_PERIODS[0], adjust=False).mean() - \
                             price_history['Close'].ewm(span=EMA_PERIODS[1], adjust=False).mean()
price_history['Signal Line'] = price_history['MACD Line'].ewm(span=EMA_PERIODS[2], adjust=False).mean()

while True:
    # Fetch the latest data for the stock
    stock_data = yf.download(STOCK_SYMBOL, period='1d', interval=INTERVAL)
    latest_price = stock_data['Close'][-1]
    timestamp = stock_data.index[-1]

    # Append the latest price to the price history dataframe
    price_history = pd.concat([price_history, pd.DataFrame({'Timestamp': [timestamp], 'Close': [latest_price]})],
                              ignore_index=True)

    # Calculate MACD line and signal line
    price_history['MACD Line'] = price_history['Close'].ewm(span=EMA_PERIODS[0], adjust=False).mean() - \
                                 price_history['Close'].ewm(span=EMA_PERIODS[1], adjust=False).mean()
    price_history['Signal Line'] = price_history['MACD Line'].ewm(span=EMA_PERIODS[2], adjust=False).mean()

    # Check if MACD crossover happened and execute a buy order
    if is_macd_crossover(price_history):
        buy(STOCK_SYMBOL, 1000)
        print('Buy signal detected. Executing buy order.')

    # Check if MACD crossunder happened and execute a sell order
    if is_macd_crossunder(price_history):
        sell(STOCK_SYMBOL, 1000)
        print('Sell signal detected. Executing sell order.')

    # Print the latest values
    latest_macd = price_history['MACD Line'].iloc[-1]
    latest_signal = price_history['Signal Line'].iloc[-1]
    print('Latest Price:', latest_price)
    print('MACD Line:', latest_macd)
    print('Signal Line:', latest_signal)
    print('Timestamp:', timestamp)
    print()

    # Wait for the specified interval before fetching the data again
    time.sleep(300)
