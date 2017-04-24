import time

# Placer for one order
class hk_trader_placer:

    def __init__(self, ma, opt, type):
        self.ma = ma
        self.opt = opt
        self.type = type

    def get_quato(self):
        ask = 0
        bid = 0
        while( ask == 0 or bid == 0):
            ask, bid = self.ma.find_ask_bid(self.type)
            time.sleep(0.2)
        return ask, bid

    def buy_on_market_price(self, qty, stock_str):
        ask, bid = self.get_quato()
        print(str(ask - bid))
        if ask * 1000 - bid * 1000 == 0:
            print("quato error")
        if ask * 1000 - bid * 1000 == 1:
            self.opt.buy(ask, qty, stock_str)
        if ask * 1000 - bid * 1000 == 2:
            self.opt.buy(ask - 0.001, qty, stock_str)
        if ask * 1000 - bid * 1000 == 3:
            self.opt.buy(ask - 0.001, qty, stock_str)
        if ask * 1000 - bid * 1000 > 2:
            print("should not buy")
            return -1
        return 0

# assume buy all qty
    def sell_on_market_price(self, qty, stock_str):
        ask, bid = self.get_quato()
        print(str(ask - bid))
        if ask * 1000 - bid * 1000 == 0:
            print("quato error")
        if ask * 1000 - bid * 1000 == 1:
            self.opt.sell(bid, qty, stock_str)
        if ask * 1000 - bid * 1000 == 2:
            self.opt.sell(bid + 0.001, qty, stock_str)
        if ask * 1000 - bid * 1000 == 3:
            self.opt.sell(bid + 0.002, qty, stock_str)
        if ask * 1000 - bid * 1000 > 2:
            print("should not buy")
            return -1
        return 0
