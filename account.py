#!/usr/bin/env python3

# Importing the API and instantiating the REST client according to our keys
from alpaca.trading.client import TradingClient

API_KEY = "PKD2SNVTL4MK3CWY0Z3F"
SECRET_KEY = "ImchqiPGdvb2PKXNaxZhIKIjbEpnuiauTl1R0eVl"

trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

account = trading_client.get_account()
for property_name, value in account:
  print(f"\"{property_name}\": {value}")
