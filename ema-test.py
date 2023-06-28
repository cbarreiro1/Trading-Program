#!/usr/bin/env python3

from alpaca.data.live import CryptoDataStream

API_KEY = "PKW33XAPHXH0B1L47RJP"
SECRET_KEY = "67nqMnGmsi67BhZQTWWnQX8rhvw3xMcHrnp9TKJc"

# Initiate class
crypto_stream = CryptoDataStream(API_KEY, SECRET_KEY)

prev_price = 0
curr_price = 0
i = 0

async def bar_callback(bar):
    if i % 5 == 0:
        for property_name, value in bar:
            if property_name == "close":
                prev_price = curr_price
                curr_price = float(value)
    i += i

# Subscribing to bar event 
symbol = "BTC/USD"
crypto_stream.subscribe_bars(bar_callback, symbol)

crypto_stream.run()
