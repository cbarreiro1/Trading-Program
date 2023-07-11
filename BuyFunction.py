import alpaca_trade_api as tradeapi
import yfinance as yf

# Alpaca API credentials
API_KEY = 'PKQ88CJGU5PFET73L9EU'
SECRET_KEY = 'ors04z9pZAzJynPJS0ZffByvAqKHSohaBhcn42hj'
BASE_URL = 'https://paper-api.alpaca.markets'  # Paper trading base URL (sandbox environment)

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL, api_version='v2')

# Get account information
account = api.get_account()
available_cash = float(account.cash) * 0.1  # Ten percent of available cash

# Define the stock symbol and the number of shares to buy
symbol = 'AAPL'  # Example stock symbol
shares_to_buy = available_cash // yf.Ticker(symbol).history().iloc[-1]['Close']  # Buy as many shares as possible

# Place the buy order
api.submit_order(
    symbol=symbol,
    qty=shares_to_buy,
    side='buy',
    type='market',
    time_in_force='gtc'
)

print(f"Bought {shares_to_buy} shares of {symbol} using {available_cash:.2f} USD.")
