import scraping

class strategy:
    def __init__(self, symbel, *args, **kwargs):
        self.symbol = symbel
        self.Adx_open = None
        self.Adx_close = None
        # self.klass_vol = None
        self.RSI_short = None # around 70
        self.RSI_long = None # around 30
        self.SMA_20 = None #
        self.SMA_50 = None #
        self.SMA_100 = None # true of false
        self.EMA = None
        self.stoploss = None
        self.stopprofit = None
        self.positive_daily_predction = None
        self.positive_hourly_prediction = None
        self.hmm_daily_state = None
        self.hmm_daily_probability = None
        self.hmm_horly_state = None
        self.hmm_horly_probability = None
        self.top_precent_from_protfolio = None

    def optimaize(self):
       #the hmm states ['negative', 'neutral', 'positive']
       pass

    