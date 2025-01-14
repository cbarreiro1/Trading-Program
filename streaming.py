from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from config import WEBDRIVER_PATH, CONSTANT_STOCKS, EXCLUDED_STOCKS, CODE_RUNNER

# Given a certain number of stocks to look for and stocks to exclude from the list, it searched for the top stocks based on % Change
def get_top_stocks(number_to_look_for:int, excluded_stocks:list=[]) -> list:
    # Configure the webdriver (make sure you have the appropriate driver executable installed)
    options = Options()
    options.add_argument(WEBDRIVER_PATH[CODE_RUNNER])
    driver = webdriver.Chrome(options=options)

    # Load the Benzinga premarket page
    driver.get('https://stockanalysis.com/markets/gainers/')

    # Wait for the Gainers table to load
    time.sleep(2)  # Add a delay to allow the page to load
    gainers_table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-table"]')))
    gainers_rows = gainers_table.find_elements(By.XPATH, './/tbody/tr')

    # Create a list to store the stock data
    stocks = []

    # Iterate over the Gainers table rows and extract symbol and percent change values
    for row in gainers_rows:
        symbol = row.find_element(By.XPATH, './td[2]').text
        percent_change = row.find_element(By.XPATH, './td[4]').text
        percent_change = percent_change.strip('%').replace('$', '')  # Remove '%' and '$' characters
        volume = row.find_element(By.XPATH, './td[6]').text
        volume = volume.replace(',', '')  # Remove ',' characters
        volume = int(volume)
        if volume >= 400000:
            stocks.append({'symbol': symbol, 'percent_change': percent_change, 'volume': volume})

    # Sort the stocks based on percent change in descending order
    sorted_stocks = sorted(stocks, key=lambda stock: float(stock['percent_change'].strip('%')), reverse=True)
    top_stocks = []

    # Print the top 3 stocks with the highest percent change (excluding those in CONSTANT_STOCKS)
    print(f'Current Top Stocks Based on % Change with over 400,000 volume')
    count = 0
    for stock in sorted_stocks:
        if stock['symbol'] not in CONSTANT_STOCKS and stock['symbol'] not in excluded_stocks and count < number_to_look_for and stock['symbol'] not in EXCLUDED_STOCKS:
            print(f"Symbol: {stock['symbol']}, Percent Change: {stock['percent_change']}, Volume: {stock['volume']}")
            top_stocks.append(stock['symbol'])
            count += 1

    print()

    # Quit the webdriver
    driver.quit()

    return top_stocks
