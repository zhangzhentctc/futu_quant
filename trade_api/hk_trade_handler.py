import threading
import time
import math

STATUS_IDLE = 0
STATUS_WAIT_OPEN = 4
STATUS_BEAR_FORCE_SELL = 1
STATUS_BEAR_FORCE_BUY = 2
STATUS_BEAR_WAIT_PROFIT = 3

STATUS_BULL_FORCE_SELL = 5
STATUS_BULL_FORCE_BUY = 6
STATUS_BULL_WAIT_PROFIT = 7

class hk_trade_handler(threading.Thread):
## Single Class
## Status:
##    1. bear force sell -> idle
##         Change: Signal from outside
##          Input: Signal
##            Get: Position, bear_quoto
##    2. bear force buy -> bear wait profit
##         Change: Signal from outside
##          Input: Signal, Quantity
##            Get: bear_quoto
##    3. bear wait 1 profit -> idle
##         Change: After bear force buy succeed
##          Input: Signal
##            Get: Position, bear_quoto
##


    ## BUY:  CMD = 0
    ## SELL: CMD = 1
    def __init__(self, hk_trade_opt, stock_quote, bull_code, bear_code,  cmd = 1, qty = -1, type = 0):
        super(hk_trade_handler, self).__init__()
        self.hk_trade_opt = hk_trade_opt
        self.stock_quote = stock_quote
        self.stock_code = 0
        self.qty = qty
        self.cmd = cmd
        self.type = type

        self.status = STATUS_WAIT_OPEN
        self.buy_qty = 0
        self.wait_profit_qty_ratio = 0
        self.dealt_ask = 0

        self.bear_code = bear_code
        self.bull_code = bull_code

        self.busy = 0

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
                    qty -= int(dealt_qty)
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
                    qty -= int(dealt_qty)
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
                    qty -= int(dealt_qty)
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

    def bear_force_sell(self):
        if self.status != STATUS_WAIT_OPEN:
            self.status = STATUS_BEAR_FORCE_SELL

    def bear_force_buy(self, qty, wait_profit_ratio = 0.5):
        if self.status != STATUS_WAIT_OPEN and self.busy != 1:
            self.status = STATUS_BEAR_FORCE_BUY
            self.buy_qty = qty
            self.check_sufficiency_bear(qty)
            if wait_profit_ratio > 1 or wait_profit_ratio <= 0:
                self.wait_profit_qty_ratio = 1
            else:
                self.wait_profit_qty_ratio = wait_profit_ratio

    def bear_wait_profit(self):
        if self.status != STATUS_WAIT_OPEN:
            self.status = STATUS_BEAR_WAIT_PROFIT

    def set_idle(self):
        self.status = STATUS_IDLE

    def check_sufficiency_bear(self, qty):
        bear_ask_seller = self.stock_quote.get_bear_ask_seller()
        avail_cash = self.hk_trade_opt.get_avail_cash()
        if bear_ask_seller == -1 or avail_cash == -1:
            return -1
        if qty * bear_ask_seller >= avail_cash:
            ability_pen = math.floor((avail_cash / (bear_ask_seller - 0.001))/10000)
            ability_qty = ability_pen * 10000
            self.buy_qty = ability_qty


    def bull_force_sell(self):
        if self.status != STATUS_WAIT_OPEN:
            self.status = STATUS_BULL_FORCE_SELL

    def bull_force_buy(self, qty, wait_profit_ratio = 0.5):
        if self.status != STATUS_WAIT_OPEN and self.busy != 1:
            self.status = STATUS_BULL_FORCE_BUY
            self.buy_qty = qty
            self.check_sufficiency_bear(qty)
            if wait_profit_ratio > 1 or wait_profit_ratio <= 0:
                self.wait_profit_qty_ratio = 1
            else:
                self.wait_profit_qty_ratio = wait_profit_ratio

    def bull_wait_profit(self):
        if self.status != STATUS_WAIT_OPEN:
            self.status = STATUS_BULL_WAIT_PROFIT

    def check_sufficiency_bull(self, qty):
        bull_ask_seller = self.stock_quote.get_bull_ask_seller()
        avail_cash = self.hk_trade_opt.get_avail_cash()
        if bull_ask_seller == -1 or avail_cash == -1:
            return -1
        if qty * bull_ask_seller >= avail_cash:
            ability_pen = math.floor((avail_cash / (bull_ask_seller - 0.001))/10000)
            ability_qty = ability_pen * 10000
            self.buy_qty = ability_qty


    def run(self):
        while(1):
            ## Get Status
            try:
                status = self.status
            except:
                time.sleep(0.1)
                continue

            if status == STATUS_WAIT_OPEN:
                wait_open_status = 1
                while wait_open_status != 0:
                    bear_bid_seller = self.stock_quote.get_bear_bid_seller()
                    bear_ask_seller = self.stock_quote.get_bear_ask_seller()
                    if bear_bid_seller != -1 and bear_ask_seller != -1 and bear_bid_seller * 1000 - bear_ask_seller * 1000 <= 2:
                        print("SELLER STARTS!")
                        break
                    else:
                        time.sleep(0.5)
                        continue
                print("WAIT OPEN FINISHED")
                self.set_idle()
                continue


            if status == STATUS_IDLE:
                time.sleep(0.1)
                continue



            if status == STATUS_BEAR_FORCE_SELL:
                ## Check Position
                qty_p = self.hk_trade_opt.query_position_stock_qty(self.bear_code)
                if qty_p == -1 or qty_p == 0:
                    #print("No Position. Force Sell Bear Stop!")
                    self.set_idle()
                    continue
                else:
                    ## SELL
                    bear_force_sell_status = 1
                    qty = qty_p
                    wait_bad_quote = 30
                    while bear_force_sell_status != 0:
                        bear_bid = self.stock_quote.get_bear_bid()
                        bear_ask = self.stock_quote.get_bear_ask()
                        #print(bear_bid, bear_ask)
                        if bear_ask * 1000 - bear_bid * 1000 <= 2:
                            localid = self.hk_trade_opt.sell_stock_code_qty(self.bear_code, bear_bid, qty)
                            if localid == -1:
                                break
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
                                    break
                                # new qty
                                qty -= int(dealt_qty)
                                bear_force_sell_status = 2
                            elif ret == 0:
                                bear_force_sell_status = 0
                            else:
                                break
                        else:
                            if wait_bad_quote == 0:
                                break
                            else:
                                time.sleep(0.2)
                                wait_bad_quote -= 1

                        # Check if status if changed by others
                        try:
                            check_status = self.status
                        except:
                            continue
                        if check_status != STATUS_BEAR_FORCE_SELL:
                            break
                #print("FORCE SELL FINISHED")
                self.set_idle()
                self.busy = 0
                continue



            if status == STATUS_BEAR_FORCE_BUY:
                dealt_ask = 0
                if self.buy_qty <= 0:
                    print("Bad Qty. Force Buy Bear Stop!")
                    self.set_idle()
                    continue
                else:
                    bear_force_buy_status = 1
                    qty = self.buy_qty
                    wait_bad_quote = 30
                    dealt_ask = 0
                    while bear_force_buy_status != 0:
                        print("Force Buy")
                        bear_bid = self.stock_quote.get_bear_bid()
                        bear_ask = self.stock_quote.get_bear_ask()
                        print(bear_bid, bear_ask)
                        if bear_ask * 1000 - bear_bid * 1000 <= 2:
                            localid = self.hk_trade_opt.buy_stock_code_qty(self.bear_code, bear_ask, qty)
                            dealt_ask = bear_ask
                            if localid == -1:
                                break
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
                                    break
                                # new qty
                                qty -= int(dealt_qty)
                                bear_force_buy_status = 2
                            elif ret == 0:
                                bear_force_buy_status = 0
                            else:
                                break
                        else:
                            if wait_bad_quote == 0:
                                print("Bad Bear Quoto")
                            else:
                                time.sleep(0.2)
                                wait_bad_quote -= 1
                        # Check if status if changed by others
                        try:
                            check_status = self.status
                        except:
                            continue
                        if check_status != STATUS_BEAR_FORCE_BUY:
                            break
                if dealt_ask == 0:
                    print("FORCE BUY FINISHED")
                    self.set_idle()
                else:
                    print("FORCE BUY SUCCESS")
                    self.dealt_ask = dealt_ask
                    self.bear_wait_profit()
                continue



            if status == STATUS_BEAR_WAIT_PROFIT:
                ## Check Position
                sell_qty = 0
                qty_p = self.hk_trade_opt.query_position_stock_qty(self.bear_code)
                if qty_p == -1 or qty_p == 0 or self.dealt_ask == 0:
                    if self.dealt_ask == 0:
                        print("Bad Dealt Ask")
                    print("No Position. WAIT BEAR PROFIT Stop!")
                    self.set_idle()
                else:
                    sell_pencil = math.ceil((int(qty_p) / 10000) * self.wait_profit_qty_ratio)
                    sell_qty = sell_pencil * 10000
                    qty = sell_qty
                    wait_bear_profit_status = 1
                    while wait_bear_profit_status != 0:
                        bear_bid = self.stock_quote.get_bear_bid()
                        if bear_bid * 1000 - self.dealt_ask * 1000 >= 1:
                            localid = self.hk_trade_opt.sell_stock_code_qty(self.bear_code, bear_bid, qty)
                            if localid == -1:
                                break
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
                                    break
                                # new qty
                                qty -= int(dealt_qty)
                                wait_bear_profit_status = 2
                            elif ret == 0:
                                wait_bear_profit_status = 0
                            else:
                                break
                        else:
                            time.sleep(0.2)

                        # Check if status if changed by others
                        try:
                            check_status = self.status
                        except:
                            continue
                        if check_status != STATUS_BEAR_WAIT_PROFIT:
                            break
                print("BEAR WAIT PROFIT FINISHED")
                self.set_idle()
                if sell_qty == qty_p:
                    self.busy = 0
                continue

            if status == STATUS_BULL_FORCE_BUY:
                dealt_ask = 0
                if self.buy_qty <= 0:
                    print("Bad Qty. Force Buy Bull Stop!")
                    self.set_idle()
                    continue
                else:
                    bull_force_buy_status = 1
                    qty = self.buy_qty
                    wait_bad_quote = 30
                    dealt_ask = 0
                    while bull_force_buy_status != 0:
                        print("Force Buy")
                        bull_bid = self.stock_quote.get_bull_bid()
                        bull_ask = self.stock_quote.get_bull_ask()
                        print(bull_bid, bull_ask)
                        if bull_ask * 1000 - bull_bid * 1000 <= 2:
                            localid = self.hk_trade_opt.buy_stock_code_qty(self.bull_code, bull_ask, qty)
                            dealt_ask = bull_ask
                            if localid == -1:
                                break
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
                                    break
                                # new qty
                                qty -= int(dealt_qty)
                                bull_force_buy_status = 2
                            elif ret == 0:
                                bull_force_buy_status = 0
                            else:
                                break
                        else:
                            if wait_bad_quote == 0:
                                print("Bad Bull Quoto")
                            else:
                                time.sleep(0.2)
                                wait_bad_quote -= 1
                        # Check if status if changed by others
                        try:
                            check_status = self.status
                        except:
                            continue
                        if check_status != STATUS_BULL_FORCE_BUY:
                            break
                if dealt_ask == 0:
                    print("FORCE BUY FINISHED")
                    self.set_idle()
                else:
                    print("FORCE BUY SUCCESS")
                    self.dealt_ask = dealt_ask
                    self.bull_wait_profit()
                continue

            if status == STATUS_BULL_FORCE_SELL:
                ## Check Position
                qty_p = self.hk_trade_opt.query_position_stock_qty(self.bull_code)
                if qty_p == -1 or qty_p == 0:
                    # print("No Position. Force Sell Bear Stop!")
                    self.set_idle()
                    continue
                else:
                    ## SELL
                    bull_force_sell_status = 1
                    qty = qty_p
                    wait_bad_quote = 30
                    while bull_force_sell_status != 0:
                        bull_bid = self.stock_quote.get_bull_bid()
                        bull_ask = self.stock_quote.get_bull_ask()
                        # print(bear_bid, bear_ask)
                        if bull_ask * 1000 - bull_bid * 1000 <= 2:
                            localid = self.hk_trade_opt.sell_stock_code_qty(self.bull_code, bull_bid, qty)
                            if localid == -1:
                                break
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
                                    break
                                # new qty
                                qty -= int(dealt_qty)
                                bull_force_sell_status = 2
                            elif ret == 0:
                                bull_force_sell_status = 0
                            else:
                                break
                        else:
                            if wait_bad_quote == 0:
                                break
                            else:
                                time.sleep(0.2)
                                wait_bad_quote -= 1

                        # Check if status if changed by others
                        try:
                            check_status = self.status
                        except:
                            continue
                        if check_status != STATUS_BULL_FORCE_SELL:
                            break
                # print("FORCE SELL FINISHED")
                self.set_idle()
                self.busy = 0
                continue

            if status == STATUS_BULL_WAIT_PROFIT:
                ## Check Position
                sell_qty = 0
                qty_p = self.hk_trade_opt.query_position_stock_qty(self.bull_code)
                if qty_p == -1 or qty_p == 0 or self.dealt_ask == 0:
                    if self.dealt_ask == 0:
                        print("Bad Dealt Ask")
                    print("No Position. WAIT BULL PROFIT Stop!")
                    self.set_idle()
                else:
                    sell_pencil = math.ceil((int(qty_p) / 10000) * self.wait_profit_qty_ratio)
                    sell_qty = sell_pencil * 10000
                    qty = sell_qty
                    wait_bull_profit_status = 1
                    while wait_bull_profit_status != 0:
                        bull_bid = self.stock_quote.get_bull_bid()
                        if bull_bid * 1000 - self.dealt_ask * 1000 >= 1:
                            localid = self.hk_trade_opt.sell_stock_code_qty(self.bear_code, bull_bid, qty)
                            if localid == -1:
                                break
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
                                    break
                                # new qty
                                qty -= int(dealt_qty)
                                wait_bull_profit_status = 2
                            elif ret == 0:
                                wait_bull_profit_status = 0
                            else:
                                break
                        else:
                            time.sleep(0.2)

                        # Check if status if changed by others
                        try:
                            check_status = self.status
                        except:
                            continue
                        if check_status != STATUS_BULL_WAIT_PROFIT:
                            break
                print("BULL WAIT PROFIT FINISHED")
                self.set_idle()
                if sell_qty == qty_p:
                    self.busy = 0
                continue

            time.sleep(0.2)
