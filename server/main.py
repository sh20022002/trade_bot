import scrapping, database, server
import time
import strategy
def main():
    """
    The main function of the trade bot.

    This function initializes the database, checks for open positions, and looks for trades.
    It runs in a loop while the NYSE is open, with a delay of one hour between iterations.
    """
    # initialize the database
    initialize()
    hour = 60 * 60
    recmondation =  strategy.recomend_acttion
    while scrapping.is_nyse_open():
        chack_open_positions()
        recmondation.reset()
        strategy.adx_rsi()
        
        
        time.sleep(hour)


def chack_open_positions(user):
    """
    Check open positions for potential actions.

    This function iterates over the open positions of a user and checks if any actions need to be taken.
    If the current price of a position is below the stoploss or above the stopprofit, the position is closed.
    If the current total price of a position exceeds a certain percentage of the user's stock value, the position is minimized.
    """
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

        if df['ADX'].iloc(-1) > 50 and df['RSI'].iloc(-1) > 60:# end  of trend adx around 50
            #end of trend rsi around 70
            
            user.close_position(position)

def initialize():
    """
    Initialize the database.

    This function initializes the database by saving the S&P 500 companies and their information.
    It returns a list of the saved companies.
    """
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