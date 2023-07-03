#!/usr/bin/env python3

from alpaca.data.live import CryptoDataStream

API_KEY = "PK84NICY437SAQUL8QED"
SECRET_KEY = "2Wuz5WU20CNbavyzjeiYCt5Udq1owH7g3r0CzVny"

# Initiate class
crypto_stream = CryptoDataStream(API_KEY, SECRET_KEY)

async def bar_callback(bar):
    for property_name, value in bar:
        print(f"\"{property_name}\": {value}")
    print("\n")

# Subscribing to bar event 
symbol = "BTC/USD"
crypto_stream.subscribe_bars(bar_callback, symbol)

crypto_stream.run()
