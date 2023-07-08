import alpaca_trade_api as tradeapi
import yfinance as yf
import pandas as pd
import time
from message import send_text

CRYPTO_SYMBOLS = ['BTC/USD', 'ETH/USD']  # Top cryptocurrency symbols
SYMBOL_MAPPING = {
    'BTC/USD': 'BTC-USD',
    'ETH/USD': 'ETH-USD'
}
EMA_PERIODS = [12, 26, 9]
INTERVAL = '1m'  # Interval for price data
HISTORICAL_PERIOD = '5d'

# Alpaca API credentials (replace these with your own)
API_KEY = 'PKQ88CJGU5PFET73L9EU'
SECRET_KEY = 'ors04z9pZAzJynPJS0ZffByvAqKHSohaBhcn42hj'
BASE_URL = 'https://paper-api.alpaca.markets'  # Paper trading API base URL

# Initialize the Alpaca API client
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL, api_version='v2')

# Function to check if the MACD crossover happened
def is_macd_crossover(price_history):
    return price_history['MACD Line'].iloc[-2] < price_history['Signal Line'].iloc[-2] and \
           price_history['MACD Line'].iloc[-1] > price_history['Signal Line'].iloc[-1]

# Function to check if the MACD crossunder happened
def is_macd_crossunder(price_history):
    return price_history['MACD Line'].iloc[-2] > price_history['Signal Line'].iloc[-2] and \
           price_history['MACD Line'].iloc[-1] < price_history['Signal Line'].iloc[-1]

# Function to execute a buy order
def buy(symbol):
    # Get account information
    account = api.get_account()
    available_cash = float(account.cash) * 0.1  # Ten percent of available cash

    # Get the latest price for the symbol
    crypto_data = yf.download(SYMBOL_MAPPING[symbol], period='1d', interval=INTERVAL)
    latest_price = crypto_data['Close'][-1]

    # Calculate the maximum quantity of shares to buy
    quantity = int(available_cash / latest_price)

    # Check if shares are already held for the symbol
    if quantity == 0:
        print('Not enough available cash to buy shares of', symbol)
        return

    api.submit_order(
        symbol=symbol,
        qty=quantity,
        side='buy',
        type='market',
        time_in_force='gtc'
    )

    total_price = latest_price * quantity
    send_text(f"{quantity} share(s) of {symbol} have been bought for ${total_price:.2f}")

# Function to execute a sell order
def sell(symbol):
    # Check if shares are held for the symbol
    position = api.get_position(symbol)
    if position.qty == '0':
        print('No shares of', symbol, 'are currently held. Skipping sell order.')
        return

    api.submit_order(
        symbol=symbol,
        qty=position.qty,
        side='sell',
        type='market',
        time_in_force='gtc'
    )

    latest_price = price_history[symbol]['Close'].iloc[-1]  # Get the latest price for the symbol
    total_price = latest_price * int(position.qty)
    send_text(f"{position.qty} share(s) of {symbol} have been sold for ${total_price:.2f}")

# Create a dictionary to store the price history for each cryptocurrency
price_history = {}

# Retrieve historical price data for each cryptocurrency
for symbol in CRYPTO_SYMBOLS:
    crypto = yf.Ticker(SYMBOL_MAPPING[symbol])
    historical_data = crypto.history(period=HISTORICAL_PERIOD, interval=INTERVAL)
    price_history[symbol] = historical_data[['Close']].reset_index().rename(columns={'Datetime': 'Timestamp'})

while True:
    # Fetch the latest data for each cryptocurrency
    for symbol in CRYPTO_SYMBOLS:
        crypto_data = yf.download(SYMBOL_MAPPING[symbol], period='1d', interval=INTERVAL)
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
            buy(symbol)
            print('Buy signal detected for', symbol, '. Executing buy order.')

        # Check if MACD crossunder happened and execute a sell order
        if is_macd_crossunder(price_history[symbol]):
            sell(symbol)
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
