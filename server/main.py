import scrapping, database, server
import time

def main():
    # initialize the database
    initialize()
    hour = 60 * 60

    while scrapping.is_nyse_open():
        chack_open_positions()
        look_for_trades()
        
        time.sleep(hour)


def look_for_trades():
    for compeny in database.get_compenies():
        df = compeny.get_df()
        if df['ADX'].iloc[-1] > compeny.strategy.Adx_open and df['ADX'].iloc[-1] < compeny.strategy.Adx_close:
            if df['RSI'].iloc[-1] <= compeny.strategy.RSI_short and df['RSI'].iloc[-1] >= compeny.strategy.RSI_long:
                        interval, state, predction, probability = compeny.probability_of_returns('1h')
                        Dinterval, Dstate, Dpredction, Dprobability = compeny.probability_of_returns('1h')
                        if state == 'positive' and Dstate == 'positive':
                            print('buy')

                                                   

def chack_open_positions(user):
    for position in user.open_positions:
        #chack all open positions for the transaction symbol
        avg_price = position.value
        # df with all the data of the stock 
        df = position.compeny.get_df()
        # close of last hour
        current_price = scrapping.current_stock_price(position.symbol)
        # percent change from the price when the position was open
        prcet_change = (current_price - avg_price) / avg_price
        current_total_price = current_price * position.amount
        time_in_position = scrapping.get_exchange_time() - position.date
        if current_price <= position.strategy.stoploss or current_price >= position.strategy.stopprofit:
            user.close_position(position)
        else:
            if (current_total_price / user.stock_value)>= user.strategy.top_precent_from_protfolio:
                minimizeby = (current_total_price / user.stock_value) - user.strategy.top_precent_from_protfolio
                user.minimize(position, minimizeby)

        if df['ADX'].iloc(-1) > position.strategy.adx and df['RSI'].iloc(-1) > position.strategy.rsi:# end  of trend adx around 50
            #end of trend rsi around 70
            
            user.close_position(position)
def initialize():
    # initialize the database
    sp500_compenies = scraping.get_tickers()

    # Index(['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry',

        #    'Headquarters Location', 'Date added', 'CIK', 'Founded']

    compenies = []

    for i in range(2):

        # print(sp500_compenies.index)

        compenies.append(sp500_compenies[1][i])

        compeny = server.compeny(sp500_compenies[2][i], sp500_compenies[1][i])

        compeny.GICS_Sector = sp500_compenies[3][i]

        compeny.GICS_Sub_Industry = sp500_compenies[4][i]

        compeny.Location = sp500_compenies[5][i]

        compeny.CIK = sp500_compenies[6][i]

        compeny.Founded = sp500_compenies[7][i]
        
        database.save_compeny(compeny)

    return compenies