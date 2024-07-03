import scraping
from deap import base, creator, tools, algorithms
import random




class recomend_acttion:

    sell = []
    buy = []

    def reset(self):
        # This function resets the class-level array
        self.buy = []
        self.sell = []


    def add_to_buy(self, symbol):
        # This function adds an element to the class-level array
        self.buy.append(symbol)

    def add_to_sell(self, symbol):
        # This function adds an element to the class-level array
        self.sell.append(symbol)


    def get_buy(self):
        # This function returns the current state of the array
        return self.buy

    def get_sell(self): 
        # This function returns the current state of the array
        return self.sell


class strategy:


    """


    A class representing a trading strategy.



    Attributes:


    - avg_price (float): The average price of the asset.


    - top_percent_from_portfolio (float): The top percentage of the portfolio to consider for trading.


    - loss_percent (float): The percentage below the average price to set as the stop loss.


    - profit_percent (float): The percentage above the average price to set as the stop profit.



    Methods:


    - __init__(avg_price, top_percent_from_portfolio, loss_percent, profit_percent, **kwargs): Initializes the strategy object.


    - __str__(): Prints the attributes of the strategy object.


    - optimize(): Optimizes the strategy using a genetic algorithm.


    - adx_rsi(): Looks for potential trades based on ADX and RSI indicators.


    """
    


    def __init__(self, avg_price, top_percent_from_portfolio=0.05, loss_percent=0.05, profit_percent=0.2, **kwargs):


        self.avg_price = avg_price


        self.top_percent_from_portfolio = top_percent_from_portfolio


        self.loss_percent = loss_percent


        self.profit_percent = profit_percent


        # Set stoploss and stopprofit based on avg_price and the respective percents


        self.stoploss = self.avg_price * (1 - self.loss_percent)


        self.stopprofit = self.avg_price * (1 + self.profit_percent)


        # Process additional keyword arguments if necessary


        for key, value in kwargs.items():


            setattr(self, key, value)



    def __str__(self):


        """


        Prints the attributes of the strategy object.


        """


        for key, value in self.__dict__.items():


            if key and value:


                print(f'{key}: {value}')



    def simulate_trading(self, prices, cash=10000, commission=0.01):


        """


        Simulates trading based on the strategy.



        This function simulates trading based on the strategy and returns the final cash balance.


        """
            
    
        for price in prices:
            if price <= self.stoploss or price >= self.stopprofit:
                    # Close the position
                    cash += price
            else:
                    # Check if the position exceeds the top percent from the portfolio
                if (price / cash) >= self.top_percent_from_portfolio:
                    # Minimize the position
                    minimize_by = (price / cash) - self.top_percent_from_portfolio
                    cash -= price * minimize_by

                    #use the class methods strategy.buy and strategy.sell to get the symbols to buy and sell
        return cash


    def optimize(self):


        """


        Optimizes the strategy using a genetic algorithm.


        """
        pass



    def adx_rsi(self):


        """


        Look for potential trades.



        This function iterates over the companies in the database and checks if the conditions for a trade are met.


        If the conditions are met, it prints 'buy'.


        """
        

        for compeny in database.get_compenies():


            df = compeny.get_df()


            if 30 <= df['ADX'].iloc[-1] <= 50:


                if 30 <= df['RSI'].iloc[-1] <= 70:


                    interval, state, predction, probability = compeny.probability_of_returns('1h')


                    Dinterval, Dstate, Dpredction, Dprobability = compeny.probability_of_returns('1h')


                    if state == 'positive' and Dstate == 'positive':


                        if probability > 0.6 and Dprobability > 0.6:


                            if compeny.symbol not in self.buy:


                                recomend_acttion.add_to_buy(compeny.symbol)
                        


                elif df['RSI'].iloc[-1] > 70:


                    #  is overbought


                    if compeny.symbol not in self.sell:


                        recomend_acttion.add_to_sell(compeny.symbol)
                    



# Define the evaluation function


def evaluate(strategy, prices):


    return strategy.simulate_trading(prices),

def anlayze(symbol):
    # This function analyzes a symbol and takes appropriate actions
    pass


def optimize_strategy_ga(prices):


    # Define the individual and population


    creator.create("FitnessMax", base.Fitness, weights=(1.0,))


    creator.create("Individual", list, fitness=creator.FitnessMax)



    toolbox = base.Toolbox()


    toolbox.register("attr_float", random.random)


    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, 4)


    toolbox.register("population", tools.initRepeat, list, toolbox.individual)



    # Register the genetic algorithm operators


    toolbox.register("mate", tools.cxBlend, alpha=0.5)


    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)


    toolbox.register("select", tools.selTournament, tournsize=3)


    toolbox.register("evaluate", evaluate, prices=prices)



    population = toolbox.population(n=100)


    hof = tools.HallOfFame(1)



    # Run the genetic algorithm


    algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=40, stats=None, halloffame=hof, verbose=True)



    return hof[0]


#example


# strategy1 = strategy(avg_price=100, top_precent_from_protfolio=0.05, loss_precent=0.05, profit_precent=0.2, Adx_open=0.3 , Adx_close=0.5 , RSI_short=0.7, RSI_long=0.3)


# print(strategy1.stoploss)