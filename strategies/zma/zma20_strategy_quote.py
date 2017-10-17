from data_src.stock_info.get_stock_quote import *
import threading
import time
import pandas as pd
from ui.PlaySound import *
from trade_api.hk_trade_op import *
from trade_api.hk_trade_handler import *

NO_POS = 0
CUR_POS = 1
TIME_POS = 2
ZMA10_POS = 3
ZMA20_POS = 4
ZMA10_RATIO_POS = 5
ZMA20_RATIO_POS = 6
ZMA20_RATIO_RATIO_POS = 7
ZMA_GAP_POS = 8
ZMA_GAP_RATIO_POS = 9
ZMA_GAP_RATIO_RATIO_POS = 10
ZMA10_RATIO_RATIO_POS = 11
ZMA10_RATIO_RATIO_RATIO_POS = 12
# CUR_RATIO_RATIO_POS = 12
ZMA5_POS = 13
ZMAQ_POS = 14
BULL_DECREASE_POS = 15
BEAR_DECREASE_POS = 16
BUY = 0
SELL = 1

class zma20_strategy_quote(threading.Thread):
    def __init__(self, qc, play, interval = 0.5 ):
        super(zma20_strategy_quote, self).__init__()
        self.__quote_ctx = qc
        self.deposit_bear = 0
        self.deposit_bottom = 0
        self.deposit_bull = 0
        self.deposit_top = 0
        self.zma10_new_trend = 0
        self.zma10_decrease = 1
        self.zma10_decrease_start = 0
        self.cur_zma10_ratio_simple_ratio = 0
        self.cur_zma10_ratio_simple_ratio_0 = 0
        self.cur_zma10_ratio_simple_ratio_ratio = 0
        self.cur_zma10_ratio_simple_ratio_ratio_0 = 0
        self.ret= []
        self.interval = 0.5
        self.count = 0
        self.is_available = 0
        self.play = play
        self.direction = 0
        self.sell_bear = 0
        self.band_bear = 0
        self.MA20_vol = 0
        self.vol_last = 0
        self.vol_now = 0
        self.vol_break = 0
        self.running = 0

## Trade
        self.buy_bull = 0
        self.buy_bear = 0

        data= []
        for i in range(0, 60000):
            data.append({"No.": 0})
        self.ret = pd.DataFrame(data, columns=["No.", "cur", "time", "zma10", "zma20",
                                               "zma10_ratio", "zma20_ratio","zma20_ratio_ratio", "zma_gap", "zma_gap_ratio",
                                               "zma_gap_ratio_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "zma5", "zmaq",
                                               "bull_decrease", "bear_decrease"])
        # 120K
        self.trade_qty = 15 * 10000
        self.bear_code = 61000
        self.bull_code = 64563
        self.hk_trade = hk_trade_api()
        self.hk_trade.initialize()
        self.hk_trade.unlock_trade('88888888', '584679')
        self.opt_real = hk_trade_opt(self.hk_trade, 0)
        self.opt_simulation = hk_trade_opt(self.hk_trade)
        ### Change Trade Type Here
        self.opt = self.opt_simulation
        self.stock_quote = get_stock_quote(self.__quote_ctx, "HK." + str(self.bull_code), "HK." + str(self.bear_code))
        self.hk_trade_handler = hk_trade_handler(self.opt, self.stock_quote, self.bull_code, self.bear_code)
        # self.hk_trade_handler_bear = hk_trade_handler(self.opt, self.stock_quote, self.bear_code)
        # self.hk_trade_handler_bear_simulation = hk_trade_handler(self.opt_simulation, self.stock_quote, self.bear_code)
        self.test = 1
        # self.opt.disble_order_stock_code(67863)
        #    localid = opt.buy(0.06, 10000, "67541")
        #    orderid = opt.get_order_id(localid)
        #    status = opt.check_order_status(orderid)
        #    dealt = opt.get_dealt_qty(orderid)
        #    print(dealt)
        #    opt.disable_order(orderid)




    ## MA
    def cal_zmaq(self, position):
        len = 30
        sum = 0
        if position < len :
            return -1
        if position == len :
            for j in range(0, len):
                sum += self.ret["cur"][len + 1 - 1 - j]
            avr0 = sum / len
            self.ret.iloc[position, ZMAQ_POS] = avr0
            return 1
        starter = self.ret["cur"][position - len ]
        avr = self.ret["zmaq"][position -1] - starter/len + self.ret["cur"][position]/len
        self.ret.iloc[position, ZMAQ_POS] = avr

        return 0

    def cal_zma5(self, position):
        len = 600
        sum = 0
        if position < len :
            return -1
        if position == len :
            for j in range(0, len):
                sum += self.ret["cur"][len + 1 - 1 - j]
            avr0 = sum / len
            self.ret.iloc[position, ZMA5_POS] = avr0
            return 1
        starter = self.ret["cur"][position - len ]
        avr = self.ret["zma5"][position -1] - starter/len + self.ret["cur"][position]/len
        self.ret.iloc[position, ZMA5_POS] = avr
        return 0

    def cal_zma10(self, position):
        len = 1200
        sum = 0
        if position < len:
            return -1
        if position == len:
            for j in range(0, len):
                sum += self.ret["cur"][len + 1 - 1 - j]
            avr0 = sum / len
            self.ret.iloc[position, ZMA10_POS] = avr0
            return 1
        starter = self.ret["cur"][position - len]
        avr = self.ret["zma10"][position - 1] - starter / len + self.ret["cur"][position] / len
        self.ret.iloc[position, ZMA10_POS] = avr
        #        print("zma10 " + str(avr) + " starter: " + str(self.ret["cur"][position - len ]) + " Cur: " + str(self.ret["cur"][position]) + " Before: " + str(self.ret["zma10"][position -1 ]))
        return 0

    def cal_zma20(self, position):
        len = 2400
        sum = 0
        if position < len :
            return -1
        if position == len :
            for j in range(0, len):
                sum += self.ret["cur"][len + 1 - 1 - j]
            avr0 = sum / len
            self.ret.iloc[position, ZMA20_POS] = avr0
            return 1
        starter = self.ret["cur"][position - len ]
        avr = self.ret["zma20"][position - 1 ] - starter/len + self.ret["cur"][position]/len
        self.ret.iloc[position, ZMA20_POS] = avr
#        print("zma20 " + str(avr))
        return 0


    ## MA Ratio
    def cal_zma10_ratio(self, position, sample = 60):
        len = 1200
        t = sample
        val =0
        start_pos = len + t
        if position < start_pos:
          return -1

        ret, val = self.optimized_least_square_method(position - t + 1, position, "zma10")
        if ret == -1:
            val = 0
        self.ret.iloc[position, ZMA10_RATIO_POS] = val  * 120
        return 1

    def cal_zma10_ratio_simple(self, position, sample = 120):
        len = 1200
        t = sample
        val =0
        c = 120 / sample
        start_pos = len + t
        if position < start_pos:
          return -1

        val = self.ret.iloc[position, ZMA10_POS] - self.ret.iloc[position - t, ZMA10_POS]
        self.ret.iloc[position, ZMA10_RATIO_POS] = val * c

        return 1

## Require ZMA10_RATIO
    def refresh_zma10_ratio_simple(self, position, sample = 120):
        len = 1200
        start_pos = len + sample
        ## Assign zma10_new_trend at the first time
        if self.zma10_new_trend == 0:
            try:
                deltaMA10_ma3 = self.deltaMA10_ma3
                if deltaMA10_ma3 >= 0:
                    self.zma10_new_trend = 1
                else:
                    self.zma10_new_trend = -1
            except:
                x = 1

        if position > start_pos + 1:
            older_ma10_ratio = self.ret.iloc[position - 1, ZMA10_RATIO_POS]
            now_ma10_ratio = self.ret.iloc[position, ZMA10_RATIO_POS]
            if older_ma10_ratio >= 0 and now_ma10_ratio < 0:
                self.zma10_new_trend = -1
            if older_ma10_ratio <= 0 and now_ma10_ratio > 0:
                self.zma10_new_trend = 1

        return


    def cal_zma20_ratio(self, position, sample = 60):
        len = 2400
        t = sample
        val =0
        start_pos = len + t
        if position < start_pos:
          return -1
        ret, val = self.optimized_least_square_method(position - t + 1, position, "zma20")
        if ret == -1:
            val = 0
        self.ret.iloc[position, ZMA20_RATIO_POS] = val * 120
        return 1

    def cal_zma20_ratio_ratio(self, position):
        len = 2400
        t = 240
        val =0
        start_pos = len + t + 60
        if position < start_pos:
          return -1

        ret, val = self.optimized_least_square_method(position - t + 1, position, "zma20_ratio")
        if ret == -1:
            val = 0
        self.ret.iloc[position, ZMA20_RATIO_RATIO_POS] = val * 10000
        return 1

    def cal_zma10_ratio_ratio(self, position):
        len = 2400
        t = 240
        val =0
        start_pos = len + t + 60
        if position < start_pos:
          return -1

        ret, val = self.optimized_least_square_method(position - t + 1, position, "zma10_ratio")
        if ret == -1:
            val = 0
        self.ret.iloc[position, ZMA10_RATIO_RATIO_POS] = val * 10000
        return 1

    def cal_zma10_ratio_simple_ratio(self, position, sample = 360):
        len = 1200 + 121
        val =0
        start_pos = len + sample
        if position < start_pos:
          return -1
        self.cur_zma10_ratio_simple_ratio_0 = self.cur_zma10_ratio_simple_ratio
        val = self.ret.iloc[position, ZMA10_RATIO_POS] - self.ret.iloc[position - sample, ZMA10_RATIO_POS]
        self.ret.iloc[position, ZMA10_RATIO_RATIO_POS] = val / sample
        self.cur_zma10_ratio_simple_ratio = val / sample
        return 1


    def cal_zma10_ratio_ratio_ratio_simple(self, position, sample = 120):
        len = 1200 + 121 + 360
        val =0
        start_pos = len + sample
        c = 120 / sample
        if position < start_pos:
          return -1

        self.cur_zma10_ratio_simple_ratio_ratio_0 = self.cur_zma10_ratio_simple_ratio_ratio
        val = self.ret.iloc[position, ZMA10_RATIO_RATIO_POS] - self.ret.iloc[position - sample, ZMA10_RATIO_RATIO_POS]
        self.ret.iloc[position, ZMA10_RATIO_RATIO_RATIO_POS] = val * c
        self.cur_zma10_ratio_simple_ratio_ratio = val * c

        return 1

    ## MA GAP
    def cal_zma_gap(self, position):
        len = 2400
        start_pos = len + 1
        if position < start_pos:
            return -1

        val = self.ret["zma10"][position] - self.ret["zma20"][position]
        self.ret.iloc[position, ZMA_GAP_POS] = val
        return 1

    def cal_zma_gap_ratio(self, position):
        len = 2400
        t = 240
        val =0
        start_pos = len + t + 1
        if position < start_pos:
          return -1

        ret, val = self.optimized_least_square_method(position - t + 1, position, "zma_gap")
        if ret == -1:
            val = 0
        self.ret.iloc[position, ZMA_GAP_RATIO_POS] = float(val) * 10000
        return 1

    def cal_zma_gap_ratio_ratio(self, position):
        len = 1200
        t = 180
        val =0
        start_pos = len + t + 240 + 1
        if position < start_pos:
          return -1

        ret, val = self.optimized_least_square_method(position - t + 1, position, "zma_gap_ratio")
        if ret == -1:
            val = 0
        self.ret.iloc[position, ZMA_GAP_RATIO_RATIO_POS] = val * 10000
        return 1

    def optimized_least_square_method(self, start, end, column):
        A = 0
        B = 0
        xi = 0
        t = end - start + 1
        avr_x = 0
        avr_y = 0
        if self.count < start:
            return -1, 0
        B = (t - 1) * t
        B /= 2
        for i in range(start, end + 1):
            cur = self.ret[column][i]
            A += xi * cur
            avr_x += xi / t
            avr_y += cur/t
            xi += 1
        M = t * avr_x
        ratio = (A - M * avr_y) / (B - M * avr_x) *(-1)
        return 1, ratio

    def first_10min_warning(self):
        try:
            cur_time = self.data_time
        except:
            return
        morning_danger = "9:40:00"
        morning_danger_list = morning_danger.split(":")
        morning_danger_second = int(morning_danger_list[0]) * 3600 + int(morning_danger_list[1]) * 60 + int(morning_danger_list[2])

        cur_time_list = cur_time.split(":")
        cur_time_second = int(cur_time_list[0]) * 3600 + int(cur_time_list[1]) * 60 + int(cur_time_list[2])

        if cur_time_second < morning_danger_second:
            self.play.play_morning_warn()
        else:
            self.play.stop_play_morning_warn()
        return

    def determine_direction(self):
        UP_THRESHOLD = 0.5
        DOWN_THRESHOLD = -0.5
        try:
            deltaMA20 = self.deltaMA20_ma3
        except:
            return

        if deltaMA20 > UP_THRESHOLD:
            self.direction = 1
        else:
            if deltaMA20 < DOWN_THRESHOLD:
                self.direction = -1
            else:
                self.direction = 0
        return

    def guard_direction(self):
        try:
            direction = self.direction
        except:
            return
        if direction == 0:
            self.play.play_no_trend()
        else:
            self.play.stop_play_no_trend()
        return

    def guard_burst(self):
        UP_BURST_THRESHOLD = 1
        DOWN_BURST_THRESHOLD = -1
        try:
            gap_20s = self.cur_gap_20s
        except:
            return
        if gap_20s > UP_BURST_THRESHOLD:
            self.play.play_burst_up()
        else:
            self.play.stop_burst_up()

        if gap_20s < DOWN_BURST_THRESHOLD:
            self.play.play_burst_down()
        else:
            self.play.stop_burst_down()

    def warn_bull_recover(self):
        REVOVER_THRESHOLD = 0.5
        #print(self.ma_1m_table)
        try:
            deltaMA20 = self.deltaMA20_ma3
            cur_ma20 = self.MA20_cur
        except:
            return
        ## Condition 1: MA20 Changes fast
        if deltaMA20 <= REVOVER_THRESHOLD:
            self.play.stop_play_warn_bull_recover()
            return
        else:
            count = 26
            sub = self.ma_1m_table.iloc[count - 2, 3] - self.ma_1m_table.iloc[count - 2, 2]
            ## Condition 2: Latest bar is red
            if sub >= 0:
                self.play.stop_play_warn_bull_recover()
                return
            else:
                high = self.ma_1m_table.iloc[count - 2, 4]
                low = self.ma_1m_table.iloc[count - 2, 5]
                ## Condition 3: MA20 Value is surrounded by Latest bar
                if cur_ma20 < high and cur_ma20 > low:
                    self.play.play_warn_bull_recover()
                else:
                    self.play.stop_play_warn_bull_recover()
        return

    def warn_ma_low(self):
        LOWMA10_THRESHOLD = 0.7
        LOWMA20_THRESHOLD = 0.5
        try:
            deltaMA20 = self.deltaMA20_ma3
            deltaMA10 = self.deltaMA10_ma3
        except:
            return

        ## Condition 1: MA20 Changes fast
        if abs(deltaMA20) <= LOWMA20_THRESHOLD and abs(deltaMA10) <= LOWMA10_THRESHOLD:
            self.play.play_warn_ma_low()
            self.opt.disble_order_stock_code(self.bear_code)
            self.opt.disble_order_stock_code(self.bull_code)
        else:
             self.play.stop_play_warn_ma_low()
        return

    def guard_bear(self):
        count = 26
        GROWTH_THRESHOLD = 10
        PRIV_THRESHOLD = -2
        try:
            deltaMA20 = self.deltaMA20_ma3
        except:
            return
        if self.deposit_bear == 0:
            sub = self.ma_1m_table.iloc[count - 2, 3] - self.ma_1m_table.iloc[count - 2, 2]
            if sub <= 0:
                self.deposit_bear = 0
                self.deposit_bottom = 0
                self.play.stop_play_stop_lossing_bear()
                print("Guard Bear: reset red")
                return
            else:
                self.deposit_bear = sub
                if self.deposit_bear >= GROWTH_THRESHOLD:
                    if deltaMA20 < PRIV_THRESHOLD:
                        self.play.play_stop_lossing_bear_inst()
                    else:
                        self.play.play_stop_lossing_bear()
                    self.deposit_bear = 0
                    self.deposit_bottom = 0
                    print("Guard Bear: warn directly")
                else:
                    self.deposit_bottom = self.ma_1m_table.iloc[count - 2, 2]
                    print("Guard Bear: wait, find deposit")
                    return
        else:
        # we have a Green K bar that is less than VALUE
            new_deposit = self.cur - self.deposit_bottom
            if new_deposit >= GROWTH_THRESHOLD:
                if deltaMA20 > PRIV_THRESHOLD:
                    self.play.play_stop_lossing_bear_inst()
                else:
                    self.play.play_stop_lossing_bear()
                self.deposit_bear = 0
                self.deposit_bottom = 0
                print("Guard Bear: warn with deposit")
            else:
                sub = self.ma_1m_table.iloc[count - 2, 3] - self.ma_1m_table.iloc[count - 2, 2]
                if sub < 0:
                    if self.ma_1m_table.iloc[count - 2, 3] <= self.deposit_bottom:
                        self.deposit_bear = 0
                        self.deposit_bottom = 0
                        self.play.stop_play_stop_lossing_bear()
                        print("Guard Bear: reset with deposit")
                print("Guard Bear: wait with deposit " + str(self.deposit_bottom))
                return

    def guard_bear2(self):
        K_NO = 56
        count = K_NO

        open_pos = 2
        high_pos = 3
        close_pos = 4
        low_pos = 5
        check_value = 10000

        observe_num = 5
        current_weight = 0.6
        score = 0
        tolerance = 0
        limit = 10
        extra_tolerance = 2
        sell_bear = 0
        band_bear = 0
        ## Check K-1M quality
        for i in range(observe_num, 0, -1):
            if self.ma_1m_table["open"][count - i] < check_value:
                return
            if self.ma_1m_table["high"][count - i] < check_value:
                return
            if self.ma_1m_table["close"][count - i] < check_value:
                return
            if self.ma_1m_table["low"][count - i] < check_value:
                return

        ### Get Latest 5 Bars
        data = []
        for i in range(observe_num, 0, -1):
                data.append({"code": self.ma_1m_table["code"][count - i], "time_key": self.ma_1m_table["time_key"][count - i], \
                             "open": self.ma_1m_table["open"][count - i], "high": self.ma_1m_table["high"][count - i], "close": self.ma_1m_table["close"][count - i], "low": self.ma_1m_table["low"][count - i], \
                             "volume": self.ma_1m_table["volume"][count - i], "turnover": self.ma_1m_table["turnover"][count - i]})
        ma_1m_table = pd.DataFrame(data, columns=["code", "time_key", "open", "high", "close", "low", "volume", "turnover"])


        ## Fix Open value, = older close
        for i in range(1, observe_num):
            ma_1m_table.iloc[i,open_pos] = ma_1m_table.iloc[i - 1, close_pos]
            # if new open > high, new high =  new open
            if ma_1m_table.iloc[i, open_pos] > ma_1m_table.iloc[i, high_pos]:
                ma_1m_table.iloc[i, high_pos] = ma_1m_table.iloc[i, open_pos]
            # if new open < low, new low = new open
            if ma_1m_table.iloc[i, open_pos] < ma_1m_table.iloc[i, low_pos]:
                ma_1m_table.iloc[i, low_pos] = ma_1m_table.iloc[i, open_pos]

        ## Find the lowest low
        lowest_pos = 0
        for i in range(1, observe_num):
            if (ma_1m_table.iloc[i, low_pos] < ma_1m_table.iloc[lowest_pos, low_pos]) or (ma_1m_table.iloc[i, low_pos] == ma_1m_table.iloc[lowest_pos, low_pos]):
                lowest_pos = i

        ## Find the highest
        highest_pos = 0
        for i in range(1, observe_num):
            if (ma_1m_table.iloc[i, high_pos] > ma_1m_table.iloc[highest_pos, high_pos]) or ( ma_1m_table.iloc[i, high_pos] == ma_1m_table.iloc[highest_pos, high_pos]):
                highest_pos = i

        # Calculate limit bonus
        high_low_gap = ma_1m_table.iloc[highest_pos, high_pos] - ma_1m_table.iloc[lowest_pos, low_pos]
        if high_low_gap > 0:
            limit_bonus = (high_low_gap % 10) * 0.5
            extra_tolerance_bonus = (high_low_gap % 10) * 0.5
            limit += limit_bonus
            extra_tolerance += extra_tolerance_bonus

        ## If lowest is the latest one
        pointer = lowest_pos
        while(pointer < observe_num):
            if pointer == observe_num - 1:
                if lowest_pos == observe_num - 1:
                    score += (ma_1m_table.iloc[pointer, close_pos] - ma_1m_table.iloc[pointer, low_pos]) * current_weight
                else:
                    if ma_1m_table.iloc[pointer, close_pos] > ma_1m_table.iloc[pointer, open_pos]:
                        score += (ma_1m_table.iloc[pointer, close_pos] - ma_1m_table.iloc[pointer, open_pos]) * current_weight
                if tolerance > 0:
                    if (ma_1m_table.iloc[pointer, high_pos] - ma_1m_table.iloc[pointer, open_pos]) > tolerance:
                        #print("WARN!!!! SELL BEAR!!! Over Tolerance")
                        sell_bear = 1
                else:
                    if score > limit:
                        #print("WARN!!!! SELL BEAR!!!")
                        sell_bear = 1
                pointer += 1
            else:
                long_gap = ma_1m_table.iloc[observe_num - 2, close_pos] - ma_1m_table.iloc[lowest_pos, low_pos]
                if long_gap < 0:
                    print("ERROR!!! LONG GAP ERROR!!!")
                score += long_gap
                if score > limit:
                    band_bear = 1
                    tolerance = extra_tolerance
                    #print("Assign Tollerance")
                pointer = observe_num - 1
        #print("SCORE: " + str(score))
        self.sell_bear = sell_bear
        self.band_bear = band_bear
        if sell_bear == 1:
            self.play.play_stop_lossing_bear_inst()
            #self.opt.clear_stock_code(self.bear_code, self.bear_bid_seller)
            #if self.hk_trade_handler_bear.is_alive() == False:
                #self.hk_trade_handler_bear = hk_trade_handler(self.opt, self.stock_quote, self.bear_code)
                #self.hk_trade_handler_bear.start()

            #if self.hk_trade_handler_bear_simulation.is_alive() == False:
                #self.hk_trade_handler_bear_simulation = hk_trade_handler(self.opt_simulation, self.stock_quote, self.bear_code)
                #self.hk_trade_handler_bear_simulation.start()
            if self.buy_bear == 1:
                self.buy_bear = 0
                self.hk_trade_handler.bear_force_sell()
        else:
            self.play.stop_play_stop_lossing_bear()


        return

## Require ZMA10_RATIO_SIMPLE_RATIO
    def detect_zma10_decrease(self):
        try:
            cur_zma10_ratio_simple_ratio   = self.cur_zma10_ratio_simple_ratio
            cur_zma10_ratio_simple_ratio_0 = self.cur_zma10_ratio_simple_ratio_0
        except:
            return
        if cur_zma10_ratio_simple_ratio_0 > -0.01 and cur_zma10_ratio_simple_ratio <= -0.01:

            print("REMIND!!!DETECT MA10 DECREASE!!")
            self.zma10_decrease = 1
            self.play.play_zma10_decrease()
        else:
            self.zma10_decrease = 0
            self.play.stop_play_zma10_decrease()
        #print(cur_zma10_ratio_simple_ratio, "AAAAAAAA", cur_zma10_ratio_simple_ratio_0)
        return

    def detect_zma10_decrease_start(self):
        try:
            cur_zma10_ratio_simple_ratio_ratio   = self.cur_zma10_ratio_simple_ratio_ratio
            cur_zma10_ratio_simple_ratio_ratio_0 = self.cur_zma10_ratio_simple_ratio_ratio_0
        except:
            return
        if cur_zma10_ratio_simple_ratio_ratio_0 > -0.004 and cur_zma10_ratio_simple_ratio_ratio <= -0.004:
            print(str(self.data_time), "REMIND!!!DETECT MA10 DECREASE START!!")
            self.zma10_decrease_start = 1
            #self.play.play_zma10_decrease()
        else:
            self.zma10_decrease_start = 0
            #self.play.stop_play_zma10_decrease()
        #print(cur_zma10_ratio_simple_ratio_ratio, "SSSSSSSS", cur_zma10_ratio_simple_ratio_ratio_0)
        return

## Require zma10_decrease
    def detect_empty_decrease(self):

        ## First, See if meet 001 condition
        if self.zma10_decrease == 0:
            return
        if self.zma10_decrease == 1:
            ## Second, See if we can do it for the first time
            if self.zma10_new_trend != -1:
                return
            else:
                ## Now We check Empty Start
                ## Condition 1: MA10 goes down
                ## Condition 2: MA10 is less than MA20
                ## Condition 3: Current value is less than MA10
                if self.count < 1500:
                    ma10_ratio = self.deltaMA10_cur
                else:
                    ma10_ratio = self.ret.iloc[self.count, ZMA10_RATIO_POS]
                if ma10_ratio < 0 and \
                    self.MA10_cur < self.MA20_cur and \
                    self.cur < self.MA10_cur and \
                    self.sell_bear == 0:
                    zma10_rrr = self.ret.iloc[self.count, ZMA10_RATIO_RATIO_POS] - self.ret.iloc[self.count - 120, ZMA10_RATIO_RATIO_POS]
                    if zma10_rrr <= -0.005:
                        print("BUY BUY BUY!!!")
                        #if self.hk_trade_handler_bear_simulation.is_alive() == False:
                            #self.hk_trade_handler_bear_simulation = hk_trade_handler(self.opt_simulation, self.stock_quote, self.bear_code, BUY, self.trade_qty)
                            #self.hk_trade_handler_bear_simulation.start()
                            #self.test = 1
                        self.hk_trade_handler.bear_force_buy(self.trade_qty)
                        self.zma10_new_trend = -9999
                    else:
                        print("zma10_rrr", zma10_rrr)

        return

        ## Require zma10_decrease
    def detect_empty_start(self):
        bear_start = 0
         ## First, See if meet 0004 condition
        if self.zma10_decrease_start == 0:
             return
        if self.zma10_decrease_start == 1:
            ## Second, See if we can do it for the first time
            if self.zma10_new_trend != -1:
                return
            else:
                    ## Now We check Empty Start
                    ## Condition 1: M10_r_r <=0 or M10_r_r - 0.004 * 60 <= 0
                    ## Condition 2: Cur < M10
                    ## Condition 3:
                    ##         If 	1. M20_r > -1:
                    ##                 a. M10_r <= 0 or M10_r - M10_r_r * 60 <= 0
                    ##                 b. M10_r < M20_r
                    ##         If   2. M20_r < -1:
                    ##                 M10_r < 0
                    ##

                if self.count < 1700:
                    return

                ma10_ratio_ratio = self.ret.iloc[self.count, ZMA10_RATIO_RATIO_POS]
                ma10_ratio = self.ret.iloc[self.count, ZMA10_RATIO_POS]
                ma20_ratio = self.deltaMA20_cur
                ma10_r_r_r_value = -0.004
                ma20_many_head = -2
                ma10_r_r_value = -0.005
                ma10_r_r_small_value = -0.001
                if self.vol_break != 1:
                    ## MA20_r is big
                    ## MA10 r is
                    if ma20_ratio >= ma20_many_head and \
                            (ma10_ratio <= 0 or ma10_ratio + ma10_ratio_ratio * 60 <= 0) and ma10_ratio >= -3 and \
                                    ma10_ratio < ma20_ratio :
                        if ma10_ratio_ratio <= ma10_r_r_value and \
                                self.cur < self.MA10_cur and (self.MA10_cur  + ma10_ratio * 2) < self.MA20_cur:
                            gap = self.cur - self.ret["cur"][self.count - 120]
                            if gap > -10 and gap < -5:
                                bear_start = 1118
                            if gap <= -10:
                                bear_start = 1114

                    if ma20_ratio >= ma20_many_head and ma20_ratio < 0.5 and \
                            ma10_ratio < -1 and ma10_ratio >= -3 and \
                            ma10_ratio < ma20_ratio:
                        if ma10_ratio_ratio <= ma10_r_r_small_value and ma10_ratio_ratio > ma10_r_r_value and \
                                self.cur < self.MA10_cur and (self.MA10_cur + ma10_ratio * 2) < self.MA20_cur:
                            gap = self.cur - self.ret["cur"][self.count - 120]
                            ratio = gap / ma10_ratio
                            if ratio <= 8 and gap < 0:
                                bear_start = 2222



        if bear_start != 0 and self.sell_bear == 0:
            print("BUY BUY BUY!!!")
            print(self.ret.iloc[self.count,])
            if self.is_trade_limit_time() == 1:
                if bear_start == 1114:
                    self.hk_trade_handler.bear_force_buy(self.trade_qty, 1)
                    self.zma10_new_trend = -9999
                if bear_start == 1118:
                    self.hk_trade_handler.bear_force_buy(self.trade_qty, 1)
                    self.zma10_new_trend = -9999
                if bear_start == 2222:
                    self.hk_trade_handler.bear_force_buy(self.trade_qty, 0.7)
                    self.zma10_new_trend = -9999



        ## Require zma10_decrease
    def  buy_bear_13th_oct_no_delay(self):
        K_NO = 56
        if self.oct_13th_strategy_trade_time() == 0:
            return

        ma5_list = self.MA5_list

        vol_now = self.vol_now
        vol_last = self.vol_last
        MA20_vol = self.MA20_vol
        cur =  self.cur
        MA5_now = ma5_list[0]
        MA10_now = self.MA10_now
        MA20_now = self.MA20_now
        MA50_cur = self.MA50_cur
        deltaMA10_now = self.deltaMA10_now
        deltaMA20_now = self.deltaMA20_now
        down_count = 0
        up_count = 0
        point = 0
        ma5_ok = 0
        ## VOL Break, and
        ## Red bar
        if vol_now >= MA20_vol and \
            self.ma_1m_table["open"][K_NO - 1] > self.ma_1m_table["close"][K_NO - 1] + 2:
            if ma5_list[0] - ma5_list[1] < -2:
                for i in range(0, 9):
                    if ma5_list[i] < ma5_list[i + 1]:
                        down_count += 1
                        point += 1
                    else:
                        break

                if point >= 9:
                    return

                for i in range(point, 9):
                    if ma5_list[i] >= ma5_list[i + 1]:
                        up_count += 1

                if down_count <= 3 and up_count >= 1:
                    ma5_ok = 1

                if ma5_ok == 1:
                    if cur < MA5_now and \
                        (MA5_now < MA10_now or MA5_now < MA20_now ) and \
                        MA10_now - 3 < MA20_now :
                        if self.buy_bear == 0:
                            self.buy_bear = 1
                            self.hk_trade_handler.bear_force_buy(self.trade_qty, 0.5)
                            print("buy bear", self.ret.iloc[self.count,])

                down_count = 0
                up_count = 0
                point = 0
                ma5_ok = 0
                if ma5_list[0] - ma5_list[1] < -4:
                    for i in range(0, 9):
                        if ma5_list[i] < ma5_list[i + 1]:
                            down_count += 1
                            point += 1
                        else:
                            break

                    if point >= 9:
                        return

                    for i in range(point, 9):
                        if ma5_list[i] >= ma5_list[i + 1]:
                            up_count += 1

                    if down_count <= 3 and up_count >= 1:
                        ma5_ok = 1

                    if ma5_ok == 1:
                        if cur < MA5_now and \
                                deltaMA10_now < 0 and deltaMA20_now < 0.2:
                            if self.buy_bear == 0:
                                self.buy_bear = 1
                                self.hk_trade_handler.bear_force_buy(self.trade_qty, 0.5)
                                print("buy bear q", self.ret.iloc[self.count,])




        return



    def cal_bull_decrease(self, position):
        start = 1250

        if position < start:
            self.ret.iloc[position, BULL_DECREASE_POS] = -1
            return

        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"

        ma10_ratio = self.ret["zma10_ratio"][position]
        curq = self.ret["zmaq"][position]

        if ma10_ratio >= 0 and self.ret["zma10_ratio"][position - 1] < 0:
            self.bull_decrease_max = curq
            self.bull_decrease_ma10_up = 1

        if ma10_ratio < 0 and self.ret["zma10_ratio"][position - 1] >= 0:
            self.bull_decrease_ma10_up = 0

        try:
            if self.bull_decrease_ma10_up == 1:

                if curq < self.bull_decrease_max:
                    gap = self.bull_decrease_max - curq
                else:
                    self.bull_decrease_max = curq
                    gap = 0
            else:
                gap = -1
        except:
            gap = -1

        self.ret.iloc[position, BULL_DECREASE_POS] = gap

        return

    def cal_bear_decrease(self, position):
        start = 1250

        if position < start:
            self.ret.iloc[position, BEAR_DECREASE_POS] = -1
            return

        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"

        ma10_ratio = self.ret["zma10_ratio"][position]
        curq = self.ret["zmaq"][position]

        if ma10_ratio <= 0 and self.ret["zma10_ratio"][position - 1] > 0:
            self.bear_decrease_max = curq
            self.bear_decrease_ma10_down = 1

        if ma10_ratio > 0 and self.ret["zma10_ratio"][position - 1] <= 0:
            self.bear_decrease_ma10_down = 0

        try:
            if self.bear_decrease_ma10_down == 1:

                if curq > self.bear_decrease_max:
                    gap = curq -  self.bear_decrease_max
                else:
                    self.bear_decrease_max = curq
                    gap = 0
            else:
                gap = -1
        except:
            gap = -1

        self.ret.iloc[position, BEAR_DECREASE_POS] = gap

        return

    def sell_bear_15th_oct(self):
        position = self.count
        bear_decrease = self.ret["bear_decrease"][position]
        zma10 = self.ret["zma10"][position]
        zma10_ratio = self.ret["zma10_ratio"][position]
        zma5 = self.ret["zma5"][position]

        if bear_decrease >= abs(zma10_ratio * 5):
            if self.buy_bear == 1:
                self.buy_bear = 0
                self.hk_trade_handler.bear_force_sell()
                print("buy bear5", self.ret.iloc[self.count,])

        if zma5 >= zma10 and self.ret["zma5"][position - 1] < self.ret["zma10"][position - 1]:
            if self.buy_bear == 1:
                self.buy_bear = 0
                self.hk_trade_handler.bear_force_sell()
                print("buy bearx", self.ret.iloc[self.count,])

        return

    def sell_bull_15th_oct(self):
        position = self.count
        bull_decrease = self.ret["bull_decrease"][position]
        zma10 = self.ret["zma10"][position]
        zma10_ratio = self.ret["zma10_ratio"][position]
        zma5 = self.ret["zma5"][position]

        if bull_decrease >= zma10_ratio * 5:
            if self.buy_bull == 1:
                self.buy_bull = 0
                self.hk_trade_handler.bull_force_sell()
                print("buy bull5", self.ret.iloc[self.count,])

        if zma5 <= zma10 and self.ret["zma5"][position - 1] > self.ret["zma10"][position - 1]:
            if self.buy_bull == 1:
                self.buy_bull = 0
                self.hk_trade_handler.bull_force_sell()
                print("buy bullx", self.ret.iloc[self.count,])

        return




    def buy_bull_13th_oct_no_delay(self):
        K_NO = 56
        if self.oct_13th_strategy_trade_time() == 0:
            return

        ma5_list = self.MA5_list
        vol_now = self.vol_now
        vol_last = self.vol_last
        MA20_vol = self.MA20_vol
        MA20_vol_last = self.MA20_vol_last
        cur = self.cur
        MA5_now = ma5_list[0]
        MA10_now = self.MA10_now
        MA20_now = self.MA20_now
        #MA50_cur = self.MA50_cur
        deltaMA10_now = self.deltaMA10_now
        deltaMA20_now = self.deltaMA20_now


        down_count = 0
        up_count = 0
        point = 0
        ma5_ok = 0
        ## VOL Break, and
        if vol_now >= MA20_vol and \
            self.ma_1m_table["open"][K_NO - 1] < self.ma_1m_table["close"][K_NO - 1]:

            ## 1. General Bull
            if ma5_list[0] - ma5_list[1] >= 2 and \
                (deltaMA10_now >= 0.9 or deltaMA20_now >= 0.72):
                for i in range(0, 9):
                    if ma5_list[i] > ma5_list[i + 1]:
                        up_count += 1
                        point += 1
                    else:
                        break

                if point >= 9:
                    return

                for i in range(point, 9):
                    if ma5_list[i] <= ma5_list[i + 1]:
                        down_count += 1

                if up_count <= 3 and down_count >= 1:
                    ma5_ok = 1

                if ma5_ok == 1:
                    if cur > MA5_now and \
                        MA10_now > MA20_now and \
                        MA5_now > MA20_now:
                        #### BUY BULL
                        if self.buy_bull == 0:
                            self.buy_bull = 1
                            self.hk_trade_handler.bull_force_buy(self.trade_qty, 0.5)
                        print("buy bull", self.ret.iloc[self.count,])


            ## 2. Quick Bull Start
            down_count = 0
            up_count = 0
            point = 0
            ma5_quick_ok = 0
            if ma5_list[0] - ma5_list[1] >= 4 and \
                (deltaMA10_now >= 0 or deltaMA20_now >= -0.4):
                for i in range(0, 9):
                    if ma5_list[i] > ma5_list[i + 1]:
                        up_count += 1
                        point += 1
                    else:
                        break

                if point >= 9:
                    return

                for i in range(point, 9):
                    if ma5_list[i] <= ma5_list[i + 1]:
                        down_count += 1

                if up_count <= 3 and down_count >= 1:
                    ma5_quick_ok = 1

                if ma5_quick_ok == 1:
                    if cur > MA5_now and \
                        MA10_now <= MA20_now and \
                        cur > MA10_now and cur > MA20_now :
                        #### BUY BULL
                        if self.buy_bull == 0:
                            self.buy_bull = 1
                            self.hk_trade_handler.bull_force_buy(self.trade_qty, 0.5)
                            print("buy bull q", self.ret.iloc[self.count,])

        return


    def buy_bull_13th_oct_delay(self):
        K_NO = 56
        if self.oct_13th_strategy_trade_time() == 0:
            return

        ma5_list = self.MA5_list

        vol_now = self.vol_now
        vol_last = self.vol_last
        MA20_vol = self.MA20_vol
        MA20_vol_last = self.MA20_vol_last
        cur =  self.cur
        MA5_cur = ma5_list[0]
        MA10_cur = self.MA10_cur
        MA20_cur = self.MA20_cur
        MA50_cur = self.MA50_cur
        deltaMA10_cur = self.deltaMA10_cur
        deltaMA20_cur = self.deltaMA20_cur

        down_count = 0
        up_count = 0
        point = 0
        ma5_ok = 0
        ## VOL Break, and
        if vol_last >= MA20_vol_last and vol_last <= MA20_vol_last * 3 and \
            self.ma_1m_table["open"][K_NO - 1] < self.ma_1m_table["close"][K_NO - 1]:

            ## General Bull
            if ma5_list[1] - ma5_list[2] >= 2 and \
                    (deltaMA10_cur >= 1 or deltaMA20_cur >= 0.8):
                for i in range(1, 9):
                    if ma5_list[i] > ma5_list[i + 1]:
                        up_count += 1
                        point += 1
                    else:
                        break

                if point >= 8:
                    return

                for i in range(point, 9):
                    if ma5_list[i] <= ma5_list[i + 1]:
                        down_count += 1

                if up_count <= 3 and down_count >= 1:
                    ma5_ok = 1

                if ma5_ok == 1:
                    if cur > MA5_cur and  MA10_cur > MA20_cur and \
                            MA5_cur > MA20_cur:
                        #### BUY BULL
                        if self.buy_bull == 0:
                            self.buy_bull = 1
                            self.hk_trade_handler.bull_force_buy(self.trade_qty, 1)
                            print("buy bull", self.ret.iloc[self.count,])

            ## Quick Bull Start
            if ma5_list[1] - ma5_list[2] >= 4 and \
                    (deltaMA10_cur >= 0 or deltaMA20_cur >= 0):
                for i in range(1, 9):
                    if ma5_list[i] > ma5_list[i + 1]:
                        up_count += 1
                        point += 1
                    else:
                        break

                if point >= 8:
                    return

                for i in range(point, 9):
                    if ma5_list[i] <= ma5_list[i + 1]:
                        down_count += 1

                if up_count <= 3 and down_count >= 1:
                    ma5_quick_ok = 1
                else:
                    ma5_quick_ok = 0

                if ma5_quick_ok == 1:
                    if cur > MA5_cur and  cur > MA10_cur and cur > MA20_cur and \
                        MA10_cur <= MA20_cur:
                        #### BUY BULL
                        if self.buy_bull == 0:
                            self.buy_bull = 1
                            self.hk_trade_handler.bull_force_buy(self.trade_qty, 1)
                            print("buy bull", self.ret.iloc[self.count,])


        return


    def oct_13th_strategy_trade_time(self):
        cur_time = self.data_time
        morning_start = "09:40:00"

        morning_start_list = morning_start.split(":")
        morning_start_second = int(morning_start_list[0]) * 3600 + int(morning_start_list[1]) * 60 + int(morning_start_list[2])


        cur_time_list = cur_time.split(":")
        cur_time_second = int(cur_time_list[0]) * 3600 + int(cur_time_list[1]) * 60 + int(cur_time_list[2])

        if cur_time_second > morning_start_second:
            return 1

        return 0


    def guard_vol_break(self):
        #print("VOL MA20:",self.MA20_vol, "Last:", self.vol_last, " now:",self.vol_now)
        if self.MA20_vol != 0:
            ratio = self.vol_last / self.MA20_vol
            if ratio >= 3:
                self.vol_break = 1
            else:
                ratio = self.vol_now / self.MA20_vol
                if ratio >= 2.5:
                    self.vol_break = 1
                else:
                    self.vol_break = 0

    def guard_bull(self):
        count = 26
        DECREASE_THRESHOLD = 10
        if self.deposit_bull == 0:
            sub = self.ma_1m_table.iloc[count - 2, 3] - self.ma_1m_table.iloc[count - 2, 2]
            if sub >= 0:
                self.deposit_bull = 0
                self.deposit_top = 0
                self.play.stop_play_stop_lossing_bull()
                #print("Guard Bull: reset green")
                return
            else:
                self.deposit_bull = abs(sub)
                if self.deposit_bull >= DECREASE_THRESHOLD:
                    self.play.play_stop_lossing_bull()
                    self.deposit_bull = 0
                    self.deposit_top = 0
                    #print("Guard Bull: warn directly")
                else:
                    self.deposit_top = self.ma_1m_table.iloc[count - 2, 2]
                    #print("Guard Bull: wait, find deposit")
                    return
        else:
        # we have a Green K bar that is less than VALUE
            new_deposit = self.cur - self.deposit_top
            if new_deposit <= DECREASE_THRESHOLD * (-1):
                self.play.play_stop_lossing_bull()
                self.deposit_bull = 0
                self.deposit_top = 0
                #print("Guard Bull: warn with deposit")
            else:
                sub = self.ma_1m_table.iloc[count - 2, 3] - self.ma_1m_table.iloc[count - 2, 2]
                if sub > 0:
                    if self.ma_1m_table.iloc[count - 2, 3] <= self.deposit_top:
                        self.deposit_bull = 0
                        self.deposit_top = 0
                        self.play.stop_play_stop_lossing_bull()
                        #print("Guard Bull: reset with deposit")
                #print("Guard Bull: wait with deposit " + str(self.deposit_top))
                return








    def warn_low_amplitude(self):
        try:
            cur_time = self.data_time
            cur_amplitude = self.cur_amplitude
        except:
            return
        AMPLITUDE_THRESHOLD = 0.4
        warn_seconds = 60
        alarm_time = "10:00:00"
        alarm_time_list = alarm_time.split(":")
        alarm_time_second = int(alarm_time_list[0]) * 3600 + int(alarm_time_list[1]) * 60 + int(alarm_time_list[2])
        cur_time_list = cur_time.split(":")
        cur_time_second = int(cur_time_list[0]) * 3600 + int(cur_time_list[1]) * 60 + int(cur_time_list[2])

        if cur_time_second > alarm_time_second and \
                        cur_time_second < alarm_time_second + warn_seconds:
            if cur_amplitude < AMPLITUDE_THRESHOLD:
                self.play.play_warn_low_amplitude()
            else:
                self.play.stop_play_warn_low_amplitude()

        return





    def is_trade_time(self, cur_time):
        #return 1
        morning_end = "11:59:58"
        noon_start = "13:00:01"

        morning_end_list = morning_end.split(":")
        morning_end_second = int(morning_end_list[0]) * 3600 + int(morning_end_list[1]) * 60 + int(morning_end_list[2])

        noon_start_list = noon_start.split(":")
        noon_start_second = int(noon_start_list[0]) * 3600 + int(noon_start_list[1]) * 60 + int(noon_start_list[2])

        cur_time_list = cur_time.split(":")
        cur_time_second = int(cur_time_list[0]) * 3600 + int(cur_time_list[1]) * 60 + int(cur_time_list[2])

        if cur_time_second > morning_end_second and cur_time_second < noon_start_second:
            return 0

        return 1

    def is_trade_limit_time(self):
        trade_end_time = "15:30:00"

        trade_end_time_list = trade_end_time.split(":")
        trade_end_time_second = int(trade_end_time_list[0]) * 3600 + int(trade_end_time_list[1]) * 60 + int(trade_end_time_list[2])

        cur_time_list = self.data_time.split(":")
        cur_time_second = int(cur_time_list[0]) * 3600 + int(cur_time_list[1]) * 60 + int(cur_time_list[2])

        if cur_time_second > trade_end_time_second:
            return 0

        return 1


    def get_cur_zma_quote(self):
        if self.count <= 1:
            return RET_ERROR, ""
        pos = self.count - 1
        data = []
        data.append({"No.": self.ret.iloc[pos, NO_POS], "cur": self.ret.iloc[pos, CUR_POS], "time": self.ret.iloc[pos, TIME_POS],
                     "zma10": self.ret.iloc[pos, ZMA10_POS], "zma20": self.ret.iloc[pos, ZMA20_POS],
                     "zma10_ratio": self.ret.iloc[pos, ZMA10_RATIO_POS], "zma20_ratio": self.ret.iloc[pos, ZMA20_RATIO_POS],"zma20_ratio_ratio": self.ret.iloc[pos, ZMA20_RATIO_RATIO_POS],
                     "zma_gap": self.ret.iloc[pos, ZMA_GAP_POS], "zma_gap_ratio": self.ret.iloc[pos, ZMA_GAP_RATIO_POS], "zma_gap_ratio_ratio": self.ret.iloc[pos, ZMA_GAP_RATIO_RATIO_POS],
                     "zma10_ratio_ratio": self.ret.iloc[pos, ZMA10_RATIO_RATIO_POS], "zma10_ratio_ratio_zma_ratio": self.ret.iloc[pos, ZMA10_RATIO_RATIO_RATIO_POS]
                     })
        zma_quote = pd.DataFrame(data,
                             columns=["No.", "cur", "time", "zma10", "zma20", "zma10_ratio", "zma20_ratio",
                                      "zma20_ratio_ratio", "zma_gap", "zma_gap_ratio",
                                      "zma_gap_ratio_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_zma_ratio"])
        return RET_OK, zma_quote

    def print_ma(self):
        print("delta MA50")
        print(str(self.deltaMA50_cur))
        print("delta MA20")
        print(str(self.deltaMA20_cur) + " " + str(self.deltaMA20_ma3) + " " + str(self.deltaMA20_ma5))
        print("delta MA10")
        print(str(self.deltaMA10_cur) + " " + str(self.deltaMA10_ma3) + " " + str(self.deltaMA10_ma5))
        print("MA10")
        print(str(self.MA10_cur) + " " + str(self.MA10_3))
        print("MA20")
        print(str(self.MA20_cur) + " " + str(self.MA20_3))
        print("MA50")
        print(str(self.MA50_cur) + " " + str(self.MA50_3))
        print("MA5 List")
        print(str(self.MA5_list))
        print("VOL")
        print(str(self.vol_now) + " " + str(self.vol_last) + " " + str(self.MA20_vol))

    def cal_cur_speed(self):
        if self.count > 40:
            #print("Changes in last 5s,10s,20s")
            self.cur_gap_5s = (self.ret.iloc[self.count, CUR_POS] - self.ret.iloc[self.count - 10, CUR_POS]) / 5
            self.cur_gap_10s = (self.ret.iloc[self.count, CUR_POS] - self.ret.iloc[self.count - 20, CUR_POS]) / 10
            self.cur_gap_20s = (self.ret.iloc[self.count, CUR_POS] - self.ret.iloc[self.count - 40, CUR_POS]) / 20
            #print(str(self.cur_gap_5s) + " " + str(self.cur_gap_10s) + " " + str(self.cur_gap_20s))


    def run(self):
        self.running = 1
        stock_quote = self.stock_quote
        stock_quote.start()
        while stock_quote.ready != 1 :
            time.sleep(1)

        self.hk_trade_handler.start()

        self.data_time = stock_quote.get_data_time()
        cur_stock_quoto = stock_quote.get_stock_quoto()
        self.cur = cur_stock_quoto
        cur_amplitude = stock_quote.get_stock_amplitude()
        self.cur_amplitude = cur_amplitude
        ret, tmp = stock_quote.get_1mK_line()
        if ret == 1:
            self.ma_1m_table = tmp
        while(1):
            if self.is_trade_time(self.data_time) == 1:
            ## In Trade Time
                start = time.time()
                self.is_available = 0
                self.count += 1
                self.ret.iloc[self.count, NO_POS] = self.count
                self.ret.iloc[self.count, CUR_POS] = cur_stock_quoto
                self.ret.iloc[self.count, TIME_POS] = self.data_time
                self.cal_zma10(self.count)
                #self.cal_zma20(self.count)
                self.cal_zma10_ratio_simple(self.count)
                self.cal_zma10_ratio_simple_ratio(self.count)
                self.cal_zma10_ratio_ratio_ratio_simple(self.count)
                #self.cal_zma10_ratio(self.count, 360)
                #self.cal_zma20_ratio(self.count, 360)
                #self.cal_zma_gap(self.count)
                self.cal_zmaq(self.count)
                self.cal_zma5(self.count)
                self.cal_bull_decrease(self.count)
                self.cal_bear_decrease(self.count)
                self.is_available = 1

                if stock_quote.ready == 1:
                    self.stock_quote = stock_quote
                    self.data_time = stock_quote.get_data_time()
                    cur_stock_quoto = stock_quote.get_stock_quoto()
                    self.cur = cur_stock_quoto
                    cur_amplitude = stock_quote.get_stock_amplitude()
                    self.cur_amplitude = cur_amplitude
                    ret, tmp = stock_quote.get_1mK_line()
                    if ret == 1:
                        self.ma_1m_table = tmp
                    self.deltaMA50_cur = stock_quote.get_deltaMA50_cur()
                    self.deltaMA20_now = stock_quote.get_deltaMA20_now()
                    self.deltaMA20_cur = stock_quote.get_deltaMA20_cur()
                    self.deltaMA20_ma3 = stock_quote.get_deltaMA20_ma3()
                    self.deltaMA20_ma5 = stock_quote.get_deltaMA20_ma5()
                    self.deltaMA10_now = stock_quote.get_deltaMA10_now()
                    self.deltaMA10_cur = stock_quote.get_deltaMA10_cur()
                    self.deltaMA10_ma3 = stock_quote.get_deltaMA10_ma3()
                    self.deltaMA10_ma5 = stock_quote.get_deltaMA10_ma5()
                    self.MA5_now = stock_quote.get_MA5_now()
                    self.MA5_list = stock_quote.get_MA5_List()
                    self.MA10_now = stock_quote.get_MA10_now()
                    self.MA10_cur = stock_quote.get_MA10_cur()
                    self.MA10_3 = stock_quote.get_MA10_3()
                    self.MA20_now = stock_quote.get_MA20_now()
                    self.MA20_cur = stock_quote.get_MA20_cur()
                    self.MA20_3 = stock_quote.get_MA20_3()
                    self.MA50_cur = stock_quote.get_MA50_cur()
                    self.MA50_3 = stock_quote.get_MA50_3()
                    self.MA20_vol = stock_quote.get_ma20_vol()
                    self.MA20_vol_last = stock_quote.get_ma20_vol_last()
                    self.vol_last = stock_quote.get_vol_last()
                    self.vol_now = stock_quote.get_vol_now()
                    self.bull_bid_seller = stock_quote.get_bull_bid_seller()
                    self.bull_ask_seller = stock_quote.get_bull_ask_seller()
                    self.bear_bid_seller = stock_quote.get_bear_bid_seller()
                    self.bear_ask_seller = stock_quote.get_bear_ask_seller()
                else:
                    cur_stock_quoto = self.ret.iloc[self.count, CUR_POS]
                    self.cur = cur_stock_quoto

                #self.print_ma()
                self.cal_cur_speed()
                self.determine_direction()
                self.refresh_zma10_ratio_simple(self.count)
                self.guard_vol_break()
                #self.detect_zma10_decrease()
                self.detect_zma10_decrease_start()
                # Detect Empty and Buy
                #self.detect_empty_decrease()

                self.buy_bear_13th_oct_no_delay()
                self.sell_bear_15th_oct()
                # self.guard_burst()
                # self.guard_bear()
                # self.guard_bear2()

                #self.detect_empty_start()


                self.buy_bull_13th_oct_no_delay()
                self.sell_bull_15th_oct()
                #self.guard_bull()
                #self.empty_head()
                #self.many_head()
                #self.first_10min_warning()
                #self.warn_bull_recover()
                #self.warn_recover_bull_down_trend()
                #self.warn_bogus_break()
                #self.warn_low_amplitude()
                #self.warn_ma_low()
                #self.disable_adverse_bull()
                #self.disable_adverse_bear()
                #self.print_ma()

                #print(self.ret.iloc[self.count,])
                end = time.time()
                dur = end - start
                if dur > self.interval:
                    time.sleep(0)
                else:
                    time.sleep(self.interval - dur)
            else:
                ## Not in Trade Time
                self.is_available = 0
                time.sleep(self.interval)
                self.data_time = stock_quote.get_data_time()

            ## Check Quote Status
            if stock_quote.is_alive() == False:
                try:
                    self.stock_quote = get_stock_quote(self.__quote_ctx)
                    stock_quote = self.stock_quote
                    print("quote dies. Restart")
                    stock_quote.start()
                except:
                    print("Restart Quote Fail. Exit!")
                    #print("quote_ctx alive ", self.__quote_ctx.is_run())
                    break

            if self.hk_trade_handler.is_alive() == False:
                try:
                    self.hk_trade_handler = hk_trade_handler(self.opt, self.stock_quote, self.bull_code, self.bear_code)
                    self.hk_trade_handler.start()
                except:
                    print("Restart trade handler Fail. Exit!")
                    break

            if self.ret.iloc[self.count, TIME_POS] == self.ret.iloc[self.count - 10, TIME_POS]:
                break

            if self.count >= 59990:
                break

        print("MAIN THREAD DIE!!!!!!!!!!!")
        self.running = 0


