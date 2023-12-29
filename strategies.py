from pandas import DataFrame

# Function to check if the MACD line is greater than the Signal line
def is_macd_line_over_signal(price_history:DataFrame, symbol:str):
    macd_line = price_history[symbol]['MACD Line']
    signal_line = price_history[symbol]['Signal Line']
    return macd_line.iloc[-1] > signal_line.iloc[-1]

# Function to check if the MACD line is greater than the zero line
def is_macd_line_over_zero(price_history:DataFrame, symbol:str):
    macd_line = price_history[symbol]['MACD Line']
    return macd_line.iloc[-1] > 0

# Function to check if the MACD has crossed over the Signal line
def has_macd_crossed_over_signal(price_history:DataFrame, symbol:str):
    macd_line = price_history[symbol]['MACD Line']
    signal_line = price_history[symbol]['Signal Line']
    return macd_line.iloc[-1] > signal_line.iloc[-1] and macd_line.iloc[-2] <= signal_line.iloc[-2]

# Function to check if the MACD has crossed over zero line
def has_macd_crossed_over_zero(price_history:DataFrame, symbol:str):
    macd_line = price_history[symbol]['MACD Line']
    return macd_line.iloc[-1] > 0 and macd_line.iloc[-2] <= 0

def has_macd_crossed_over_signal(values:list):
    return not values[-2] and values[-1]

def has_macd_crossed_over_zero(values:list):
    return not values[-2] and values[-1]
