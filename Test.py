from alpaca.data.live import CryptoDataStream

API_KEY = 'PKW33XAPHXH0B1L47RJP'
SECRET_KEY = '67nqMnGmsi67BhZQTWWnQX8rhvw3xMcHrnp9TKJc'

# Initiate class
crypto_stream = CryptoDataStream(API_KEY, SECRET_KEY)

async def bar_callback(bar):
    for property_name, value in bar:
        print(f"\"{property_name}\": {value}")

# Subscribing to bar event 
symbol = "AAPL"
crypto_stream.subscribe_bars(bar_callback, symbol)

crypto_stream.run()


