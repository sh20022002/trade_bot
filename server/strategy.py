import scraping
from deap import base, creator, tools, algorithms
import random

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

    def simulate_trading(self, prices):
        """
        Simulates trading based on the strategy.

        This function simulates trading based on the strategy and returns the final portfolio value.
        """
        pass

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
                        yield 'buy', compeny.symbol
                elif df['RSI'].iloc[-1] > 70:
                    #  is overbought
                    yield 'sell', compeny.symbol

# Define the evaluation function
def evaluate(strategy, prices):
    return strategy.simulate_trading(prices),


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

strategy1 = strategy(avg_price=100, top_precent_from_protfolio=0.05, loss_precent=0.05, profit_precent=0.2, Adx_open=20, Adx_close=30, RSI_short=30, RSI_long=70)
strategy1.__str__()