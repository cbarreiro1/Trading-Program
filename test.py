from database import *
from config import CONSTANT_STOCKS

update_macd_database(stocks= CONSTANT_STOCKS)
print(get_macd_crossover_from_database())
update_macd_database(stock='BPTS', crossover=True)
update_macd_database(stock='ARDS', crossover=True)
print(get_macd_crossover_from_database())
update_stock_database(CONSTANT_STOCKS)
