import yfinance as yf
import alpaca_trade_api as tradeapi
from message import send_text

# Alpaca API credentials (replace these with your own)
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'
APCA_API_KEY_ID = 'PKPGKE6TQF1HOU642RKN'
APCA_API_SECRET_KEY = 'lQgguyUp3tSHTiMbzfmvLcwCcCexNVguUvoL4Mkg'

# Initialize the Alpaca API client
api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL, api_version='v2')

# Function to execute a buy order
def buy(symbol, max_budget_percentage=0.1):
    # Get the account information
    account = api.get_account()
    available_cash = float(account.buying_power) * max_budget_percentage

    # Get the latest price for the symbol
    crypto = yf.Ticker(symbol)
    latest_price = float(crypto.history(period='1d')['Close'][-1])

    # Calculate the maximum quantity of shares that can be bought within the budget
    max_quantity = int(available_cash / latest_price)

    # Place a market order to buy the maximum quantity of shares
    if max_quantity > 0:
        api.submit_order(
            symbol=symbol,
            qty=max_quantity,
            side='buy',
            type='market',
            time_in_force='gtc'
        )

        total_price = latest_price * max_quantity
        send_text(f"{max_quantity} share(s) of {symbol} have been bought for ${total_price:.2f}")

# Function to print available cash in the account
def print_available_cash():
    account = api.get_account()
    available_cash = float(account.buying_power)
    print(f"Available cash in the account: ${available_cash:.2f}")

# Print available cash in the account
print_available_cash()

# Buy Ethereum (ETH) using 10% of available cash
buy('ETH/USD', max_budget_percentage=0.1)
