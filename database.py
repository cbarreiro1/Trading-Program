import sqlite3
from datetime import datetime

def update_stock_data_to_database(symbol: str, latest_price: float, latest_macd, latest_signal, macd_crossover: bool):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create the stock_data table if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS stock_datas
                      (symbol TEXT, latest_price REAL, latest_macd REAL,
                       latest_signal REAL, macd_crossover BOOLEAN, timestamp TEXT,
                       PRIMARY KEY (symbol, timestamp))''')

    cursor.execute('''INSERT INTO stock_data (symbol, latest_price, latest_macd, latest_signal, macd_crossover, timestamp)
                      VALUES (?, ?, ?, ?, ?, ?)''', (symbol, latest_price, latest_macd, latest_signal, macd_crossover, timestamp))

    conn.commit()
    conn.close()

def sort_stock_data_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the stock_data table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stock_data'")
    table_exists = cursor.fetchone()

    if table_exists:
        # Retrieve all data from the stock_data table
        cursor.execute('SELECT * FROM stock_data')
        data = cursor.fetchall()

        # Sort the data by symbol and then within each symbol, sort by timestamp
        sorted_data = sorted(data, key=lambda x: (x[0], x[4]))

        # Clear the existing data from the stock_data table
        cursor.execute('DELETE FROM stock_data')

        # Insert the sorted data back into the stock_data table
        cursor.executemany('''INSERT INTO stock_data (symbol, latest_price, latest_macd, latest_signal, timestamp)
                              VALUES (?, ?, ?, ?, ?)''', sorted_data)

        conn.commit()
    else:
        print("stock_data table does not exist in the database.")

    conn.close()

def update_stock_database(stock_symbols:list):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the stock_status table if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS stock_status
                      (symbol TEXT, timestamp TEXT,
                       PRIMARY KEY (symbol, timestamp))''')

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rows = [(symbol, timestamp) for symbol in stock_symbols]

    for row in rows:
        cursor.execute('INSERT INTO stock_status (symbol, timestamp) VALUES (?, ?)', row)

    conn.commit()
    conn.close()

def sort_stock_status_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the stock_status table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stock_status'")
    table_exists = cursor.fetchone()

    if table_exists:
        # Sort the table based on symbol and timestamp
        cursor.execute('SELECT * FROM stock_status ORDER BY symbol, timestamp')
        sorted_rows = cursor.fetchall()

        # Clear the existing data in the table
        cursor.execute('DELETE FROM stock_status')

        # Insert the sorted rows back into the table
        cursor.executemany('INSERT INTO stock_status (symbol, timestamp) VALUES (?, ?)', sorted_rows)

        conn.commit()
    else:
        print("stock_status table does not exist in the database.")

    conn.close()

def delete_table(table_name:str):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(f'DROP TABLE IF EXISTS {table_name}')

    conn.commit()
    conn.close()

def update_macd_database(stocks:list=None, stock:str=None, crossover:bool=False):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the macd_crossover table if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS macd_crossover
                    (symbol TEXT PRIMARY KEY, crossed BOOLEAN)''')
    
    if stocks is not None:
        # Insert or update rows for each symbol in the dictionary
        for symbol in stocks:
            cursor.execute('INSERT OR IGNORE INTO macd_crossover (symbol, crossed) VALUES (?, ?)', (symbol, crossover))

        # Delete rows for symbols that are no longer in use
        symbols_in_use = set(stocks)
        cursor.execute('SELECT symbol FROM macd_crossover')
        existing_symbols = set(row[0] for row in cursor.fetchall())
        symbols_to_delete = existing_symbols - symbols_in_use
        for symbol in symbols_to_delete:
            cursor.execute('DELETE FROM macd_crossover WHERE symbol = ?', (symbol,))

    elif stock is not None:
        # Insert or update the row for the specified stock
        cursor.execute('UPDATE macd_crossover SET crossed = ? WHERE symbol = ?', (crossover, stock))

    conn.commit()
    conn.close()

def get_macd_crossover_from_database() -> dict:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Retrieve the MACD crossover data from the database
    cursor.execute('SELECT * FROM macd_crossover')
    rows = cursor.fetchall()

    # Create a dictionary to store the MACD crossover data
    macd_crossover = {}
    for row in rows:
        symbol, crossed = row
        macd_crossover[symbol] = bool(crossed)

    conn.close()

    return macd_crossover
