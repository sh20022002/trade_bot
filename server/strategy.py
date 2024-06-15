class strategy:
    def __init__(self, symbol, action, value, amount, total_price, date, *args, **kwargs):
        self.symbol = symbol
        self.action = action
        self.value = value
        self.amount = amount
        self.total_price = total_price
        self.Volume = None
        self.TR = None
        self.Adx = None
        self.klass_vol = None
        self.RSI = None
        self.SMA_20 = None
        self.SMA_50 = None
        self.SMA_100 = None
        self.EMA = None
        self.stoploss = None
        self.stopprofit = None
        self.daily_predction = None
        self.hourly_prediction = None
        self.hmm_daily_state = None
        self.hmm_daily_probability = None
        self.hmm_horly_state = None
        self.hmm_horly_probability = None
        self.top_precent_from_protfolio = None

    def optimaize(self, symbol, action, value, amount, total_price, date):
        self.symbol = symbol
        self.action = action
        self.value = value
        self.amount = amount
        self.total_price = total_price        

    