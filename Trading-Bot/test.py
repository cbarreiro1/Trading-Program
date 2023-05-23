# Importing the API and instantiating the REST client according to our keys
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass

API_KEY = 'PKW33XAPHXH0B1L47RJP'
SECRET_KEY = '67nqMnGmsi67BhZQTWWnQX8rhvw3xMcHrnp9TKJc'

trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

# Getting account information and printing it
account = trading_client.get_account()
for property_name, value in account:
  print(f"\"{property_name}\": {value}")

# Check if our account is restricted from trading.
if account.trading_blocked:
    print('Account is currently restricted from trading.')

# Check how much money we can use to open new positions.
print('${} is available as buying power.'.format(account.buying_power))

# search for US equities
search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)

assets = trading_client.get_all_assets(search_params)

