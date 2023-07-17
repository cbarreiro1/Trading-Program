# Populates a dictionary with all the stocks as keys and False as their values
def create_stock_bool_dict(stocks:list) -> dict:
    bool_dict = {}
    
    for stock in stocks:
        bool_dict[stock] = False

    return bool_dict
    
def update_macd_dict(macd_dict:dict, stocks:list):
    for stock in stocks:
        if stock not in macd_dict:
            macd_dict[stock] = False

CONSTANT_STOCKS = ['DMAQ', 'AIMD', 'WAVSU']
EMA_PERIODS = [12, 26, 9]
INTERVAL = '5m'  # Interval for price data
HISTORICAL_PERIOD = '7d'
BASE_URL = 'https://paper-api.alpaca.markets'  # Paper trading API base URL

# Alpaca API credentials
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'
APCA_API_KEY_ID = 'PKD2SNVTL4MK3CWY0Z3F'
APCA_API_SECRET_KEY = 'ImchqiPGdvb2PKXNaxZhIKIjbEpnuiauTl1R0eVl'

# Webdriver Path on Local Machine
WEBDRIVER_PATH = 'C:\\Users\\cjgat\\Downloads\\chromedriver_win32\\chromedriver.exe'
