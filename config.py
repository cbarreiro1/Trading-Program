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

CONSTANT_STOCKS = []
EXCLUDED_STOCKS = []
EMA_PERIODS = [12, 26, 9]
INTERVAL = '5m'  # Interval for price data
HISTORICAL_PERIOD = '7d'
BASE_URL = 'https://paper-api.alpaca.markets'  # Paper trading API base URL

# Alpaca API credentials
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'
APCA_API_KEY_ID = {'CJ': 'PKHNW562AA4FC6BQ9Y0L',
                   'Durston': 'PKIT5MXHGJEBG1GRXQSJ'}
APCA_API_SECRET_KEY = {'CJ': 'aOeNOqIG9ortGxsyxqcpY1rmbk7ZpaftkxGyKzXv',
                       'Durston': 'QRFOYM1dCY0UHGLdLkjypzZblxbdjnL3FInHliCC'}

# Webdriver path on local machine
WEBDRIVER_PATH = {'CJ': 'C:\\Users\\cjgat\\Downloads\\chromedriver_win32\\chromedriver.exe',
                  'Durston': 'C:\\Users\\durst\\Downloads\\chromedriver.exe'}

# Person running the code
CODE_RUNNER = 'CJ'
