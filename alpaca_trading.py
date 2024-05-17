import alpaca_trade_api as tradeapi
from config import APCA_API_BASE_URL, APCA_API_KEY_ID, APCA_API_SECRET_KEY, CODE_RUNNER
import pandas as pd
from message import send_text
from datetime import datetime, time

# Initialize the Alpaca API client
api = tradeapi.REST(APCA_API_KEY_ID[CODE_RUNNER], APCA_API_SECRET_KEY[CODE_RUNNER], APCA_API_BASE_URL, api_version='v2')

def get_shares(symbol:str) -> float:
    # Retrieve your account's positions
    positions = api.list_positions()

    # Find the position for the specific stock you want
    stock_position = next((position for position in positions if position.symbol == symbol), None)

    # Check if you hold the stock
    if stock_position is not None:
        return stock_position.qty
    else:
        return 0

# Function to execute a buy order
def buy(symbol:str, price_history:dict) -> bool:
    # Check if shares are already held for the symbol
    if float(get_shares(symbol)) > 0:
        print('Shares of', symbol, 'are already being held. Skipping buy order.')
        return False
    
    # Get account information
    account = api.get_account()
    equity = float(account.equity) * 0.33  # 10% of equity in account

    latest_price = price_history[symbol]['Close'].iloc[-1]  # Get the latest price for the symbol

    # Calculate maximum quantity of shares to buy
    quantity = int(equity / latest_price)

    # Checks if at least one share is being bought
    if quantity == 0:
        print('Skipping buy order. Not enough equity to buy a full share.')
        return False

    api.submit_order(
        symbol=symbol,
        qty=quantity,
        side='buy',
        type='market',
        time_in_force='gtc'
    )

    send_text(f"{quantity} share(s) of {symbol} have been bought for ${(quantity * latest_price):.2f}")
    return True

# Function to execute a sell order
def sell(symbol:str, price_history:dict) -> bool:
    # Check if shares are held for the symbol
    if float(get_shares(symbol)) == 0:
        print('No shares of', symbol, 'are currently held. Skipping sell order.')
        return False

    quantity = get_shares(symbol)

    api.submit_order(
        symbol=symbol,
        qty=quantity,
        side='sell',
        type='market',
        time_in_force='gtc'
    )

    latest_price = price_history[symbol]['Close'].iloc[-1]  # Get the latest price for the symbol
    total_price = latest_price * int(quantity)
    send_text(f"{quantity} share(s) of {symbol} have been sold for ${total_price:.2f}")
    return True

# Get the symbols of stocks that are already held
def get_held_stocks() -> list:
    return [position.symbol for position in api.list_positions()]


def sell_all_positions_before_market_close():
    current_time = datetime.now().time()
    # Check if it's 3:55 PM
    if current_time == time(15, 55):
        held_stocks = get_held_stocks()
        if held_stocks:
            print("Selling all open positions before market close")
            for symbol in held_stocks:
                sell(symbol)
                print(f"Sold all shares of {symbol}")
        else:
            print("No open positions to sell.")
