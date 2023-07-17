from config import update_macd_dict, add_stocks

dict = {'a': True,
        'b': False
        }

list = ['a', 'b', 'c', 'd']
list2 = ['a', 'd', 't', 'd', 's']

update_macd_dict(dict, list)

def add5(int):
    int + 5

int = 7
add5(int)
print(int)

add_stocks(list, list2)
print(list)

print(dict)