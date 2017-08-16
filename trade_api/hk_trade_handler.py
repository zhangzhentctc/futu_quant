import threading
import time
import math

class hk_trade_handler(threading.Thread):

    ## BUY:  CMD = 0
    ## SELL: CMD = 1
    def __init__(self, hk_trade_opt, stock_quote, stock_code,  cmd = 1, qty = -1, type = 0):
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
                        ## If it is simulation
                        if self.hk_trade_opt.envtype == 1:
                            break
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

                    ## Sell Forcely
                    # sell to bid 1
                    # wait 2s
                    # sell to bid 1

    def buy_bear_force_sell_half(self, stock_code, qty0):
        status = 1
        qty = qty0
        wait_bad_quote = 20
        dealt_ask = 0
        while status != 0:
            print("Force Buy")
            bear_bid = self.stock_quote.get_bear_bid()
            bear_ask = self.stock_quote.get_bear_ask()
            print(bear_bid, bear_ask)
            if bear_ask * 1000 - bear_bid * 1000 <= 2:
                localid = self.hk_trade_opt.buy_stock_code_qty(stock_code, bear_ask, qty)
                dealt_ask = bear_ask
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
                        ## If it is simulation
                        if self.hk_trade_opt.envtype == 1:
                            break
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
                    print("Bad Bear Quoto")
                else:
                    time.sleep(0.5)
                    wait_bad_quote -= 1

        ## BUY END
        ## Sell half
        ## 1. Get Position0
        ## 2. Wait until no position -> quit OR
        ##    bid == dealt_ask + 1 -> sell
        ## 3.LOOP
        status = 1

        ## Get Sell Qty
        position0 = self.hk_trade_opt.query_position_stock_qty(self.stock_code)
        if position0 == -1 or position0 == 0:
            print("No Position")
            if self.hk_trade_opt.envtype != 1:
                return -1

        sell_pencil = math.ceil((int(position0)/10000)/2)
        sell_qty = sell_pencil * 10000
        qty = sell_qty
        print("SELL QTY:", sell_qty)
        while status != 0:
            bear_bid = self.stock_quote.get_bear_bid()
            if bear_bid * 1000 - dealt_ask * 1000 >= 1 :
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
                        ## If it is simulation
                        if self.hk_trade_opt.envtype == 1:
                            break
                        return -1
                    # new qty
                    qty -= dealt_qty
                    status = 2
                elif ret == 0:
                    status = 0
                else:
                    return -1
            else:
                time.sleep(0.3)

            # Check Position
            position = self.hk_trade_opt.query_position_stock_qty(self.stock_code)
            if position == -1 or position == 0:
                print("No Position")
                break
        ## While End
        return


    def run(self):
        ## Sell Task
        if self.cmd == 1:
            if self.qty == -1:
                qty = self.hk_trade_opt.query_position_stock_qty(self.stock_code)
                if qty == -1 or qty == 0:
                    print("No Position")
                self.qty = qty
            self.sell_bear_force(self.stock_code, self.qty)

        ## Buy Task
        if self.cmd == 0:
            if self.qty == -1:
                print("Please specify Buy Quantity!")
                return
            else:
                self.buy_bear_force_sell_half(self.stock_code, self.qty)

