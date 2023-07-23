# Function to check if the MACD crossover happened
def is_macd_crossover(price_history, symbol):
    macd_line = price_history[symbol]['MACD Line']
    signal_line = price_history[symbol]['Signal Line']
    return macd_line.iloc[-2] < signal_line.iloc[-2] and macd_line.iloc[-1] > signal_line.iloc[-1]

# Function to check if the MACD crossunder happened
def is_macd_crossunder(price_history, symbol):
    macd_line = price_history[symbol]['MACD Line']
    signal_line = price_history[symbol]['Signal Line']
    return macd_line.iloc[-2] > signal_line.iloc[-2] and macd_line.iloc[-1] < signal_line.iloc[-1]
