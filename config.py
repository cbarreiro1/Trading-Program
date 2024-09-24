# Populates a dictionary with all the stocks as keys and False as their values
def create_stock_bool_dict(stocks:list) -> dict:
    bool_dict = {}
    
    for stock in stocks:
        bool_dict[stock] = False

    return bool_dict
    
# Updates MACD dict to only have keys present in the stock list
def update_macd_dict(macd_dict:dict, stocks:list):
    delete = []
    for stock in stocks:
        if stock not in macd_dict:
            macd_dict[stock] = False
    for key in macd_dict.keys():
        if key not in stocks:
            delete.append(key)
    for key in delete:
        if key in macd_dict.keys():
            del macd_dict[key]

# Set up variables before running
CONSTANT_STOCKS = []
NUMBER_OF_STOCKS = 7
EXCLUDED_STOCKS = []
EMA_PERIODS = [12, 26, 9]
INTERVAL = '5m'  # Interval for price data
HISTORICAL_PERIOD = '60d'
BASE_URL = 'https://paper-api.alpaca.markets'  # Paper trading API base URL

#PDT Trade Count
Max_Trade_Count = 3

# Alpaca API credentials
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'
APCA_API_KEY_ID = 'PUT_API_KEY_HERE'
APCA_API_SECRET_KEY = 'PUT_SECRET_KEY_HERE'

# Webdriver path on local machine
WEBDRIVER_PATH = 'C:\\Users\\cjgat\\Downloads\\chromedriver_win32\\chromedriver.exe'
