import Traiding_custamer
from functions import calculate_rsi
stock = Traiding_custamer.compeny('asts', 'ASTS')
rsi = calculate_rsi(stock.get_df)
stock.probability_of_returns()
# stock.show

print(rsi)