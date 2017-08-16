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
CUR_RATIO_RATIO_POS = 12


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
        self.cur_zma10_ratio_simple_ratio = 0
        self.cur_zma10_ratio_simple_ratio_0 = 0
        self.ret= []
        self.interval = 0.5
        self.count = 0
        self.is_available = 0
        self.play = play
        self.direction = 0
        data= []
        for i in range(0, 60000):
            data.append({"No.": 0})
        self.ret = pd.DataFrame(data, columns=["No.", "cur", "time", "zma10", "zma20", "zma10_ratio", "zma20_ratio",
                                               "zma20_ratio_ratio", "zma_gap", "zma_gap_ratio", "zma_gap_ratio_ratio", "zma10_ratio_ratio", "cur_ratio"])

        self.bear_code = 62162
        self.bull_code = 69512
        self.hk_trade = hk_trade_api()
        self.hk_trade.initialize()
        self.hk_trade.unlock_trade('88888888', '584679')
        self.opt = hk_trade_opt(self.hk_trade)
        self.stock_quote = get_stock_quote(self.__quote_ctx, "HK." + str(self.bull_code), "HK." + str(self.bear_code))
        self.hk_trade_handler_bear = hk_trade_handler(self.opt, self.stock_quote, self.bear_code)
        # self.opt.disble_order_stock_code(67863)
        #    localid = opt.buy(0.06, 10000, "67541")
        #    orderid = opt.get_order_id(localid)
        #    status = opt.check_order_status(orderid)
        #    dealt = opt.get_dealt_qty(orderid)
        #    print(dealt)
        #    opt.disable_order(orderid)




    ## MA
    def cal_zma10(self, position):
        len = 1200
        sum = 0
        if position < len :
            return -1
        if position == len :
            for j in range(0, len):
                sum += self.ret["cur"][len + 1 - 1 - j]
            avr0 = sum / len
            self.ret.iloc[position, ZMA10_POS] = avr0
            return 1
        starter = self.ret["cur"][position - len ]
        avr = self.ret["zma10"][position -1] - starter/len + self.ret["cur"][position]/len
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

    def cal_cur_ratio(self, position):
        len = 360
        t = 360
        val =0
        start_pos = len + t
        if position < start_pos:
          return -1

        ret, val = self.optimized_least_square_method(position - t + 1, position, "cur")
        if ret == -1:
            val = 0
        self.ret.iloc[position, CUR_RATIO_RATIO_POS] = val * 10000
        return 1

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
        print("ratio ratio ma10: ",self.cur_zma10_ratio_simple_ratio )
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
        count = 26

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
                        print("WARN!!!! SELL BEAR!!! Over Tolerance")
                        sell_bear = 1
                else:
                    if score > limit:
                        print("WARN!!!! SELL BEAR!!!")
                        sell_bear = 1
                pointer += 1
            else:
                long_gap = ma_1m_table.iloc[observe_num - 2, close_pos] - ma_1m_table.iloc[lowest_pos, low_pos]
                if long_gap < 0:
                    print("ERROR!!! LONG GAP ERROR!!!")
                score += long_gap
                if score > limit:
                    tolerance = extra_tolerance
                    print("Assign Tollerance")
                pointer = observe_num - 1
        print("SCORE: " + str(score))
        if sell_bear == 1:
            self.play.play_stop_lossing_bear_inst()
            #self.opt.clear_stock_code(self.bear_code, self.bear_bid_seller)
            if self.hk_trade_handler_bear.is_alive() == False:
                self.hk_trade_handler_bear = hk_trade_handler(self.opt, self.stock_quote, self.bear_code)
                self.hk_trade_handler_bear.start()
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
        print(cur_zma10_ratio_simple_ratio, "AAAAAAAA", cur_zma10_ratio_simple_ratio_0)
        return

## Require zma10_decrease
    def detect_empty_start(self):
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
                    self.cur < self.MA10_cur:
                    print("BUY BUY BUY!!!")
                    self.zma10_new_trend = -9999

        return


    def guard_bull(self):
        count = 26
        DECREASE_THRESHOLD = 10
        if self.deposit_bull == 0:
            sub = self.ma_1m_table.iloc[count - 2, 3] - self.ma_1m_table.iloc[count - 2, 2]
            if sub >= 0:
                self.deposit_bull = 0
                self.deposit_top = 0
                self.play.stop_play_stop_lossing_bull()
                print("Guard Bull: reset green")
                return
            else:
                self.deposit_bull = abs(sub)
                if self.deposit_bull >= DECREASE_THRESHOLD:
                    self.play.play_stop_lossing_bull()
                    self.deposit_bull = 0
                    self.deposit_top = 0
                    print("Guard Bull: warn directly")
                else:
                    self.deposit_top = self.ma_1m_table.iloc[count - 2, 2]
                    print("Guard Bull: wait, find deposit")
                    return
        else:
        # we have a Green K bar that is less than VALUE
            new_deposit = self.cur - self.deposit_top
            if new_deposit <= DECREASE_THRESHOLD * (-1):
                self.play.play_stop_lossing_bull()
                self.deposit_bull = 0
                self.deposit_top = 0
                print("Guard Bull: warn with deposit")
            else:
                sub = self.ma_1m_table.iloc[count - 2, 3] - self.ma_1m_table.iloc[count - 2, 2]
                if sub > 0:
                    if self.ma_1m_table.iloc[count - 2, 3] <= self.deposit_top:
                        self.deposit_bull = 0
                        self.deposit_top = 0
                        self.play.stop_play_stop_lossing_bull()
                        print("Guard Bull: reset with deposit")
                print("Guard Bull: wait with deposit " + str(self.deposit_top))
                return

    def empty_head(self):
        K_NO = 26
        MA10_THRESHOLD = 1.4
        MA20_THRESHOLD = 0.7
        GAP_DOWN = 0.5
        GAP_UP = 20
        K_GROW_THRESHOLD = 10

        ret_0 = 99
        str_0 = "ERROR``````````````````````"
        ret_1 = 99
        str_1 = "ERROR````````"
        # MA Conditions
        if self.deltaMA10_ma3 < 0 and \
                        self.deltaMA20_ma3 < 0 and \
                        self.MA10_cur < self.MA20_cur:
            if abs(self.deltaMA10_ma3) > MA10_THRESHOLD and \
                    abs(self.deltaMA20_ma3) > MA20_THRESHOLD:
                gap = self.MA20_3 - self.MA10_3
                if gap > GAP_DOWN and gap < GAP_UP:
                    ret_0 = 0
                else:
                    # GAP problem
                    ret_0 = 3
            else:
                # Rates are too small
                ret_0 = 2
        else:
            # Not goes down together
            ret_0 = 1

        # K-line conditions

        ### Increase Calculation
        key_values = [self.ma_1m_table.iloc[K_NO - 3, 2], self.ma_1m_table.iloc[K_NO - 3, 3], self.ma_1m_table.iloc[K_NO - 2, 3], self.ma_1m_table.iloc[K_NO - 1, 3]]
        color = [0, 0, 0]
        if key_values[1] - key_values[0] > 0:
            color[0] = 1

        if key_values[2] - key_values[1] > 0:
            color[1] = 1

        if key_values[3] - key_values[2] > 0:
            color[2] = 1

        increase = 0
        if color[1] == 1 and color[1] == 1 and color[2] == 1:
            increase = key_values[3] - key_values[0]

        if color[1] == 1 and color[1] == 1 and color[2] == 0:
            increase = key_values[2] - key_values[0]

        if color[1] == 1 and color[1] == 0 and color[2] == 1:
            if key_values[0] > key_values[2]:
                val1 = key_values[1] - key_values[0]
                val2 = key_values[3] - key_values[2]
                if val1 > val2:
                    increase = val1
                else:
                    increase = val2
            else:
                increase = key_values[3] - key_values[0]

        if color[1] == 1 and color[1] == 0 and color[2] == 0:
            increase = key_values[1] - key_values[0]

        if color[0] == 0 and color[1] == 1 and color[2] == 1:
            increase = key_values[3] - key_values[1]

        if color[0] == 0 and color[1] == 1 and color[2] == 0:
            increase = key_values[2] - key_values[1]

        if color[0] == 0 and color[1] == 0 and color[2] == 1:
            increase = key_values[3] - key_values[2]

        if color[0] == 0 and color[1] == 0 and color[2] == 0:
            increase = 0

        #### Compare with Threshold
        if increase >= K_GROW_THRESHOLD:
            ret_1 = 1
        else:
            ret_1 = 0

        if ret_0 == 0:
            str_0 = "MA is OK```````````````````"
        if ret_0 == 1:
            str_0 = "MA do not go down``````````"
        if ret_0 == 2:
            str_0 = "MA changes rate are not big"
        if ret_0 == 3:
            str_0 = "MA Gap is not proper```````"
        if ret_1 == 0:
            str_1 = "K-Line is OK`"
        if ret_1 == 1:
            str_1 = "K-Line is bad"
        if ret_0 == 0 and ret_1 == 0:
            ret = "GO GO GO"
            self.play.play_start_bear()
        else:
            ret = "XX XX XX"
            self.play.stop_play_start_bear()
        print("EMPTY HEAD" + " | " + ret + " | " + str_0 + " | " + str_1)
        return

    def many_head(self):
        K_NO = 26
        MA10_THRESHOLD = 1.8
        MA20_THRESHOLD = 1.4
        GAP_DOWN = 3
        GAP_UP = 20
        K_MA10_THRESHOLD = 4
        # MA Conditions
        if self.deltaMA10_ma3 > 0 and \
                        self.deltaMA20_ma3 > 0 and \
                        self.MA10_cur > self.MA20_cur and \
                        self.MA10_3 > self.MA20_3:
            if abs(self.deltaMA10_ma3) > MA10_THRESHOLD and \
                    abs(self.deltaMA20_ma3) > MA20_THRESHOLD:
                gap = self.MA10_3 - self.MA20_3
                if gap > GAP_DOWN and gap < GAP_UP:
                    ret_0 = 0
                else:
                    # GAP problem
                    ret_0 = 3
            else:
                # Rates are too small
                ret_0 = 2
        else:
            # Not goes down together
            ret_0 = 1

        k_ma10_gap = self.ma_1m_table.iloc[K_NO - 2, 3] - self.MA10_cur

        if (k_ma10_gap <= K_MA10_THRESHOLD and k_ma10_gap >= 0) or k_ma10_gap < 0:
            ret_1 = 0
        else:
            ret_1 = 1

        if ret_0 == 0:
            str_0 = "MA is OK```````````````````"
        if ret_0 == 1:
            str_0 = "MA do not go up````````````"
        if ret_0 == 2:
            str_0 = "MA changes rate are not big"
        if ret_0 == 3:
            str_0 = "MA Gap is not proper```````"
        if ret_1 == 0:
            str_1 = "K-Line is OK`"
        if ret_1 == 1:
            str_1 = "K-Line is bad"
        if ret_0 == 0:
            ret = "GO GO GO"
            self.play.play_start_bull()
        else:
            ret = "XX XX XX"
            self.play.stop_play_start_bull()
        print("MANY  HEAD" + " | " + ret + " | " + str_0 + " | " + str_1)
        return

    def warn_recover_bull_down_trend(self):
        K_NO = 26
        MA10_THRESHOLD = 1.5
        MA20_THRESHOLD = 0.8

        ret_0 = 99
        str_0 = "ERROR``````````````````````"
        ret_1 = 99
        str_1 = "ERROR````````"
        # MA Conditions
        if self.deltaMA20_ma3 < 0 and \
                        self.MA10_cur < self.MA20_cur:
            if abs(self.deltaMA10_ma3) < MA10_THRESHOLD and \
                abs(self.deltaMA20_ma3) > MA20_THRESHOLD and \
                    abs(self.deltaMA10_ma3) < abs(self.deltaMA20_ma3):
                ret_0 = 0
            else:
                # Rates are too small
                ret_0 = 2
        else:
            # Not goes down together
            ret_0 = 1

        if ret_0 == 0:
            str_0 = "MA is OK```````````````````"
        if ret_0 == 1:
            str_0 = "MA do not go down``````````"
        if ret_0 == 2:
            str_0 = "MA changes rate bad````````"
        if ret_0 == 0:
            ret = "GO GO GO"
            self.play.play_bull_recover_down_trend()
        else:
            ret = "XX XX XX"
            self.play.stop_play_bull_recover_down_trend()
        print("BullRecover" + "| " + ret + " | " + str_0 + " | " + str_1)
        return

    def warn_bogus_break(self):
        MA20_THRESHOLD = -0.6
        CH_RATE_THRESHOLD = -0.5
        try:
            ch_rate_20s = self.cur_gap_20s
            deltaMA20 = self.deltaMA20_ma3
        except:
            return

        if deltaMA20 > MA20_THRESHOLD and ch_rate_20s < CH_RATE_THRESHOLD:
            self.play.play_warn_bogus_break()
        else:
            self.play.stop_play_warn_bogus_break()
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

    def disable_adverse_bull(self):
        # Disable Bull when MA20 decreases sharply
        MA20_THRESHOLD = -2
        try:
            deltaMA20 = self.deltaMA20_ma3
        except:
            return

        if deltaMA20 <= MA20_THRESHOLD:
            self.opt.disble_order_stock_code(self.bull_code)

        return

    def disable_adverse_bear(self):
        # Disable Bear when cur > MA10 and MA10,Ma20 increase
        MA10_THRESHOLD = 0.7
        MA20_THRESHOLD = 0.5
        try:
            deltaMA20 = self.deltaMA20_ma3
            deltaMA10 = self.deltaMA10_ma3
            ma10 = self.MA10_cur
            ma20 = self.MA20_cur
            cur = self.cur
        except:
            return

        if deltaMA20 >= MA20_THRESHOLD and deltaMA10 >= MA10_THRESHOLD and \
                ma10 > ma20 and cur > ma10:
            self.opt.disble_order_stock_code(self.bear_code)

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


    def get_cur_zma_quote(self):
        if self.count <= 1:
            return RET_ERROR, ""
        pos = self.count - 1
        data = []
        data.append({"No.": self.ret.iloc[pos, NO_POS], "cur": self.ret.iloc[pos, CUR_POS], "time": self.ret.iloc[pos, TIME_POS],
                     "zma10": self.ret.iloc[pos, ZMA10_POS], "zma20": self.ret.iloc[pos, ZMA20_POS],
                     "zma10_ratio": self.ret.iloc[pos, ZMA10_RATIO_POS], "zma20_ratio": self.ret.iloc[pos, ZMA20_RATIO_POS],"zma20_ratio_ratio": self.ret.iloc[pos, ZMA20_RATIO_RATIO_POS],
                     "zma_gap": self.ret.iloc[pos, ZMA_GAP_POS], "zma_gap_ratio": self.ret.iloc[pos, ZMA_GAP_RATIO_POS], "zma_gap_ratio_ratio": self.ret.iloc[pos, ZMA_GAP_RATIO_RATIO_POS],
                     "zma10_ratio_ratio": self.ret.iloc[pos, ZMA10_RATIO_RATIO_POS], "cur_ratio": self.ret.iloc[pos, CUR_RATIO_RATIO_POS]
                     })
        zma_quote = pd.DataFrame(data,
                             columns=["No.", "cur", "time", "zma10", "zma20", "zma10_ratio", "zma20_ratio",
                                      "zma20_ratio_ratio", "zma_gap", "zma_gap_ratio",
                                      "zma_gap_ratio_ratio", "zma10_ratio_ratio", "cur_ratio"])
        return RET_OK, zma_quote

    def print_ma(self):
        print("delta MA20")
        print(str(self.deltaMA20_cur) + " " + str(self.deltaMA20_ma3) + " " + str(self.deltaMA20_ma5))
        print("delta MA10")
        print(str(self.deltaMA10_cur) + " " + str(self.deltaMA10_ma3) + " " + str(self.deltaMA10_ma5))
        print("MA10")
        print(str(self.MA10_cur) + " " + str(self.MA10_3))
        print("MA20")
        print(str(self.MA20_cur) + " " + str(self.MA20_3))


    def cal_cur_speed(self):
        if self.count > 40:
            print("Changes in last 5s,10s,20s")
            self.cur_gap_5s = (self.ret.iloc[self.count, CUR_POS] - self.ret.iloc[self.count - 10, CUR_POS]) / 5
            self.cur_gap_10s = (self.ret.iloc[self.count, CUR_POS] - self.ret.iloc[self.count - 20, CUR_POS]) / 10
            self.cur_gap_20s = (self.ret.iloc[self.count, CUR_POS] - self.ret.iloc[self.count - 40, CUR_POS]) / 20
            print(str(self.cur_gap_5s) + " " + str(self.cur_gap_10s) + " " + str(self.cur_gap_20s))


    def run(self):
        stock_quote = self.stock_quote
        stock_quote.start()
        while stock_quote.ready != 1 :
            time.sleep(1)

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
                #self.cal_zma10_ratio(self.count, 360)
                #self.cal_zma20_ratio(self.count, 360)
                #self.cal_zma_gap(self.count)

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
                    self.deltaMA20_cur = stock_quote.get_deltaMA20_cur()
                    self.deltaMA20_ma3 = stock_quote.get_deltaMA20_ma3()
                    self.deltaMA20_ma5 = stock_quote.get_deltaMA20_ma5()
                    self.deltaMA10_cur = stock_quote.get_deltaMA10_cur()
                    self.deltaMA10_ma3 = stock_quote.get_deltaMA10_ma3()
                    self.deltaMA10_ma5 = stock_quote.get_deltaMA10_ma5()
                    self.MA10_cur = stock_quote.get_MA10_cur()
                    self.MA10_3 = stock_quote.get_MA10_3()
                    self.MA20_cur = stock_quote.get_MA20_cur()
                    self.MA20_3 = stock_quote.get_MA20_3()
                    self.bull_bid_seller = stock_quote.get_bull_bid_seller()
                    self.bull_ask_seller = stock_quote.get_bull_ask_seller()
                    self.bear_bid_seller = stock_quote.get_bear_bid_seller()
                    self.bear_ask_seller = stock_quote.get_bear_ask_seller()
                else:
                    cur_stock_quoto = self.ret.iloc[self.count, CUR_POS]
                    self.cur = cur_stock_quoto

                self.print_ma()
                self.cal_cur_speed()
                self.determine_direction()
                self.refresh_zma10_ratio_simple(self.count)
                self.detect_zma10_decrease()
                self.detect_empty_start()

                self.guard_burst()
                #self.guard_bear()
                self.guard_bear2()

                #self.guard_bull()
                self.empty_head()
                self.many_head()
                self.first_10min_warning()
                self.warn_bull_recover()
                self.warn_recover_bull_down_trend()
                self.warn_bogus_break()
                self.warn_low_amplitude()
                #self.warn_ma_low()
                #self.disable_adverse_bull()
                #self.disable_adverse_bear()


                print(self.ret.iloc[self.count,])
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
                self.stock_quote = get_stock_quote(self.__quote_ctx)
                stock_quote = self.stock_quote
                print("quote dies. Restart")
                stock_quote.start()




