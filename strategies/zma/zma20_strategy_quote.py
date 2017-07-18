from data_src.stock_info.get_stock_quote import *
import threading
import time
import pandas as pd
from ui.PlaySound import *
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

        self.ret= []
        self.interval = 0.5
        self.count = 0
        self.is_available = 0
        self.play = play
        self.direction = 0
        data= []
        for i in range(0, 50000):
            data.append({"No.": 0})
        self.ret = pd.DataFrame(data, columns=["No.", "cur", "time", "zma10", "zma20", "zma10_ratio", "zma20_ratio",
                                               "zma20_ratio_ratio", "zma_gap", "zma_gap_ratio", "zma_gap_ratio_ratio", "zma10_ratio_ratio", "cur_ratio"])



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
    def cal_zma10_ratio(self, position):
        len = 1200
        t = 60
        val =0
        start_pos = len + t
        if position < start_pos:
          return -1

        ret, val = self.optimized_least_square_method(position - t + 1, position, "zma10")
        if ret == -1:
            val = 0
        self.ret.iloc[position, ZMA10_RATIO_POS] = val  * 120
        return 1

    def cal_zma20_ratio(self, position):
        len = 2400
        t = 60
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
        UP_THRESHOLD = 0.3
        DOWN_THRESHOLD = -0.3
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


    def guard_bear(self):
        count = 26
        GROWTH_THRESHOLD = 10
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
        GAP_DOWN = 3
        GAP_UP = 20
        K_GROW_THRESHOLD = 10

        ret_0 = 99
        str_0 = "ERROR``````````````````````"
        ret_1 = 99
        str_1 = "ERROR````````"
        # MA Conditions
        if self.deltaMA10_ma3 < 0 and \
                        self.deltaMA20_ma3 < 0 and \
                        self.MA10_cur < self.MA20_cur and \
                        self.MA10_3 < self.MA20_3:
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


    def is_trade_time(self, cur_time):
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
        stock_quote = get_stock_quote(self.__quote_ctx)
        stock_quote.start()
        while stock_quote.ready != 1:
            time.sleep(1)

        self.data_time = stock_quote.get_data_time()
        cur_stock_quoto = stock_quote.get_stock_quoto()
        self.cur = cur_stock_quoto
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
                self.cal_zma20(self.count)
                self.cal_zma10_ratio(self.count)
                self.cal_zma20_ratio(self.count)
                self.cal_zma_gap(self.count)

                self.is_available = 1

                if stock_quote.ready == 1:
                    self.data_time = stock_quote.get_data_time()
                    cur_stock_quoto = stock_quote.get_stock_quoto()
                    self.cur = cur_stock_quoto
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
                else:
                    cur_stock_quoto = self.ret.iloc[self.count, CUR_POS]
                    self.cur = cur_stock_quoto

                self.determine_direction()
                self.guard_burst()
                self.guard_bear()
                self.guard_bull()
                self.empty_head()
                self.many_head()
                self.print_ma()
                self.cal_cur_speed()
                self.first_10min_warning()

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
                stock_quote = get_stock_quote(self.__quote_ctx)
                print("quote dies. Restart")
                stock_quote.start()




