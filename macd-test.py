#!/usr/bin/env python3

import pandas_datareader as pdr
import datetime as dt
start = dt.datetime(2020, 1, 1)
end = dt.datetime.now()
ticker = pdr.get_data_yahoo("AAPL", start, end)['Adj Close']
print(ticker)

pdr.DataFrame()

exp1 = ticker.ewm(span=12, adjust=False).mean()
exp2 = ticker.ewm(span=26, adjust=False).mean()
macd = exp1 - exp2
exp3 = macd.ewm(span=9, adjust=False).mean()

macd.plot(label='AAPL MACD', color='g')
ax = exp3.plot(label='Signal Line', color='r')
ticker.plot(ax=ax, secondary_y=True, label='AAPL')

ax.set_ylabel('MACD')
ax.right_ax.set_ylabel('Price $')
ax.set_xlabel('Date')
lines = ax.get_lines() + ax.right_ax.get_lines()
ax.legend(lines, [l.get_label() for l in lines], loc='upper left')
