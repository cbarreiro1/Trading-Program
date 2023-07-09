# Function to check if the MACD crossover happened
def is_macd_crossover(price_history:dict) -> bool:
    return price_history['MACD Line'].iloc[-2] < price_history['Signal Line'].iloc[-2] and \
           price_history['MACD Line'].iloc[-1] > price_history['Signal Line'].iloc[-1]

# Function to check if the MACD crossunder happened
def is_macd_crossunder(price_history:dict) -> bool:
    return price_history['MACD Line'].iloc[-2] > price_history['Signal Line'].iloc[-2] and \
           price_history['MACD Line'].iloc[-1] < price_history['Signal Line'].iloc[-1]