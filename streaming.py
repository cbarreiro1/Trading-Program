from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from config import WEBDRIVER_PATH, CONSTANT_STOCKS

def get_top_stocks() -> list:
    # Configure the webdriver (make sure you have the appropriate driver executable installed)
    options = Options()
    options.add_argument(WEBDRIVER_PATH)
    driver = webdriver.Chrome(options=options)

    # Load the Benzinga premarket page
    driver.get('https://www.benzinga.com/premarket')

    # Wait for the Gainers table to load
    time.sleep(2)  # Add a delay to allow the page to load
    gainers_table = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="bz-gainers-table"]')))
    gainers_rows = gainers_table.find_elements(By.XPATH, './/tbody/tr')

    # Create a list to store the stock data
    stocks = []

    # Iterate over the Gainers table rows and extract symbol and percent change values
    for row in gainers_rows:
        symbol = row.find_element(By.XPATH, './td[1]').text
        percent_change = row.find_element(By.XPATH, './td[4]').text
        percent_change = percent_change.strip('%').replace('$', '')  # Remove '%' and '$' characters
        stocks.append({'symbol': symbol, 'percent_change': percent_change})

    # Sort the stocks based on percent change in descending order
    sorted_stocks = sorted(stocks, key=lambda stock: float(stock['percent_change'].strip('%')), reverse=True)
    top_stocks = []

    # Print the top 3 stocks with the highest percent change (excluding those in CONSTANT_STOCKS)
    print(f'Current Top Stocks Based on % Change')
    count = 0
    for stock in sorted_stocks:
        if stock['symbol'] not in CONSTANT_STOCKS and count < 3:
            print(f"Symbol: {stock['symbol']}, Percent Change: {stock['percent_change']}")
            top_stocks.append(stock['symbol'])
            count += 1

    print()

    # Quit the webdriver
    driver.quit()

    return top_stocks
