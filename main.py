import Traiding_custamer
from functions import calculate_rsi
stock = Traiding_custamer.compeny('apple', 'AAPL')
rsi = calculate_rsi(stock.get_df)
print(stock.probability_of_returns())
# stock.show

# print(rsi)