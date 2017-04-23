import time

class hk_trader_placer:

    def __init__(self, ma, opt):
        self.ma = ma
        self.opt = opt

    def get_quato(self):
        self.ask = 0
        self.bid = 0
        while( self.ask == 0 or self.bid == 0):
            self.ask, self.bid = self.ma.get_get_ask_bid()
            time.sleep(0.2)

    def buy(self, qty, stock_str):
        self.get_quato()
        print(str(self.ask - self.bid))
        if self.ask * 1000 - self.bid * 1000 == 1:
            self.opt.buy(self.ask, qty, stock_str)
        if self.ask * 1000 - self.bid * 1000 == 2:
            self.opt.buy(self.ask - 0.001, qty, stock_str)
        if self.ask * 1000 - self.bid * 1000 > 2:
            print("should not buy")
            return -1
        return 0

