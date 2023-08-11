import sqlite3
from datetime import datetime

# Adds given stock data to its own table
def update_stock_data_table(symbol:str, latest_price:float, latest_macd:float, latest_signal:float, macd_crossover:bool,
                            macd_line_over_signal:bool, macd_line_over_zero:bool, macd_crossed_over_signal:bool, 
                            macd_crossed_over_zero:bool):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create a table with the stock symbol as the name
    table_name = f'stock_{symbol}'
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}
                      (latest_price REAL, latest_macd REAL,
                       latest_signal REAL, macd_crossover BOOLEAN, macd_line_over_signal BOOLEAN,
                       macd_line_over_zero BOOLEAN, macd_crossed_over_signal BOOLEAN, macd_crossed_over_zero BOOLEAN,
                       timestamp TEXT, PRIMARY KEY (timestamp))''')

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insert the provided data along with the current timestamp
    cursor.execute(f'''INSERT INTO {table_name} (latest_price, latest_macd, latest_signal, macd_crossover,
                      macd_line_over_signal, macd_line_over_zero, macd_crossed_over_signal, macd_crossed_over_zero,
                      timestamp)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (latest_price, latest_macd, latest_signal, macd_crossover,
                                                            macd_line_over_signal, macd_line_over_zero,
                                                            macd_crossed_over_signal, macd_crossed_over_zero, timestamp))

    conn.commit()
    conn.close()


# Deletes every table in a given database
def delete_all_tables_in_database(database_name:str):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Get the list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Drop each table one by one
    for table in tables:
        table_name = table[0]
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

    conn.commit()
    conn.close()

# Now, you can call the functions appropriately when you need them.


# Updates the if the MACD has crossed over for the stocks being searched for
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

# Returns a dictionary with data from the MACD crossover table
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
