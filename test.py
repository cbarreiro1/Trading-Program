from strategies import *

macd_over_signal = False
macd_over_zero = False
macd_crossed_over_signal = False
macd_crossed_over_zero = False

true_count = sum([macd_over_signal, macd_over_zero, macd_crossed_over_signal, macd_crossed_over_zero])

print(true_count)

values = [False, False]
print(has_macd_crossed_over_zero(values))
values = [False, True]
print(has_macd_crossed_over_zero(values))
values = [True, False]
print(has_macd_crossed_over_zero(values))
values = [True, True]
print(has_macd_crossed_over_zero(values))
