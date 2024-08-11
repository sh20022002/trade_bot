# SmarTraid
# making Algo Trading more accessible.

__trading system__

I created a system with a bot and a paper trading system that uses a microservices approuch, that bot contiosly chack s&p500 compenys and open postions for capitalazing on market flactuations of stocks using a models to predict prices and the probability of the prediction and uses different quant trading methods to find each stock its best strategy useing genetic algoritham optimazition the data is gatherd by scraping the models and costumer data are stored in a database servies and all system actions are rund in the server.


the system is seprated to 3 serviecies a database server the server and the client side.

1. the database is a mongo db instance build with:
    - stocks-consumer collection that

    - stocks collection

    - clients collection

    - models collection
    
    - transaction collection
  
2. the server is writen in python with:
    - scrapping module with scrapping methods for fetching compeny data, historical stock data, exchange rate and more..
  
    - a client handeling module with a user class and paper trade user info and account methods has a datbase sync method.
  
    - the compeny moduale with the compeny class and methods.
  
    - the database with the database methods in pymongo.
  
    - the function module with data pipline methods for calculating stock indicaitors.
  
    - a mail agent for sending stock recomadations.
  
    - main with the bot funcinalties thats runs in peralel with the server.
  
    - plots with the plotly stock ploting.
  
    - run uses subprocess to run the server and the bot stock scanner in peralel.
  
    - server with the socket handeling uses ssl for secure TCP communactions.
  
    - strategy with the strategies that are the prerequisites for the scanner conditions and Genetic Algoritham for optimazining the strategys per stock and adjast the parameters.
  
    - predictions fetchs the traind prediction models and makes a predictions for day and hour intervals for stock price change and probability useing Markov Model and Reggrasion Model.
  
    - tranining module trains the models for each intervals and for Markov Model also per stock symbol and if the stock is traind trains it up to date.
  
    - transactions class and methods
      
   
3. client side
   - uses streamlit for a backend focuos project
     pages:
         - loging page has a key resrictaions for script injection prevantions

         - register page ask for all relevent data for trading in with a brokrege in the futare.
         - app with options to plot all stocks and all open postions and more.

   - client for client server communactions











__tecnical indicaters in use__
sma - [50, 100, 200] the simple moving average of the price of the stock add the [50, 100, 200] last days pricers and devide by the number of days [50, 100,200]

ema - exponential moving average == (today_value * (smoothing/ 1 + days))
+ yesterday_ema * (1 - (smothing / 1 + days))
the exponential change in value


rsi -(Relative Strength Index)  RSI measures the speed and magnitude of a security's recent price
 1 - 100 - [100 / [1+ avg gain/ avg loss]]
 2 - 100 - [100 / [1 + prev avg gain * 13 + currnt gain / prev loss * 13 + current loss]]

 tr - ( True Range) The distance from today's high to today's low

 trx - (The average directional index) determine the strength of a trend.


__uses of ai in trading__

 1 - Predictive modeling: One of the most common uses of machine learning in the stock market is for predictive modeling. This involves using historical data to train a model that can predict future stock prices. This can be useful for investors who want to identify potential opportunities for buying or selling stocks.

2 - Algorithmic trading: Algorithmic trading is the use of computer programs to execute trades automatically based on certain predetermined rules. Machine learning algorithms can be used to optimize these rules and make more accurate predictions, which can lead to more profitable trades.

3 - Portfolio optimization: Machine learning can also be used to optimize a portfolio of stocks. This can include identifying the best stocks to invest in and determining the optimal allocation of assets.


4 - 
Risk management: Machine learning can also be used to identify potential risks associated with a particular stock or portfolio. This can help investors make more informed decisions and manage their risk more effectively.

__implemented strategies__
1. Mean Reversion Trading:
Concept: This strategy assumes that asset prices will revert to their historical average or mean over time.
Python Implementation: Use statistical techniques such as Bollinger Bands or the Relative Strength Index (RSI) to identify overbought or oversold conditions.

2. Trend Following:
Concept: This strategy relies on identifying and following the prevailing market trends.
Python Implementation: Utilize moving averages or trend indicators like the Moving Average Convergence Divergence (MACD) to detect trends and generate buy/sell signals.


3. Machine Learning-Based Strategies:
Concept: Use advanced machine learning algorithms to analyze market data and make trading decisions.
Python Implementation: Implement machine learning models such as decision trees, random forests, or neural networks for predicting price movements.

4. Volatility Trading:
Concept: Exploit changes in market volatility to make trading decisions.
Python Implementation: Calculate historical volatility, use options strategies like straddle or strangle, or implement the Volatility Index (VIX) as a trading signal.

5. Momentum Trading:
Concept: Capitalize on the continuation of existing trends by entering trades in the direction of the prevailing momentum.
Python Implementation: Use momentum indicators like the Relative Strength Index (RSI) or rate of change (ROC) to identify strong trends and generate buy/sell signals.

8. Event-Driven Strategies:
Concept: Trade based on specific events, such as earnings announcements or economic releases.
Python Implementation: Develop algorithms that react to predefined events, leveraging sentiment analysis or natural language processing to assess news and social media sentiment.
