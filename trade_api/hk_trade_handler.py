import threading
import time


class hk_trade_handler(threading.Thread):
    def __init__(self, hk_trade_opt, stock_quote, stock_code,  cmd = 0, type = 0, qty = -1):
        super(hk_trade_handler, self).__init__()
        self.hk_trade_opt = hk_trade_opt
        self.stock_quote = stock_quote
        self.stock_code = stock_code
        self.qty = qty
        self.cmd = cmd
        self.type = type

## Sell Forcely
# sell to bid 1
# wait 2s
# sell to bid 1
    def sell_bear_force(self, stock_code, qty0):
        status = 1
        qty = qty0
        wait_bad_quote = 20
        while status != 0:
            print("Force Cell")
            bear_bid = self.stock_quote.get_bear_bid()
            bear_ask = self.stock_quote.get_bear_ask()
            print(bear_bid, bear_ask)
            if bear_ask * 1000 - bear_bid * 1000 <= 2:
                localid = self.hk_trade_opt.sell_stock_code_qty(stock_code, bear_bid, qty)
                if localid == -1:
                    return -1
                time.sleep(1)

                # status = 2 when not all dealt
                # status = 0 when all dealt
                ret = self.hk_trade_opt.check_dealt_all(localid)
                if ret == -1:
                    # if not all dealt, get dealt and delete order
                    dealt_qty = self.hk_trade_opt.get_dealt_qty_localid_and_recall(localid)
                    if dealt_qty == -1:
                        return -1
                    # new qty
                    qty -= dealt_qty
                    status = 2
                elif ret == 0:
                    status = 0
                else:
                    return -1
            else:
                if wait_bad_quote == 0:
                    return -1
                else:
                    time.sleep(0.5)
                    wait_bad_quote -= 1

    def run(self):
        if self.qty == -1:
            qty = self.hk_trade_opt.query_position_stock_qty(self.stock_code)
            if qty == -1 or qty == 0:
                print("No Position")
            self.qty = qty
        self.sell_bear_force(self.stock_code, self.qty)
