'''all oop(object orianted programing) uses and there functions'''


from scraping import get_stock_sum, current_stock_price
from functions import summery ,add_all , calculate_hourly_returns
from plots import plot_stock
import database
from training import train_hmm
from prediction import predict_next_state_and_probabilities, stock_and_tecnical, predict_next_close



class Compeny:
    def __init__(self, compeny_name, symbol, *args, **kwargs):
        self.compeny_name = compeny_name
        self.symbol = symbol
        self.GICS_Sector = None
        self.GICS_Sub_Industry = None
        self.CIK = None
        self.Founded = None
        self.Location = None
        self.summery = None#get_stock_sum('short\long-none\sma\50\100\200-none\pricer-none\price-prediction')
        self.price = current_stock_price(self.symbol)
        self.last_price = None
        self.sentiment = None
        
        
        
        
    
    
    def get_df(self, DAYS=365, interval='1h'):
        """
        Get the stock data for the company.

        Args:
        - DAYS (int, optional): The number of days of data to retrieve.

        Returns:
        - DataFrame: The stock data for the company.
        """
        df = stock_and_tecnical(self.symbol, interval=interval)
        return df


    @property
    def show(self, interval, columns):
        """
        Show the stock data for the company.
        """
        plot_stock(self.get_df(interval=interval), self.compeny_name, columns, show='all', interval=interval)



    def probability_of_returns(self, interval):
        """
        Calculate the probability of future stock returns using the HMM model.
        """
        # needs a function to refit the hmm model

        df = self.get_df(interval=interval)
        df = add_all(df)
        current_return = df['Close'][0] - df['Close'][1]
        hmm = database.get_hmm_model(self.symbol, interval=interval)
        if(hmm == None):
            model = train_hmm(self.symbol, df)
        else:
            model = hmm
        state, probability = predict_next_state_and_probabilities(current_return, self.symbol)

        prediction = predict_next_close(self.symbol, self.get_df(interval=interval))
        
        return interval, state, prediction, probability

# for now no use for database because of the small amount data and the need for it to be updated frquantly
# if will be used for more then one costomer will need a database and methods to update all data frequantly 
# and there will be an advange for bigger usege doo to the better accessing times and aficcentce to run and grow
# --needs an updated aprouch for scallability
    
    
    def add_stock(self, compeny_name, symbol, summery):
        """
        Add a stock to the database.

        Args:
        - compeny_name (str): The name of the company.
        - symbol (str): The symbol of the stock.
        - summery (str): The summary of the stock.

        Returns:
        - str: A string representing the result of adding the stock.
        """
        stock = compeny(self, compeny_name, symbol, summery)
        database.insert_stock(compeny_name, symbol)
        return f'added {compeny_name}.'
    
    def del_stock(self):
        """
        Remove the stock from the database.

        Returns:
        - str: A string representing the result of removing the stock.
        """
        r = database.remove_from_db(self.symbol)
        return f'{self.compeny_name} removed from database!'
        