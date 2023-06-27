#!/usr/bin/env python3

# Importing the API and instantiating the REST client according to our keys
from alpaca.trading.client import TradingClient

API_KEY = "PKW33XAPHXH0B1L47RJP"
SECRET_KEY = "67nqMnGmsi67BhZQTWWnQX8rhvw3xMcHrnp9TKJc"

trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

account = trading_client.get_account()
for property_name, value in account:
  print(f"\"{property_name}\": {value}")
