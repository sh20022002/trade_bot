# traiding_impl

trading system 
















___tecnical_indicaters___
sma - [50, 100, 200] the simple moving average of the price of the stock add the [50, 100, 200] last days pricers and devide by the number of days [50, 100,200]

ema - exponential moving average == (today_value * (smoothing/ 1 + days))
+ yesterday_ema * (1 - (smothing / 1 + days))
the exponential change in value


rsi -(Relative Strength Index)  RSI measures the speed and magnitude of a security's recent price
 1 - 100 - [100 / [1+ avg gain/ avg loss]]
 2 - 100 - [100 / [1 + prev avg gain * 13 + currnt gain / prev loss * 13 + current loss]]

 tr - ( True Range) The distance from today's high to today's low

 trx - (The average directional index) determine the strength of a trend.