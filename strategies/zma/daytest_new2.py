from db.db_ma_trend import *
#from openft.open_quant_context import *
import pandas as pd
import time
import math
from ui.show_plots import *


# "No.", "cur", "time", "zma10", "zma20", "zma10_ratio", "zma20_ratio", "zma20_ratio_ratio", "zma_gap", "zma_gap_ratio", "zma_gap_ratio_ratio",

##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
NO_POS = 0
CUR_POS = 1
TIME_POS = 2
ZMA10_POS = 3
ZMA20_POS = 4
ZMA10_RATIO_POS = 5
ZMA10_RATIO_RATIO_POS = 6
ZMA10_RATIO_RATIO_RATIO_POS = 7
TRADE_MARK_POS = 8
MA20_RATIO_POS = 9
ZMA10_RATIO_RATIO_SHORT_POS = 10
ZMA5_POS = 13
ZMA5_RATIO_POS = 14
ZMA1_POS = 15
ZMA1_RATIO_POS = 16
ZMA1_RATIO_SHORT_POS = 17
ZMA1_ZMA10_GAP_POS = 18
ZMA1_ZMA10_GAP_SCOPE_POS = 19
ZMA5_RATIO_RATIO_POS = 20
ZMA1_RATIO_RATIO_POS = 21
ZMA50_POS = 22
ZMA50_RATIO_POS = 23

NO_SRC_POS = 0
CUR_SRC_POS = 3
TIME_SRC_POS = 8

NO_SRC_NEW_POS = 0
CUR_SRC_NEW_POS = 1
MA10_R_SRC_NEW_POS = 2
MA20_SRC_NEW_POS = 3
MA20_R_SRC_NEW_POS = 5
TIME_SRC_NEW_POS = 6

class adjust_paras:
    def __init__(self):
        self.index = 0
        self.zma10_ratio_sh = 0
        self.zma20_ratio_sh = 0
        self.zma10_ratio_ratio_sh = 0
        self.zma20_ratio_ratio_sh = 0
        self.zma_gap_min_sh = 0
        self.zma_gap_max_sh = 9999
        self.zma_gap_ratio_sh = 0
        self.zma_gap_ratio_ratio_sh = 0
        self.zma20_sh = 0
        self.cur_ratio_sh = 0


class daytest:
    def __init__(self):
        self.count = 0
        self.daytestcount = 0
        self.tmp = 0
        self.trend_c_cnt = 0
        self.trend = 0
        self.trend_p_cnt = 0

    def Initialize(self):
        self.db = MySQLCommand("localhost", 3306, "root", "123456", "trend2")
        self.db.connectMysql()
        self.op = dbop_ma_trand()
        self.mydb = MySQLCommand("localhost", 3306, "root", "123456", "day_review_01")
        self.mydb.connectMysql()
        self.myop = dbop_ma_trand()

    ##
    # Operation on Database: day_review_01
    def queryDayTestData(self,start, end):
        self.daytestcount = self.myop.dbop_read_day_data(self.mydb, start, end)
        if self.daytestcount == 0:
            return -1
        return self.daytestcount

    def getNextDayTestData(self):
        ret = self.myop.dbop_read_day_data_next(self.mydb)
        return ret

    def parseDayTestData(self):
        data = []
        for i in range(0, self.daytestcount):
            line = self.getNextDayTestData()
            data.append({"No.": line[NO_POS], "cur": line[CUR_POS], "time":line[TIME_POS], "zma10":line[ZMA10_POS],  "ma20":line[ZMA20_POS],
                         "zma10_ratio":line[ZMA10_RATIO_POS],"zma10_ratio_ratio": line[ZMA10_RATIO_RATIO_POS], "zma10_ratio_ratio_ratio": line[ZMA10_RATIO_RATIO_RATIO_POS], "trade_mark": line[TRADE_MARK_POS], "ma20_ratio": line[MA20_RATIO_POS],
                         "zma10_ratio_ratio_short": line[ZMA10_RATIO_RATIO_SHORT_POS], "bull_decrease": 0 ,"zmab":0, "zma5":0, "zma5_ratio":0,
                         "zma1":0, "zma1_ratio":0,"zma1_ratio_short":0,"zma1_zma10_gap":0, "zma1_zma10_gap_scope":0, "zma5_ratio_ratio":0,
                         "zma1_ratio_ratio": 0, "ma50": 0})

        self.ret = pd.DataFrame(data, columns=["No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio","zma10_ratio_ratio_ratio", "trade_mark", "ma20_ratio","zma10_ratio_ratio_short",
                                               "bull_decrease","zmab","zma5","zma5_ratio", "zma1", "zma1_ratio", "zma1_ratio_short","zma1_zma10_gap","zma1_zma10_gap_scope","zma5_ratio_ratio","zma1_ratio_ratio","ma50"])
        return self.ret

    def addDayTestData(self, data):
        len = 0
        for index in data.iterrows():
             len += 1
        for i in range(1800, len):
             self.myop.dbop_add_day_data(self.mydb, data["No."][i], data["cur"][i], data["time"][i],
                                        data["zma10"][i], data["ma20"][i],
                                        data["zma10_ratio"][i], data["zma10_ratio_ratio"][i],
                                        data["zma10_ratio_ratio_ratio"][i], data["trade_mark"][i], data["ma20_ratio"][i], data["zma10_ratio_ratio_short"][i],)

    def updateDayTestData_trade_mark(self, data):
        len = 0
        for index in data.iterrows():
            len += 1
        for i in range(0, len):
            self.myop.dbop_update_day_data_trade_mark(self.mydb, data["No."][i], data["trade_mark"][i])
##
# Operation on Database: trend

    ##
    # Operation on Database: trend
    def queryData(self, start, end ):
        self.count = self.op.dbop_read_day_data_standard(self.db, start, end)
        if self.count == 0:
            return -1
        return self.count

    def getNextData(self):
        ret = self.op.dbop_read_day_data_standard_next(self.db)
        return ret

    def parse_data(self):
        data = []
        pre_cur = 0
        for i in range(0, self.count):
            line = self.getNextData()
            if line[CUR_SRC_POS] == 0:
                #data.append({"No.": line[NO_SRC_NEW_POS], "cur": pre_cur, "time": line[TIME_SRC_NEW_POS], "ma20": line[MA20_SRC_NEW_POS], "ma20_ratio": line[MA20_R_SRC_NEW_POS], "trade_mark": 0})
                data.append(
                    {"No.": line[NO_SRC_NEW_POS], "cur": pre_cur, "time": line[TIME_SRC_NEW_POS], "zma10": 0,
                     "ma20": line[MA20_SRC_NEW_POS], "zma10_ratio": 0,
                     "zma10_ratio_ratio": 0,
                     "zma10_ratio_ratio_ratio": 0, "trade_mark": 0,
                     "ma20_ratio": line[MA20_R_SRC_NEW_POS], "zma10_ratio_ratio_short": 0, "zma5": 0})

            else:
                #data.append({"No.": line[NO_SRC_NEW_POS], "cur": line[CUR_SRC_NEW_POS], "time": line[TIME_SRC_NEW_POS], "ma20": line[MA20_SRC_NEW_POS], "ma20_ratio": line[MA20_R_SRC_NEW_POS], "trade_mark": 0})
                data.append(
                    {"No.": line[NO_SRC_NEW_POS], "cur": line[CUR_SRC_NEW_POS], "time": line[TIME_SRC_NEW_POS], "zma10": 0,
                     "ma20": line[MA20_SRC_NEW_POS], "zma10_ratio": 0,
                     "zma10_ratio_ratio": 0,
                     "zma10_ratio_ratio_ratio": 0, "trade_mark": 0,
                     "ma20_ratio": line[MA20_R_SRC_NEW_POS], "zma10_ratio_ratio_short": 0, "zma5": 0})
            pre_cur =line[CUR_SRC_POS]
        self.ret = pd.DataFrame(data, columns=["No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark", "ma20_ratio", "zma10_ratio_ratio_short", "zma5"])

        return self.ret

    ## Cur Ratio
    ## Dur = 3 min
    def cal_cur_ratio(self):
        len = 0
        t = 360
        val =0
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            ret, val = self.optimized_least_square_method(i - t + 1, i, "cur")
            if ret == -1:
                val = 0
            val *= 1000000
            val = round(val, 4)
            self.ret.iloc[i, CUR_RATIO_POS] = val
        return 1

    def cal_zma1_zma10_gap(self):
        len = 0
        val =0
        start_pos = len
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            gap = self.ret.iloc[i, ZMA1_POS] - self.ret.iloc[i, ZMA10_POS]
            self.ret.iloc[i, ZMA1_ZMA10_GAP_POS] = gap
        return 1

    def cal_zma1_zma10_gap_scope(self, sample = 120):
        len = 0
        t = sample
        val =0
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            ret, val = self.optimized_least_square_method(i - t + 1, i, "zma1_zma10_gap")
            if ret == -1:
                val = 0
            val = round(val, 4)
            self.ret.iloc[i, ZMA1_ZMA10_GAP_SCOPE_POS] = val
        return 1

    def cal_ma50(self):
        len = 3600
        avg_sum = 0
        start_pos = len - 1
        if self.count < len:
            return -1
        for i in range(0, len + 1):
            self.ret.iloc[i, ZMA50_POS] = self.ret["cur"][0]

        for i in range(start_pos + 1, self.count):
            sum = self.ret["ma20"][i] * 20 + self.ret["ma20"][i - 2400] * 20 + self.ret["zma10"][i - 3600] * 10
            avr = sum / 50
            self.ret.iloc[i, ZMA50_POS] = avr
        return 0


    ## MA
    def cal_zma1(self):
        len = 120
        avg_sum = 0
        start_pos = len - 1
        if self.count < len:
            return -1

        for i in range(0, len + 1):
            self.ret.iloc[i, ZMA1_POS] = self.ret["cur"][0]

        for j in range(0, len):
            avg_sum += self.ret["cur"][len - 1 - j]/len
        avr0 = avg_sum
        self.ret.iloc[start_pos, ZMA1_POS] = avr0
        starter = self.ret["cur"][0]
        for i in range(start_pos + 1, self.count):
            avr = avr0 - starter / len + self.ret["cur"][i] / len
            self.ret.iloc[i, ZMA1_POS] = avr
            avr0 = avr
            starter = self.ret["cur"][i - len]
        return 0

    def cal_zma5(self):
        len = 600
        avg_sum = 0
        start_pos = len - 1
        if self.count < len:
            return -1

        for i in range(0, len + 1):
            self.ret.iloc[i, ZMA5_POS] = self.ret["cur"][0]

        for j in range(0, len):
            avg_sum += self.ret["cur"][len - 1 - j]/len
        avr0 = avg_sum
        self.ret.iloc[start_pos, ZMA5_POS] = avr0
        starter = self.ret["cur"][0]
        for i in range(start_pos + 1, self.count):
            avr = avr0 - starter / len + self.ret["cur"][i] / len
            self.ret.iloc[i, ZMA5_POS] = avr
            avr0 = avr
            starter = self.ret["cur"][i - len]
        return 0

    def cal_zmab(self):
        len = 60
        avg_sum = 0
        start_pos = len - 1
        if self.count < len:
            return -1
        for j in range(0, len):
            avg_sum += self.ret["cur"][len - 1 - j]/len
        avr0 = avg_sum
        self.ret.iloc[start_pos, 12] = avr0
        starter = self.ret["cur"][0]
        for i in range(start_pos + 1, self.count):
            avr = avr0 - starter / len + self.ret["cur"][i] / len
            self.ret.iloc[i, 12] = avr
            avr0 = avr
            starter = self.ret["cur"][i - len]
        return 0

    def cal_zma10(self):
        len = 1200
        sum = 0
        start_pos = len - 1
        if self.count < len:
            return -1
        for j in range(0, len):
            sum += self.ret["cur"][len - 1 - j]
        avr0 = sum / len
        self.ret.iloc[start_pos, ZMA10_POS] = avr0
        starter = self.ret["cur"][0]
        for i in range(start_pos + 1, self.count):
            avr = avr0 - starter / len + self.ret["cur"][i] / len
            self.ret.iloc[i, ZMA10_POS] = avr
            avr0 = avr
            starter = self.ret["cur"][i - len]
        return 0

    def cal_zma20(self):
        len = 2400
        sum = 0
        start_pos = len - 1
        if self.count < len:
            return -1
        for j in range(0, len):
            sum += self.ret["cur"][len - 1 - j]
        avr0 = sum / len
        self.ret.iloc[start_pos, ZMA20_POS] = avr0
        starter = self.ret["cur"][0]
        for i in range(start_pos + 1, self.count):
            avr = avr0 - starter/len + self.ret["cur"][i]/len
            self.ret.iloc[i, ZMA20_POS] = avr
            avr0 = avr
            starter = self.ret["cur"][i - len]
        return 0

    def cal_zma1_ratio_simple(self, sample = 240):
        len = 120
        t = sample
        val =0
        c = 120 / sample
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            val = self.ret.iloc[i, ZMA1_POS] - self.ret.iloc[i - t, ZMA1_POS]
            self.ret.iloc[i, ZMA1_RATIO_POS] = val * c

        return 1


    def cal_zma1_ratio_short_simple(self, sample = 120):
        len = 120
        t = sample
        val =0
        c = 120 / sample
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            val = self.ret.iloc[i, ZMA1_POS] - self.ret.iloc[i - t, ZMA1_POS]
            self.ret.iloc[i, ZMA1_RATIO_SHORT_POS] = val * c

        return 1

    def cal_zma5_ratio_simple(self, sample = 120):
        len = 600
        t = sample
        val =0
        c = 120 / sample
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            val = self.ret.iloc[i, ZMA5_POS] - self.ret.iloc[i - t, ZMA5_POS]
            self.ret.iloc[i, ZMA5_RATIO_POS] = val * c

        return 1

    def cal_zma5_ratio_simple_ratio(self, sample = 120):
        len = 600 + 121
        t = sample
        val =0
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            val = self.ret.iloc[i, ZMA5_RATIO_POS] - self.ret.iloc[i - sample, ZMA5_RATIO_POS]
            self.ret.iloc[i, ZMA5_RATIO_RATIO_POS] = val / sample
        return 1


    ## MA Ratio
    def cal_zma10_ratio(self):
        len = 1200
        t = 60
        val =0
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            ret, val = self.optimized_least_square_method(i - t + 1, i, "zma10")
            if ret == -1:
                val = 0
            self.ret.iloc[i, ZMA10_RATIO_POS] = val
        return 1

    def cal_zma10_ratio_simple(self, sample = 120):
        len = 1200
        t = sample
        val =0
        c = 120 / sample
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            val = self.ret.iloc[i, ZMA10_POS] - self.ret.iloc[i - t, ZMA10_POS]
            self.ret.iloc[i, ZMA10_RATIO_POS] = val * c

        return 1

    def cal_zma10_ratio_simple_ratio(self, sample = 360):
        len = 1200 + 121
        t = sample
        val =0
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            val = self.ret.iloc[i, ZMA10_RATIO_POS] - self.ret.iloc[i - sample, ZMA10_RATIO_POS]
            self.ret.iloc[i, ZMA10_RATIO_RATIO_POS] = val / sample
        return 1

    def cal_zma10_ratio_simple_ratio_short(self, sample = 60):
        len = 1200 + 121
        t = sample
        val =0
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            val = self.ret.iloc[i, ZMA10_RATIO_POS] - self.ret.iloc[i - sample, ZMA10_RATIO_POS]
            self.ret.iloc[i, ZMA10_RATIO_RATIO_SHORT_POS] = val / sample
        return 1

    def cal_zma10_ratio_ratio_ratio_simple(self, sample = 120):
        len = 1200 + 121 + 360
        t = sample
        val =0
        c = 120 / sample
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            val = self.ret.iloc[i, ZMA10_RATIO_RATIO_POS] - self.ret.iloc[i - sample, ZMA10_RATIO_RATIO_POS]
            self.ret.iloc[i, ZMA10_RATIO_RATIO_RATIO_POS] = val * c
        return 1




    def cal_delta_zma10(self):
        len = 1200
        if self.count < len + 1:
            return -1
        for i in range(len, self.count):
            delta = self.ret["zma10"][i] - self.ret["zma10"][i-1]
            delta *= 1000
            self.ret.iloc[i, 4] = delta
        return 0

    def cal_delta_zma20(self):
        len = 2400
        if self.count < len + 1:
            return -1
        for i in range(len, self.count):
            delta = self.ret["zma20"][i] - self.ret["zma20"][i-1]
            delta *= 1000
            self.ret.iloc[i, 5] = delta
        return 0

    def cal_delta_zma10_ma60(self):
        len = 60
        sum = 0
        start_pos = 1200 + 2 + len - 1
        if self.count < start_pos:
            return -1
        for j in range(0, 60):
            sum += self.ret["delta_zma10"][start_pos - j]
        avr0 = sum / len
        self.ret.iloc[start_pos, 6] = avr0
        starter = self.ret["delta_zma10"][start_pos - len - 1]
        for i in range(start_pos + 1, self.count):
            avr = avr0 - starter/len + self.ret["delta_zma10"][i]/len

            self.ret.iloc[i, 6] = avr
            avr0 = avr
            starter = self.ret["delta_zma10"][i - len]
        return 0

    def cal_delta_zma20_ma60(self):
        len = 60
        sum = 0
        start_pos = 2400 + 2 + len - 1
        if self.count < start_pos:
            return -1
        for j in range(0, 60):
            sum += self.ret["delta_zma20"][start_pos - j]
        avr0 = sum / len
        self.ret.iloc[start_pos, 7] = avr0
        starter = self.ret["delta_zma20"][start_pos - len - 1]
        for i in range(start_pos + 1, self.count):
            avr = avr0 - starter/len + self.ret["delta_zma20"][i]/len
            self.ret.iloc[i, 7] = avr
            avr0 = avr
            starter = self.ret["delta_zma20"][i - len]
        return 0

    def cal_delta_zma20_ma60_ratio(self):
        len = 2400
        t = 60
        val =0
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            ret, val = self.least_square_method(i - t + 1, i, "delta_zma20_ma60")
            if ret == -1:
                val = 0
            self.ret.iloc[i, 12] = val
        return 1

    def cal_ratio(self):
        len = 2400
        if self.count < len + 1 + 60:
            return -1
        for i in range(len + 60, self.count):
            if self.ret["delta_zma10_ma60"][i] == 0 or self.ret["delta_zma20_ma60"][i] == 0:
                ratio = 0
            else:
                ratio = self.ret["delta_zma10_ma60"][i]/self.ret["delta_zma20_ma60"][i]
            self.ret.iloc[i, 8] = ratio
        return 0

    ## Math
    def least_square_method(self, start, end, column):
        A = 0
        B = 0
        C = 0
        D = 0
        t = end - start +1
        avr_x = 0
        avr_y = 0
        if self.count < start:
            return -1, 0
        for i in range(start, end + 1):
            A += i * self.ret[column][i]
            B += i * i
            avr_x += i / t
            avr_y += self.ret[column][i]/t
        ratio = (A - t * avr_x * avr_y) / (B - t * avr_x * avr_x)
        return 1, ratio

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
        ratio = (A - M * avr_y) / (B - M * avr_x)
        ratio *= -1
        return 1, ratio

    def optimized_least_square_method_r(self, start, end, column):
        A = 0
        B = 0
        C = 0
        D = 0
        xi = 0
        t = end - start + 1
        avr_x = 0
        avr_y = 0
        if self.count < start:
            return -1, 0

        # Calculate avr_x, avr_y
        for i in range(start, end + 1):
            yi = self.ret[column][i]
            avr_x += xi / t
            avr_y += yi / t
            xi += 1

        xi = 0
        for i in range(start, end + 1):
            yi = self.ret[column][i]
            A += (xi - avr_x) * (yi - avr_y)
#            B += (yi - avr_y)
            C += (xi - avr_x) * (xi - avr_x)
            D += (yi - avr_y) * (yi - avr_y)
            xi += 1

        if  D == 0:
            r = 1
        else:
            r = A / ( math.sqrt(C) * math.sqrt(D))

        return 1, r

    def simple_ratio(self, start, end, column):
        if self.count < start:
            return -1, 0
        ratio = (self.ret[column][end] - self.ret[column][start])/(end - start)
        return 1, ratio


    # Calculate all
    def cal_data(self):

        start_time = time.time()
        self.cal_zma10()
        end_time = time.time()
        #print("cal_zma10 finished:" + str( end_time - start_time ))

        start_time = time.time()
        self.cal_zma10_ratio_simple()
        end_time = time.time()
        #print("cal_zma10_ratio_simple finished:" + str( end_time - start_time))

        start_time = time.time()
        self.cal_zma10_ratio_simple_ratio()
        end_time = time.time()
        #print("cal_zma10_ratio_simple_ratio finished:" + str( end_time - start_time))

        start_time = time.time()
        self.cal_zma10_ratio_simple_ratio_short()
        end_time = time.time()
        #print("cal_zma10_ratio_simple_ratio_short finished:" + str( end_time - start_time))

        start_time = time.time()
        self.cal_zma10_ratio_ratio_ratio_simple()
        end_time = time.time()
        #print("cal_zma10_ratio_ratio_ratio_simple finished:" + str( end_time - start_time))







    def mark_trade(self, position, mark):
        self.ret.iloc[position, TRADE_MARK_POS] = mark
        print("BUY:", mark,"\n", self.ret.iloc[position,])

    def detectSignal(self):
        ma10_r_r_r_value = -0.004
        ma10_r_r_value = -0.005


        start = 1200 + 121 + 360 + 120 + 1
        position = start
        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio_ratio_ratio = self.ret["zma10_ratio_ratio_ratio"][position]
            ma10_ratio_ratio = self.ret["zma10_ratio_ratio"][position]
            ma10_ratio = self.ret["zma10_ratio"][position]
            MA10_cur  = self.ret["zma10"][position]
            ma20_ratio = self.ret["ma20_ratio"][position]
            cur = self.ret["cur"][position]

            if ma10_ratio_ratio_ratio <= ma10_r_r_r_value and self.ret["zma10_ratio_ratio_ratio"][position - 1] > ma10_r_r_r_value:
                if ( ma10_ratio_ratio <= 0 or ma10_ratio_ratio + ma10_r_r_r_value /2 <= 0) :
                    if cur < MA10_cur:
                        if ma20_ratio > -2:
                            if ma10_ratio <= 0 or ma10_ratio + ma10_ratio_ratio * 60 <= 0:
                                if ma10_ratio < ma20_ratio:
                                    if ma10_ratio_ratio <= ma10_r_r_value:
                                        if ma20_ratio >= 0:
                                            if ma20_ratio - ma10_ratio < 3:
                                                self.mark_trade(position, 1)
                                            else:
                                                self.mark_trade(position, 3)
                                        else:
                                            if ma10_ratio >= -3:
                                                self.mark_trade(position, 1)
                                            else:
                                                self.mark_trade(position, 3)
                        else:
                            if ma10_ratio < 0:
                                self.mark_trade(position, 1)
            position += 1
        return 1

    def detectSignal2(self):
        ma10_r_r_r_value = -0.004
        ma20_many_head = -2
        ma10_r_r_value = -0.005

        start = 1200 + 121 + 360 + 120 + 1
        position = start


        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio_ratio_ratio = self.ret["zma10_ratio_ratio_ratio"][position]
            ma10_ratio_ratio = self.ret["zma10_ratio_ratio"][position]
            ma10_ratio_ratio_short = self.ret["zma10_ratio_ratio_short"][position]
            ma10_ratio = self.ret["zma10_ratio"][position]
            MA10_cur = self.ret["zma10"][position]
            MA20_cur = self.ret["ma20"][position]
            ma20_ratio = self.ret["ma20_ratio"][position]
            cur = self.ret["cur"][position]
            if position == start:
                if ma10_ratio < 0:
                    trend_down = 1
                else:
                    trend_down = 0

            ma10_ratio_threshold = 0
            #if ma10_ratio < ma10_ratio_threshold and self.ret["zma10_ratio"][position - 1] >= ma10_ratio_threshold:
                #ma10_down_trend = 1

            #if ma10_ratio >= ma10_ratio_threshold and self.ret["zma10_ratio"][position - 1] < ma10_ratio_threshold:
                #ma10_down_trend = 0

            if ma10_ratio < 0 and self.ret["zma10_ratio"][position - 1] >= 0:
                ma10r_down_cross_zero = 1
            else:
                ma10r_down_cross_zero = 0

            if ma10_ratio >= 0 and self.ret["zma10_ratio"][position - 1] < 0:
                ma10r_up_cross_zero = 1
            else:
                ma10r_up_cross_zero = 0

            if ma10_ratio_ratio < 0 and self.ret["zma10_ratio_ratio"][position - 1] >= 0:
                ma10rr_down_cross_zero = 1
            else:
                ma10rr_down_cross_zero = 0

            if ma10_ratio_ratio >= 0 and self.ret["zma10_ratio_ratio"][position - 1] < 0:
                ma10rr_up_cross_zero = 1
            else:
                ma10rr_up_cross_zero = 0


            if ma10rr_down_cross_zero == 1 and ma10_ratio < 0:
                trend_down = 1
            if ma10r_down_cross_zero == 1:
                trend_down = 1

            if ma10rr_up_cross_zero == 1:
                trend_down = 0



            good_hill = 0
            zma10_rrr_short_cross_float = -0.001
            if ma10_ratio_ratio_short >= ma10_ratio_ratio + zma10_rrr_short_cross_float and self.ret["zma10_ratio_ratio_short"][position - 1] < self.ret["zma10_ratio_ratio"][position - 1] + zma10_rrr_short_cross_float:
                ma10_rr_up = 1
                if trend_down == 1:
                    ma10_r_r_up_ok = 1
                    up_pos = position
                    #print("ma10_r_r_up_ok")
                else:
                    ma10_r_r_up_ok = 0
            if ma10_ratio_ratio_short < ma10_ratio_ratio - zma10_rrr_short_cross_float and self.ret["zma10_ratio_ratio_short"][position - 1] >= self.ret["zma10_ratio_ratio"][position - 1] - zma10_rrr_short_cross_float:
                ma10_rr_down = 1
                if trend_down == 1:
                    ma10_r_r_down_ok = 1
                    #print("ma10_r_r_down_ok")
                    try:
                        if ma10_r_r_up_ok == 1 and ma10_r_r_down_ok == 1:
                            if position - up_pos <= 240:
                                good_hill = 1
                                trend_down = 0
                            else:
                                print("hill time out", self.ret["time"][position],"ma10-r-r:", ma10_ratio_ratio, " ma10_ratio:", ma10_ratio, " ma20_ratio", ma20_ratio, " duration:",str((position - up_pos)/2)," seconds")
                    except:
                        print("")

                ma10_rr_up = 0
                ma10_rr_down = 0
                ma10_r_r_up_ok = 0
                ma10_r_r_down_ok = 0

            if good_hill == 1:
                if ma10_ratio <= -1 and ma20_ratio < -1:
                    if ma10_ratio_ratio <= -0.004 and \
                             ((ma10_ratio_ratio_ratio - self.ret["zma10_ratio_ratio_ratio"][position - 20]) < 0 or ma10_ratio_ratio_ratio < 0):
                        self.mark_trade(position, 555)
                        print(" duration:",str((position - up_pos)/2)," seconds")
                        trend_down = 0


            position += 1
        return 1

    def detect_turn2bear(self):
        ma10_r_r_r_value = -0.004
        ma20_many_head = -2
        ma10_r_r_value = -0.005
        ma10_r_r_value_short = -0.01
        ma10_r_r_small_value = -0.001
        start = 1200 + 121 + 360 + 120 + 1
        position = start


        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio_ratio_ratio = self.ret["zma10_ratio_ratio_ratio"][position]
            ma10_ratio_ratio = self.ret["zma10_ratio_ratio"][position]
            ma10_ratio_ratio_short = self.ret["zma10_ratio_ratio_short"][position]
            ma10_ratio = self.ret["zma10_ratio"][position]
            MA10_cur = self.ret["zma10"][position]
            MA20_cur = self.ret["ma20"][position]
            ma20_ratio = self.ret["ma20_ratio"][position]
            cur = self.ret["cur"][position]

            ## when ma10-r-r-r drops to -0.004
            if ma10_ratio_ratio_ratio <= ma10_r_r_r_value and self.ret["zma10_ratio_ratio_ratio"][position - 1] > ma10_r_r_r_value:
                ### 111 turning point drops fast
                ### a. ma20_r >= -2
                if ma20_ratio >= ma20_many_head and \
                        (ma10_ratio <= 0 or ma10_ratio + ma10_ratio_ratio * 60 <= 0) and ma10_ratio >= -3 and \
                                ma10_ratio < ma20_ratio :
                    if (ma10_ratio_ratio <= ma10_r_r_value) and \
                                cur < MA10_cur and cur < MA20_cur:
                        gap = cur - self.ret["cur"][position - 120]
                        if  gap > -10 and gap < -5:
                            self.mark_trade(position, 1114)
                            x=1
                        if gap <= -10:
                            self.mark_trade(position, 1118)
                            x=1
                        #print("gap:", cur - self.ret["cur"][position - 120])

                ### 222 turning point drops slowly
                if ma20_ratio >= ma20_many_head and ma20_ratio < 0.5 and \
                        ma10_ratio < -1 and ma10_ratio >= -3 and \
                                ma10_ratio < ma20_ratio:
                    if ma10_ratio_ratio <= ma10_r_r_small_value and ma10_ratio_ratio > ma10_r_r_value and \
                                    cur < MA10_cur and (MA10_cur + ma10_ratio * 2) < MA20_cur:
                        gap = cur - self.ret["cur"][position - 120]
                        ratio = gap/ma10_ratio
                        if ratio <= 8 and gap < 0:
                            self.mark_trade(position, 222)
                            #print("gap:", cur - self.ret["cur"][position - 120])
                            x = 1

            position += 1
        return 1

    def mark_base(self, plots):
        cur_tl = self.ret["cur"]
        zma10_tl = self.ret["zma10"]
        ma20_tl = self.ret["ma20"]
        ma50_tl = self.ret["ma50"]
        zma1_r_tl = self.ret["zma1_ratio"]
        zma1_r_s_tl = self.ret["zma1_ratio_short"]
        # zma1_r_r_tl = self.ret["zma1_ratio_ratio"]
        zma5_r_tl = self.ret["zma5_ratio"]
        zma5_r_r_tl = self.ret["zma5_ratio_ratio"]
        zma10_r_tl = self.ret["zma10_ratio"]
        ma20_r_tl = self.ret["ma20_ratio"]
        zma10_r_r_tl = self.ret["zma10_ratio_ratio"]
        zma10_r_r_s_tl = self.ret["zma10_ratio_ratio_short"]
        zma10_r_r_r_tl = self.ret["zma10_ratio_ratio_ratio"]
        bull_decrease = self.ret["bull_decrease"]
        zma5_tl = self.ret["zma5"]
        zma1_tl = self.ret["zma1"]
        zma1_zma10_gap_tl = self.ret["zma1_zma10_gap"]
        zma1_zma10_gap_scope_tl = self.ret["zma1_zma10_gap_scope"]

        plots.prepare_plot(cur_tl, 1)
        plots.prepare_plot(zma1_tl, 1)
        plots.prepare_plot(zma5_tl, 1)
        plots.prepare_plot(zma10_tl, 1)
        plots.prepare_plot(ma20_tl, 1)
        plots.prepare_plot(ma50_tl, 1)


        plots.prepare_plot(zma1_r_tl, 2)
        plots.prepare_plot(zma1_r_s_tl, 2)
        plots.prepare_plot(zma5_r_tl, 2)
        #plots.prepare_plot(zma10_r_tl, 2)
        #plots.prepare_plot(ma20_r_tl, 2)

        plots.prepare_plot(zma5_r_r_tl, 3)
        plots.prepare_plot(zma10_r_r_tl, 3)
        #plots.prepare_plot(zma10_r_r_s_tl, 3)

        #plots.prepare_plot(zma1_zma10_gap_scope_tl, 3)

        #plots.prepare_plot(zma1_r_r_tl, 4)
        #plots.prepare_plot(zma1_zma10_gap_tl, 4)
        #plots.prepare_plot(zma10_r_r_r_tl, 4)


        #plots.prepare_plot(bull_decrease,5 )

    def cal_bull_decrease(self):
        print("BULL DECREASE CAL")
        start = 120
        position = start

        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio = self.ret["zma10_ratio"][position]
            cur = self.ret["cur"][position]

            if ma10_ratio >= 0 and self.ret["zma10_ratio"][position - 1] < 0:
                max = cur
                ma10_up = 1

            if ma10_ratio < 0 and self.ret["zma10_ratio"][position - 1] >= 0:
                ma10_up = 0

            try:
                if ma10_up == 1:

                    if cur < max:
                        gap = max - cur
                    else:
                        max = cur
                        gap = 0
                else:
                    gap = -1
            except:
                gap = -1

            self.ret.iloc[position, 11] = gap

            position += 1

    def cal_bear_increase(self):
        print("Bear INCREASE CAL")
        start = 120
        position = start

        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio = self.ret["zma10_ratio"][position]
            cur = self.ret["cur"][position]
            cur_b = self.ret["zmab"][position]
            if position == start:
                if ma10_ratio < 0:
                    min = cur
                    ma10_up = 1

            if ma10_ratio < 0 and self.ret["zma10_ratio"][position - 1] >= 0:
                min = cur
                ma10_up = 1

            if ma10_ratio >= 0 and self.ret["zma10_ratio"][position - 1] < 0:
                ma10_up = 0

            try:
                if ma10_up == 1:

                    if cur_b > min:
                        gap = cur_b - min
                    else:
                        min = cur_b
                        gap = 0
                else:
                    gap = -1
            except:
                gap = -1

            self.ret.iloc[position, 11] = gap

            position += 1


    def mark_bear_zma1_zma10_cross(self, plots):
        ma10_r_r_r_value = -0.002
        ma20_many_head = -2
        ma10_r_r_value = -0.005
        ma10_r_r_value_short = -0.01
        ma10_r_r_small_value = -0.001
        #start = 1200 + 121 + 360 + 120 + 1
        start = 120
        position = start

        count = 0
        state = 0
        assign_froze = 0
        wait_time_froze = 0
        once_high = 0
        assign_froze = 0
        zma1_cross_number = 0
        wait_point = 0
        wait_ma20_pen = 0
        ma10_penetration = 0
        ma20_penetration = 0
        wait_vally = 0
        up_trend = 0
        wait_time = 2400
        marked = 0
        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio_ratio_ratio = self.ret["zma10_ratio_ratio_ratio"][position]
            ma10_ratio_ratio = self.ret["zma10_ratio_ratio"][position]
            ma10_ratio_ratio_short = self.ret["zma10_ratio_ratio_short"][position]
            ma10_ratio = self.ret["zma10_ratio"][position]
            ma5_ratio = self.ret["zma5_ratio"][position]
            ma5_ratio_ratio = self.ret["zma5_ratio_ratio"][position]
            ma1_ratio = self.ret["zma1_ratio"][position]
            ma1_s_ratio = self.ret["zma1_ratio_short"][position]
            zma1 =  self.ret["zma1"][position]
            MA5_cur = self.ret["zma5"][position]
            MA10_cur = self.ret["zma10"][position]
            MA20_cur = self.ret["ma20"][position]
            MA50_cur = self.ret["ma50"][position]
            ma20_ratio = self.ret["ma20_ratio"][position]
            cur = self.ret["cur"][position]
            basic_condition = 0
            started = 0

            if  ( zma1 > MA20_cur and self.ret["zma1"][position - 1] <= self.ret["ma20"][position - 1] ) or \
                ( zma1 > MA50_cur and self.ret["zma1"][position - 1] <= self.ret["ma50"][position - 1])    :

                plots.add_annotate(position, cur, 1,
                              "P\n"
                               , 50)
                wait_vally = wait_time
                marked = 0

            if MA5_cur < MA10_cur and self.ret["zma5"][position - 1] >= self.ret["zma10"][position - 1]:
                plots.add_annotate(position, cur, 1,
                                       "sell"
                                       , 50)


            if wait_vally > 0 and wait_vally < wait_time -240 and up_trend < 20:
                #if zma1 < MA10_cur:
                    #wait_vally = 0
                    #up_trend = 0

                ratio = ma1_ratio/(wait_time-wait_vally)
                self.ret.iloc[position, ZMA1_RATIO_RATIO_POS] = ratio



                if ma1_ratio > 4 and (ma1_ratio/(wait_time-wait_vally) ) >= 0.005 and \
                        ma1_s_ratio > 0 and ma10_ratio > 1.5 and \
                        ma5_ratio_ratio > 0:
                    x=1
                    #plots.add_annotate(position, cur, 1,
                                       #"ok"
                                       #, 100)


                if ma1_s_ratio > ma1_ratio and self.ret["zma1_ratio_short"][position - 1] <= self.ret["zma1_ratio"][position - 1] and \
                        cur > MA10_cur:
                    basic_condition = 1
                    plots.add_annotate(position, cur, 1,
                                       str(basic_condition)
                                       , 50)


                if ma1_s_ratio > ma5_ratio and self.ret["zma1_ratio_short"][position - 1] <= self.ret["zma5_ratio"][position - 1] and \
                    cur > MA10_cur:
                    basic_condition = 2
                    plots.add_annotate(position, cur, 1,
                                       str(basic_condition)
                                       , 50)

                basic_condition = 99

                if (basic_condition != 0 or 1) and marked == 0:
                    if count % 2 == 0:
                        show_len = -250
                    else:
                        show_len = -450
                    #up_trend += 1
                    if ma10_ratio >= 1.5 and \
                            ( (ma1_s_ratio >= ma20_ratio and MA20_cur < MA10_cur) or \
                              (ma1_s_ratio >= ma10_ratio and MA20_cur >= MA10_cur) ) and \
                            (ma1_s_ratio >= ma20_ratio or ma1_s_ratio >= ma10_ratio) and \
                            (ma1_ratio >= ma20_ratio or ma1_ratio >= ma10_ratio) and  \
                             ma1_ratio > 0 and \
                            ma5_ratio > 3 and \
                             ma5_ratio_ratio * 1000 >= 1:
                        #plots.add_annotate(position, cur, 1,
                        #"BULL!!!\n" + str(round(ma1_ratio,3)) + "\n" + str(round(ma5_ratio,3)) + "\n" + str(round(ma10_ratio,3)) + "\n" + str(ma20_ratio) + "\n" +
                         #str(round(ma5_ratio_ratio*1000,2)) + "\n"+ str(round(ma10_ratio_ratio*1000,2)) + "\n" +
                         #str((wait_time-wait_vally)/2) + "s" + "\n" + str(basic_condition)
                        # , show_len)

                        plots.add_annotate(position, cur, 1,
                            "BULL!!!"
                             , show_len)

                        print("BULL!!!" + str(round(ma1_ratio, 3)) + " " + str(round(ma5_ratio, 3)) + " " + str(round(ma10_ratio, 3)) + " " + str(ma20_ratio) + " " +
                              str(round(ma5_ratio_ratio * 1000, 2)) + " " + str(round(ma10_ratio_ratio * 1000, 2)) + " " +
                              str((wait_time-wait_vally)/2) + "s" + " " + str(basic_condition))
                        up_trend = 20
                        marked = 1

                    if up_trend == 20:
                        wait_vally = 0
                        up_trend = 0

                    count += 1

            if wait_vally > 0:
                wait_vally -= 1

            position += 1

        return count


    def mark_bear_rrcross_pure(self, plots):
        ma10_r_r_r_value = -0.002
        ma20_many_head = -2
        ma10_r_r_value = -0.005
        ma10_r_r_value_short = -0.01
        ma10_r_r_small_value = -0.001
        #start = 1200 + 121 + 360 + 120 + 1
        start = 120
        position = start

        count = 0
        state = 0
        assign_froze = 0
        wait_time_froze = 0
        once_high = 0
        assign_froze = 0
        zma1_cross_number = 0
        wait_point = 0
        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio_ratio_ratio = self.ret["zma10_ratio_ratio_ratio"][position]
            ma10_ratio_ratio = self.ret["zma10_ratio_ratio"][position]
            ma10_ratio_ratio_short = self.ret["zma10_ratio_ratio_short"][position]
            ma10_ratio = self.ret["zma10_ratio"][position]
            ma1_ratio = self.ret["zma1_ratio"][position]
            ma1_s_ratio = self.ret["zma1_ratio_short"][position]
            MA10_cur = self.ret["zma10"][position]
            MA20_cur = self.ret["ma20"][position]
            ma20_ratio = self.ret["ma20_ratio"][position]
            cur = self.ret["cur"][position]


            if ma10_ratio > 0 and self.ret["zma10_ratio"][position - 1] <= 0:
                zma1_cross_number = 0

            if ma10_ratio <= 0 and self.ret["zma10_ratio"][position - 1] > 0:
                zma1_cross_number = 0

            if ma1_ratio < ma20_ratio and self.ret["zma1_ratio"][position - 1] >= self.ret["ma20_ratio"][position - 1]:
                zma1_cross_number += 1

            if ma1_ratio < ma20_ratio and self.ret["zma1_ratio"][position - 1] >= self.ret["ma20_ratio"][position - 1]:
                if ma1_s_ratio < ma1_ratio and \
                    assign_froze == 0:
                    if count % 2 == 0:
                        show_len = -250
                    else:
                        show_len = -450
                    plots.add_annotate(position, cur, 1,
                                       str(cur) + "\n" +
                                       str(round(ma1_s_ratio, 2)) + "\n" + str(round(ma1_ratio, 5)) + "\n" +
                                       str(ma10_ratio) + "\n" + str(ma20_ratio) + "\n" + str(zma1_cross_number)
                                       , show_len)
                    # plots.add_annotate(position, cur, 1,
                    # str(cur) + "\n" + str(MA10_cur) + "\n" +  str(MA20_cur) + "\n" +
                    # str(ma10_ratio) + "\n"+ str(ma20_ratio) + "\n" +
                    # str(round(ma10_ratio_ratio, 5)) + "\n"+ str(round(ma10_ratio_ratio_ratio, 5)) + "\n" + str(round(ma10_ratio_ratio_short, 5)), show_len)
                    print(str(cur) + " " + str(MA10_cur) + " " + str(MA20_cur) + " " +
                          str(ma10_ratio) + " " + str(ma20_ratio) + " " +
                          str(round(ma10_ratio_ratio, 5)) + " " + str(round(ma10_ratio_ratio_ratio, 5)) + " " + str(
                        round(ma10_ratio_ratio_short, 5)))
                    assign_froze = 120
                    wait_point = 360
                    count += 1


            if wait_point > 0:
                back_units = 60
                if ma1_s_ratio < ma1_ratio and ma1_ratio < ma10_ratio and \
                    self.ret["zma1_ratio_short"][position - back_units] < self.ret["zma1_ratio"][position - back_units] and \
                    self.ret["zma1_ratio"][position - back_units] < self.ret["zma10_ratio"][position - back_units] and \
                        ma1_s_ratio < self.ret["zma1_ratio_short"][position - back_units] and \
                        ma1_ratio < self.ret["zma1_ratio"][position - back_units] and \
                        ma10_ratio < self.ret["zma10_ratio"][position - back_units] :
                    #plots.add_annotate(position, cur, 1,
                    #                   "Look!!!"
                    #                   , 50)
                    wait_point = 0

           #### End this round
            if assign_froze > 0:
                assign_froze -= 1
            if wait_point > 0:
                wait_point -= 1

            position += 1

        return count

    def mark_bear_rrcross(self, plots):
        ma10_r_r_r_value = -0.002
        ma20_many_head = -2
        ma10_r_r_value = -0.005
        ma10_r_r_value_short = -0.01
        ma10_r_r_small_value = -0.001
        #start = 1200 + 121 + 360 + 120 + 1
        start = 120
        position = start

        count = 0
        state = 0
        assign_froze = 0
        wait_time_froze = 0
        once_high = 0
        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio_ratio_ratio = self.ret["zma10_ratio_ratio_ratio"][position]
            ma10_ratio_ratio = self.ret["zma10_ratio_ratio"][position]
            ma10_ratio_ratio_short = self.ret["zma10_ratio_ratio_short"][position]
            ma10_ratio = self.ret["zma10_ratio"][position]
            MA10_cur = self.ret["zma10"][position]
            MA20_cur = self.ret["ma20"][position]
            ma20_ratio = self.ret["ma20_ratio"][position]
            cur = self.ret["cur"][position]

            if ma10_ratio + 20 * ma10_ratio_ratio_short < ma20_ratio and self.ret["zma10_ratio"][position-1] >= self.ret["ma20_ratio"][position-1] and \
                abs(MA10_cur - MA20_cur) < 15 and \
                assign_froze == 0:
                     #ma10_ratio_ratio < 0 and \
                     #ma20_ratio - self.ret["ma20_ratio"][position - 120] < 0:
                #gap_cur = cur - self.ret["cur"][position - 360]
                #gap_ma10 = cur - MA10_cur
                #if gap_cur <= -10 and gap_ma10 <= -10 :
                plots.add_annotate(position, cur, 1,
                                   str(self.ret["time"][position]) + "Cross \n" + "cur:" + str(cur) + "\n", -200)
                state = 1
                wait_time = 600
                assign_froze = 60
                wait_time_froze = 120
                print(str(self.ret["time"][position]), "assign state")

            if state == 1 and wait_time_froze == 0:
                if ma10_ratio_ratio_short >= -0.001:
                    once_high = 1

                if wait_time > 0:
                    if ma10_ratio_ratio_short <= -0.000 and self.ret["zma10_ratio_ratio_short"][position - 1] > -0.000 and once_high == 1:
                        if ma20_ratio < -1 and ma10_ratio <= -2 and \
                                cur < MA10_cur and cur < MA20_cur:
                            plots.add_annotate(position, cur, 1,str(self.ret["time"][position]) + "aaaaaa\n" + "cur:" + str(cur) + "\n" , -200)
                            count += 1
                            print(str(self.ret["time"][position]), "reset state due to good")
                        print(str(self.ret["time"][position]), "reset state due to bad")
                        state = 0
                        wait_time = 0
                        once_high = 0
                    wait_time -= 1
                else:
                    state = 0
                    once_high = 0


            if assign_froze > 0:
                assign_froze -= 1
            if wait_time_froze > 0:
                wait_time_froze -= 1
            position += 1
        return count

    def mark_undefine(self, plots):
        ma10_r_r_r_value = -0.002
        ma20_many_head = -2
        ma10_r_r_value = -0.005
        ma10_r_r_value_short = -0.01
        ma10_r_r_small_value = -0.001
        #start = 1200 + 121 + 360 + 120 + 1
        start = 120
        position = start
        print("start ",str(start))

        vally_count = 0
        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio_ratio_ratio = self.ret["zma10_ratio_ratio_ratio"][position]
            ma10_ratio_ratio = self.ret["zma10_ratio_ratio"][position]
            ma10_ratio_ratio_short = self.ret["zma10_ratio_ratio_short"][position]
            ma10_ratio = self.ret["zma10_ratio"][position]
            MA10_cur = self.ret["zma10"][position]
            MA20_cur = self.ret["ma20"][position]
            ma20_ratio = self.ret["ma20_ratio"][position]
            cur = self.ret["cur"][position]

            if ma10_ratio < ma20_ratio and self.ret["zma10_ratio"][position-1] >= self.ret["ma20_ratio"][position-1] and \
                     ma10_ratio_ratio_short <= -0.01 and \
                     ma10_ratio <= 0 and \
                     ma10_ratio_ratio < 0 and \
                     ma20_ratio - self.ret["ma20_ratio"][position - 120] < 0:
                gap = cur - self.ret["cur"][position - 360]
                plots.add_annotate(position, cur, 1,
                                   str(self.ret["time"][position]) + "\n" + "cur:" + str(cur) + "\n" + str(gap) + "\n" + str(cur - MA10_cur), -200)
            position += 1
        return 1

    def mark_bull_continue(self, plots):
        ma10_r_r_r_value = -0.002
        ma20_many_head = -2
        ma10_r_r_value = -0.005
        ma10_r_r_value_short = -0.01
        ma10_r_r_small_value = -0.001
        #start = 1200 + 121 + 360 + 120 + 1
        start = 120
        position = start
        print("start ",str(start))

        vally_count = 0
        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio_ratio_ratio = self.ret["zma10_ratio_ratio_ratio"][position]
            ma10_ratio_ratio = self.ret["zma10_ratio_ratio"][position]
            ma10_ratio_ratio_short = self.ret["zma10_ratio_ratio_short"][position]
            ma10_ratio = self.ret["zma10_ratio"][position]
            MA10_cur = self.ret["zma10"][position]
            MA20_cur = self.ret["ma20"][position]
            ma20_ratio = self.ret["ma20_ratio"][position]
            cur = self.ret["cur"][position]


            if ma10_ratio >= 0 and self.ret["zma10_ratio"][position - 1] < 0:
                vally_count = 0
                back_static = 0
                max = cur
                ma10_up = 1
                ma20_up_pos = position
                ma20_up_val = ma20_ratio

            if ma10_ratio < 0 and self.ret["zma10_ratio"][position - 1] >= 0:
                back_static = 0
                ma10_up = 0

            if position == start:
                if ma20_ratio >= 0:
                    ma20_up_pos = position
                    ma20_up_val = ma20_ratio

            #if ma20_ratio >= 0 and self.ret["ma20_ratio"][position - 1] < 0:
                #ma20_up_pos = position
                #ma20_up_val = ma20_ratio


            ## when ma10-r-r-r drops to -0.004
            if ma10_ratio_ratio_ratio * 1000 <= ma10_r_r_r_value * 1000 and \
                    self.ret["zma10_ratio_ratio_ratio"][position - 1] * 1000 > ma10_r_r_r_value * 1000 :
                ### 111 turning point drops fast
                ### a. ma20_r >= -2
                vally_count += 1
                print(self.ret.iloc[position,])
                try:
                    ma20_ratio_ratio = ((ma20_ratio - ma20_up_val)/(position - ma20_up_pos)) * 120
                except:
                    ma20_ratio_ratio = 0

                MA_Condition = 0
                if cur > MA10_cur and MA10_cur > MA20_cur and MA10_cur - MA20_cur > 2 * ma10_ratio:
                    MA_Condition = 1
                else:
                    MA_Condition = 0
                    print("MA_Condition Fail: cur:", cur, " MA10:", MA10_cur ," MA20:", MA20_cur)

                if ma20_ratio > 1 and ma10_ratio > ma20_ratio:
                    MA_R_Condition = 1
                else:
                    MA_R_Condition = 0
                    print("MA_Condition Fail: MA10_R", ma10_ratio, " MA20_R", ma20_ratio)
                ratio = (cur - MA10_cur) / ma10_ratio
                ratio2 = ma10_ratio / ma20_ratio
                if MA_Condition == 1 and MA_R_Condition == 1:
                    show = 0
                    if ma20_ratio > 1:
                        if vally_count <= 3:
                            show = 1

                    if show == 1:
                        plots.add_annotate(position, cur, 1, str(self.ret["time"][position]) + "\n"+ "cur:" + str(cur) + "\n" +str(ratio) + "\n" +str(ratio2) + "\n" + str(vally_count)+ "\n" + str(ma20_ratio_ratio), -200 )


            position += 1
        return 1


    def mark_rr_cross(self, plots):
        ma10_r_r_r_value = -0.002
        ma20_many_head = -2
        ma10_r_r_value = -0.005
        ma10_r_r_value_short = -0.01
        ma10_r_r_small_value = -0.001
        #start = 1200 + 121 + 360 + 120 + 1
        start = 120
        position = start
        print("start ",str(start))

        vally_count = 0
        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio_ratio_ratio = self.ret["zma10_ratio_ratio_ratio"][position]
            ma10_ratio_ratio = self.ret["zma10_ratio_ratio"][position]
            ma10_ratio_ratio_short = self.ret["zma10_ratio_ratio_short"][position]
            ma10_ratio = self.ret["zma10_ratio"][position]
            MA10_cur = self.ret["zma10"][position]
            MA20_cur = self.ret["ma20"][position]
            ma20_ratio = self.ret["ma20_ratio"][position]
            cur = self.ret["cur"][position]

            if ma10_ratio > ma20_ratio and self.ret["zma10_ratio"][position - 1] <= self.ret["ma20_ratio"][position - 1] and \
                    ma10_ratio_ratio_short >= 0.01 and \
                    ma10_ratio >= 0 and \
                    ma10_ratio_ratio < 0:
                    plots.add_annotate(position, cur, 1, str(self.ret["time"][position]) + "\n" + "cur:" + str(cur), -200)
            position += 1
        return 1

    def mark_bear_about_die(self, plots):
        ma10_r_r_r_value = -0.004
        ma20_many_head = -2
        ma10_r_r_value = -0.005
        ma10_r_r_value_short = -0.01
        ma10_r_r_small_value = -0.001
        start = 1200 + 121 + 360 + 120 + 1
        position = start


        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio_ratio_ratio = self.ret["zma10_ratio_ratio_ratio"][position]
            ma10_ratio_ratio = self.ret["zma10_ratio_ratio"][position]
            ma10_ratio_ratio_short = self.ret["zma10_ratio_ratio_short"][position]
            ma10_ratio = self.ret["zma10_ratio"][position]
            MA10_cur = self.ret["zma10"][position]
            MA20_cur = self.ret["ma20"][position]
            ma20_ratio = self.ret["ma20_ratio"][position]
            cur = self.ret["cur"][position]

            if ma20_ratio <= -1.5:
                if ma10_ratio < ma20_ratio and self.ret["zma10_ratio"][position-1] >= self.ret["ma20_ratio"][position-1] and self.ret["zma10_ratio"][position-120] >= self.ret["ma20_ratio"][position-120] and \
                        MA20_cur - MA10_cur > -1 * ma10_ratio and \
                        ma10_ratio_ratio < -0.001 and \
                        ma10_ratio_ratio_ratio < 0:
                    plots.add_annotate(position, cur, 1, "444 " + str(cur) + "\n" + str(ma10_ratio) + "/" + str(
                        ma20_ratio) + "\nma10_rr" + str(ma10_ratio_ratio) + "\nma10_rrr" + str(ma10_ratio_ratio_ratio))
            position += 1
        return 1


    def mark_bear_start(self, plots):
        ma10_r_r_r_value = -0.004
        ma20_many_head = -2
        ma10_r_r_value = -0.005
        ma10_r_r_value_short = -0.01
        ma10_r_r_small_value = 0
        start = 121
        position = start


        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio_ratio_ratio = self.ret["zma10_ratio_ratio_ratio"][position]
            ma10_ratio_ratio = self.ret["zma10_ratio_ratio"][position]
            ma10_ratio_ratio_short = self.ret["zma10_ratio_ratio_short"][position]
            ma10_ratio = self.ret["zma10_ratio"][position]
            MA10_cur = self.ret["zma10"][position]
            MA20_cur = self.ret["ma20"][position]
            ma20_ratio = self.ret["ma20_ratio"][position]
            cur = self.ret["cur"][position]

            ## when ma10-r-r-r drops to -0.004
            if ma10_ratio_ratio_ratio <= ma10_r_r_r_value and self.ret["zma10_ratio_ratio_ratio"][position - 1] > ma10_r_r_r_value:
                ### 111 turning point drops fast
                ### a. ma20_r >= -2
                if ma20_ratio >= ma20_many_head and \
                        (ma10_ratio <= 0 or ma10_ratio + ma10_ratio_ratio * 60 <= 0) and ma10_ratio >= -3 and \
                                ma10_ratio < ma20_ratio :
                    if (ma10_ratio_ratio <= ma10_r_r_value) and \
                                cur < MA10_cur and (MA10_cur + ma10_ratio * 2) < MA20_cur:
                        gap = cur - self.ret["cur"][position - 120]
                        ratio = gap / ma10_ratio
                        if  gap > -10 and gap < -5:
                            print("gap:", cur - self.ret["cur"][position - 120], "ratio", ratio)
                            plots.add_annotate(position, cur, 1, "1114\n" + str(cur) + "\n" + str(ma10_ratio) + "/" + str(ma20_ratio) + "\nma10_rr" + str(ma10_ratio_ratio) + "\nma10_rrr" + str(ma10_ratio_ratio_ratio))
                            self.mark_trade(position, 1114)
                            x=1
                        if gap <= -10:
                            print("gap:", cur - self.ret["cur"][position - 120], "ratio", ratio)
                            plots.add_annotate(position, cur, 1, "1118 " + str(cur) + "\n" + str(ma10_ratio) + "/" + str(ma20_ratio) + "\nma10_rr" + str(ma10_ratio_ratio) + "\nma10_rrr" + str(ma10_ratio_ratio_ratio))
                            self.mark_trade(position, 1118)
                            x=1
                        #print("gap:", cur - self.ret["cur"][position - 120])

                ### 222 turning point drops slowly
                if ma20_ratio >= ma20_many_head and ma20_ratio < 0.5 and \
                        ma10_ratio + ma10_ratio_ratio * 120 < -1 and ma10_ratio >= -3 and \
                                ma10_ratio < ma20_ratio:
                    if ma10_ratio_ratio <= ma10_r_r_small_value and ma10_ratio_ratio > ma10_r_r_value and \
                                    cur < MA10_cur and (MA10_cur + ma10_ratio * 2) < MA20_cur:
                        gap = cur - self.ret["cur"][position - 120]
                        ratio = gap/ma10_ratio
                        #print("gap:", cur - self.ret["cur"][position - 120], "ratio", ratio, " ", self.ret["time"][position])
                        if ratio < 8 and gap < 0:
                            print("gap:", cur - self.ret["cur"][position - 120], "ratio", ratio)
                            plots.add_annotate(position, cur, 1, "222" + str(cur) + "\n" + str(ma10_ratio) + "/" + str(ma20_ratio) + "\nma10_rr" + str(ma10_ratio_ratio) + "\nma10_rrr" + str(ma10_ratio_ratio_ratio))
                            self.mark_trade(position, 222)
                            #print("gap:", cur - self.ret["cur"][position - 120])
                            x = 1

                if ma20_ratio >= ma20_many_head and ma20_ratio < 0.5 and \
                        ma10_ratio < -1 and ma10_ratio >= -3:
                    if ma10_ratio_ratio <= ma10_r_r_small_value and ma10_ratio_ratio > ma10_r_r_value and \
                                    cur < MA10_cur and (MA10_cur + ma10_ratio * 2) < MA20_cur:
                        gap = cur - self.ret["cur"][position - 120]
                        ratio = gap/ma10_ratio

                        if ratio < 8 and gap < 0:
                            print("gap:", cur - self.ret["cur"][position - 120], "ratio", ratio)
                            plots.add_annotate(position, cur, 1, "222" + str(cur) + "\n" + str(ma10_ratio) + "/" + str(ma20_ratio) + "\nma10_rr" + str(ma10_ratio_ratio) + "\nma10_rrr" + str(ma10_ratio_ratio_ratio))
                            self.mark_trade(position, 22244)
                            #print("gap:", cur - self.ret["cur"][position - 120])
                            x = 1
            position += 1
        return 1

    def mark_bear_continue(self, plots):
        ma10_r_r_r_value = -0.001
        ma20_many_head = -2
        ma10_r_r_value = -0.005

        start = 1200 + 121 + 360 + 120 + 1
        position = start

        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio_ratio_ratio = self.ret["zma10_ratio_ratio_ratio"][position]
            ma10_ratio_ratio = self.ret["zma10_ratio_ratio"][position]
            ma10_ratio_ratio_short = self.ret["zma10_ratio_ratio_short"][position]
            ma10_ratio = self.ret["zma10_ratio"][position]
            MA10_cur = self.ret["zma10"][position]
            MA20_cur = self.ret["ma20"][position]
            ma20_ratio = self.ret["ma20_ratio"][position]
            cur = self.ret["cur"][position]
            if position == start:
                if ma10_ratio < 0:
                    trend_down = 1
                else:
                    trend_down = 0

            ma10_ratio_threshold = 0
            # if ma10_ratio < ma10_ratio_threshold and self.ret["zma10_ratio"][position - 1] >= ma10_ratio_threshold:
            # ma10_down_trend = 1

            # if ma10_ratio >= ma10_ratio_threshold and self.ret["zma10_ratio"][position - 1] < ma10_ratio_threshold:
            # ma10_down_trend = 0

            if ma10_ratio < 0 and self.ret["zma10_ratio"][position - 1] >= 0:
                ma10r_down_cross_zero = 1
            else:
                ma10r_down_cross_zero = 0

            if ma10_ratio >= 0 and self.ret["zma10_ratio"][position - 1] < 0:
                ma10r_up_cross_zero = 1
            else:
                ma10r_up_cross_zero = 0

            if ma10_ratio_ratio < 0 and self.ret["zma10_ratio_ratio"][position - 1] >= 0:
                ma10rr_down_cross_zero = 1
            else:
                ma10rr_down_cross_zero = 0

            if ma10_ratio_ratio >= 0 and self.ret["zma10_ratio_ratio"][position - 1] < 0:
                ma10rr_up_cross_zero = 1
            else:
                ma10rr_up_cross_zero = 0

            if ma10rr_down_cross_zero == 1 and ma10_ratio < 0:
                trend_down = 1
            if ma10r_down_cross_zero == 1:
                trend_down = 1

            if ma10rr_up_cross_zero == 1:
                trend_down = 0

            good_hill = 0
            zma10_rrr_short_cross_float = -0.001
            if ma10_ratio_ratio_short >= ma10_ratio_ratio + zma10_rrr_short_cross_float and \
                            self.ret["zma10_ratio_ratio_short"][position - 1] < self.ret["zma10_ratio_ratio"][
                                position - 1] + zma10_rrr_short_cross_float:
                ma10_rr_up = 1
                if trend_down == 1:
                    ma10_r_r_up_ok = 1
                    up_pos = position
                    # print("ma10_r_r_up_ok")
                else:
                    ma10_r_r_up_ok = 0
            # down cross ma10_ratio
            #if ma10_ratio_ratio_short < ma10_ratio_ratio - zma10_rrr_short_cross_float and \
                            #self.ret["zma10_ratio_ratio_short"][position - 1] >= self.ret["zma10_ratio_ratio"][
                                #position - 1] - zma10_rrr_short_cross_float:

            if (ma10_ratio_ratio_short < 0 and \
                    self.ret["zma10_ratio_ratio_short"][position - 1] >= 0) or \
                    ( ma10_ratio_ratio_short < ma10_ratio_ratio - zma10_rrr_short_cross_float and \
                    self.ret["zma10_ratio_ratio_short"][position - 1] >= self.ret["zma10_ratio_ratio"][position - 1] - zma10_rrr_short_cross_float):
                ma10_rr_down = 1
                if trend_down == 1:
                    ma10_r_r_down_ok = 1
                    # print("ma10_r_r_down_ok")
                    try:
                        if ma10_r_r_up_ok == 1 and ma10_r_r_down_ok == 1:
                            if position - up_pos <= 240:
                                good_hill = 1
                                trend_down = 0
                            else:
                                plots.add_annotate(position, cur, 1, "hill")
                                print("hill time out", self.ret["time"][position], "ma10-r-r:", ma10_ratio_ratio,
                                      " ma10_ratio:", ma10_ratio, " ma20_ratio", ma20_ratio, " duration:",
                                      str((position - up_pos) / 2), " seconds")
                    except:
                        print("")

                ma10_rr_up = 0
                ma10_rr_down = 0
                ma10_r_r_up_ok = 0
                ma10_r_r_down_ok = 0

            if good_hill == 1:
                if ma10_ratio <= -1 and ma20_ratio < -1:
                    if ma10_ratio_ratio <= -0.004 and \
                            ((ma10_ratio_ratio_ratio - self.ret["zma10_ratio_ratio_ratio"][
                                    position - 20]) < 0 or ma10_ratio_ratio_ratio < 0):
                        plots.add_annotate(position, cur, 1, "555\n" + str(cur) + "\n" + str(ma10_ratio) + "/" + str(
                            ma20_ratio) + "\nma10_rr" + str(ma10_ratio_ratio) + "\nma10_rrr" + str(
                            ma10_ratio_ratio_ratio))
                        self.mark_trade(position, 555)
                        print(" duration:", str((position - up_pos) / 2), " seconds")
                        trend_down = 0

            position += 1
        return 1



    def mark_pure004(self, plots):
        ma10_r_r_r_value = -0.004
        ma20_many_head = -2
        ma10_r_r_value = -0.005
        ma10_r_r_value_short = -0.01
        ma10_r_r_small_value = 0
        start = 121
        position = start


        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio_ratio_ratio = self.ret["zma10_ratio_ratio_ratio"][position]
            ma10_ratio_ratio = self.ret["zma10_ratio_ratio"][position]
            ma10_ratio_ratio_short = self.ret["zma10_ratio_ratio_short"][position]
            ma10_ratio = self.ret["zma10_ratio"][position]
            MA10_cur = self.ret["zma10"][position]
            MA20_cur = self.ret["ma20"][position]
            ma20_ratio = self.ret["ma20_ratio"][position]
            cur = self.ret["cur"][position]

            ## when ma10-r-r-r drops to -0.004
            if ma10_ratio_ratio_ratio <= ma10_r_r_r_value and self.ret["zma10_ratio_ratio_ratio"][position - 1] > ma10_r_r_r_value:
                ### 111 turning point drops fast
                ### a. ma20_r >= -2

                plots.add_annotate(position, cur, 1, "1114\n" + str(cur) + "\n" + str(ma10_ratio) + "/" + str(
                    ma20_ratio) + "\nma10_rr" + str(ma10_ratio_ratio) + "\nma10_rrr" + str(ma10_ratio_ratio_ratio))


            position += 1
        return 1

    def detect_start_bull(self):
        ma10_r_r_r_value = -0.004
        ma20_many_head = -2
        ma10_r_r_value = -0.005
        ma10_r_r_value_short = -0.01
        ma10_r_r_small_value = -0.001
        ma10_break_val = 5

        start = 1200 + 121 + 360 + 120 + 1
        position = start

        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio_ratio_ratio = self.ret["zma10_ratio_ratio_ratio"][position]
            ma10_ratio_ratio = self.ret["zma10_ratio_ratio"][position]
            ma10_ratio_ratio_short = self.ret["zma10_ratio_ratio_short"][position]
            ma10_ratio = self.ret["zma10_ratio"][position]
            MA5_cur = self.ret["zma5"][position]
            MA10_cur = self.ret["zma10"][position]
            MA20_cur = self.ret["ma20"][position]
            ma20_ratio = self.ret["ma20_ratio"][position]
            cur = self.ret["cur"][position]

            if position == start:
                ma10_cross_zero_pos = 0
                if ma20_ratio < 0:
                    ma20_up = 1
                else:
                    ma20_up = 0

            if ma20_ratio > 0 and self.ret["ma20_ratio"][position - 1] <= 0:
                ma20_up = 1
            if ma20_ratio < 0 and self.ret["ma20_ratio"][position - 1] >= 0:
                ma20_up = 0

            if ma10_ratio >= 0 and self.ret["zma10_ratio"][position - 1] < 0:
                ma10_cross_zero_pos = position

            if ma20_up == 1 and \
                    self.ret["zma10"][ma10_cross_zero_pos] < self.ret["ma20"][ma10_cross_zero_pos] and \
                    self.ret["zma10_ratio"][ma10_cross_zero_pos] > self.ret["ma20_ratio"][ma10_cross_zero_pos]:


                if ma10_ratio >= ma10_break_val and self.ret["zma10_ratio"][position - 1] < ma10_break_val:
                    #print("MA10 R break 5 ", self.ret["time"][position], " ma10rr:",self.ret["zma10_ratio_ratio"][position])
                    if ma10_ratio_ratio > 0.005 and position - ma10_cross_zero_pos < 600:
                        bull_wait = 1

                if ma10_ratio < 0 and self.ret["zma10_ratio"][position - 1] >= 0:
                    bull_wait = 0

                try:
                    if bull_wait == 1 and ma20_up == 1:
                        if cur - MA5_cur <= 5:
                            ready_to_buy = 360
                            self.mark_trade(position, 8001)
                            bull_wait = 0
                            ma20_up = 0
                except:
                    x=1
            else:
                bull_wait = 0
#######ADVICE:
#####            1. should cross MA20, far away


            position += 1
        return 1



    def detect_turn2bear2(self):
        ma10_r_r_r_value = -0.004
        ma20_many_head = -2
        ma10_r_r_value = -0.005

        start = 1200 + 121 + 360 + 120 + 1
        position = start


        ##"No.", "cur", "time", "zma10", "ma20", "zma10_ratio", "zma10_ratio_ratio", "zma10_ratio_ratio_ratio", "trade_mark"
        while position < self.count:
            ma10_ratio_ratio_ratio = self.ret["zma10_ratio_ratio_ratio"][position]
            ma10_ratio_ratio = self.ret["zma10_ratio_ratio"][position]
            ma10_ratio_ratio_short = self.ret["zma10_ratio_ratio_short"][position]
            ma10_ratio = self.ret["zma10_ratio"][position]
            MA10_cur = self.ret["zma10"][position]
            MA20_cur = self.ret["ma20"][position]
            ma20_ratio = self.ret["ma20_ratio"][position]
            cur = self.ret["cur"][position]

            if ma10_ratio_ratio_ratio >=0  and self.ret["zma10_ratio_ratio_ratio"][position - 1] < 0:
                if ma10_ratio <= -4 and ma20_ratio < 0:
                    if ma10_ratio_ratio <= ma10_r_r_value and cur < MA10_cur:
                        self.mark_trade(position, 444)
                        print("")

            position += 1
        return 1

    def readData(self, start, end):
        ret = self.queryData(start, end)
        if ret == -1:
            print("query fail")
            return -1
        self.parse_data()
        self.cal_data()

    def daytestFuc(self):
        self.strategy_1st()
#        self.updateDayTestData_trade_mark(self.ret)
#        judge_ret = self.judge(trade_record)
#        print(judge_ret)

    def store_history(self, start, end):
        ret = self.queryData(start, end)
        if ret == -1:
            print("query fail")
            return -1
        self.parse_data()
        self.cal_data()

#        print(self.ret)
        self.addDayTestData(self.ret)

    def get_data_direct(self, start, end):
        ret = self.queryData(start, end)
        if ret == -1:
            print("query fail")
            return -1
        self.parse_data()
        self.cal_data()

    def read_history(self,start_time, end_time):
        s = time.time()
        self.queryDayTestData(start_time, end_time)
        e = time.time()
        #print("Read Completed.", str(e - s))
        s = time.time()
        self.parseDayTestData()
        e = time.time()
        #print("Parse Completed.", str(e - s))
        self.count = self.daytestcount
        #self.cal_bull_decrease()
        #self.cal_zmab()
        self.cal_ma50()
        self.cal_zma5()
        self.cal_zma5_ratio_simple()
        self.cal_zma5_ratio_simple_ratio()
        self.cal_zma1()
        self.cal_zma1_ratio_simple()
        self.cal_zma1_ratio_short_simple()
        #self.cal_zma1_ratio_ratio()
        #self.cal_zma1_zma10_gap()
        #self.cal_zma1_zma10_gap_scope()
        #self.cal_bear_increase()

    def insert_para_test(self):
        zma20_ratio_list = [0.001, 0.002, 0.003, 0.004]
        zma10_ratio_ratio_list = [0.000005, 0.000008, 0.00001, 0.000012]
        cur_ratio_list = [5000, 8000, 10000, 12000, 15000]

        for zma20_r in zma20_ratio_list:
            for zma10_r_r in zma10_ratio_ratio_list:
                for cur_r in cur_ratio_list:
                    self.myop.dbop_add_adj_paras(self.mydb,zma20_r,zma10_r_r,cur_r)

    def get_cur_words(self, position):
        ma10_ratio_ratio_ratio = self.ret["zma10_ratio_ratio_ratio"][position]
        ma10_ratio_ratio = self.ret["zma10_ratio_ratio"][position]
        ma10_ratio_ratio_short = self.ret["zma10_ratio_ratio_short"][position]
        ma10_ratio = self.ret["zma10_ratio"][position]
        MA10_cur = self.ret["zma10"][position]
        MA20_cur = self.ret["ma20"][position]
        ma20_ratio = self.ret["ma20_ratio"][position]
        cur = self.ret["cur"][position]
        s = "cur:" + str(cur) + "\nMA_R" + str(ma10_ratio) + "/" + str(ma20_ratio) + \
              "\nMA10_rr" + str(ma10_ratio_ratio) + "\nma10_rrr" + str(ma10_ratio_ratio_ratio)
        return s

    def export_ret(self):
        self.ret.to_csv("C:\\export.csv", index = False)

if __name__ == "__main__":
#    Usage

    date_list1 = ["2017-08-10", "2017-08-11","2017-08-14","2017-08-15","2017-08-16","2017-08-17","2017-08-18","2017-08-21","2017-08-22","2017-08-24"]
    date_list2 = ["2017-08-09", "2017-08-08","2017-08-07","2017-08-04","2017-08-03","2017-08-02","2017-07-31","2017-07-28","2017-07-27"]

    date_list_all = ["2017-07-27", "2017-07-28", "2017-07-31", "2017-08-02", "2017-08-03", "2017-08-04", "2017-08-07", "2017-08-08", "2017-08-09",
                 "2017-08-10", "2017-08-11", "2017-08-14", "2017-08-15", "2017-08-16", "2017-08-17", "2017-08-18", "2017-08-21", "2017-08-22", "2017-08-24", "2017-08-25"]
    date_list_555 = ["2017-08-02", "2017-08-03", "2017-08-04", "2017-08-07",
             "2017-08-10",  "2017-08-14",  "2017-08-17", "2017-08-18",
             "2017-08-24", "2017-08-25"]
    date_list_all_12 = ["2017-07-27", "2017-07-28",  "2017-08-02",  "2017-08-04", "2017-08-07",
                 "2017-08-08",
                 "2017-08-10", "2017-08-11", "2017-08-14", "2017-08-15", "2017-08-16", "2017-08-17", "2017-08-18",
                 "2017-08-21",  "2017-08-24", "2017-08-25"]

    stored_date_list_all = \
                ["2017-07-27", "2017-07-28", "2017-07-31", "2017-08-02", "2017-08-03", "2017-08-04", "2017-08-07",
                 "2017-08-08", "2017-08-09",
                 "2017-08-10", "2017-08-11", "2017-08-14", "2017-08-15", "2017-08-16", "2017-08-17", "2017-08-18",
                 "2017-08-21", "2017-08-22","2017-08-24", "2017-08-25","2017-08-28","2017-08-29","2017-08-30","2017-08-31",
                 "2017-09-01","2017-09-04","2017-09-05","2017-09-06","2017-09-07"]
    not_stored = []

    test = daytest()
    test.Initialize()
    #test.store_history(start_time, end_time)

    total_s = time.time()

    for date in not_stored:
        start_time = date + " " + "9:20:00"
        end_time = date + " " + "16:00:00"
        test.store_history(start_time, end_time)
        s = time.time()
        #test.get_data_direct(start_time, end_time)
        #test.read_history(start_time, end_time)
        e = time.time()
        print("Data finished:" + str( e - s ))
        #test.detectSignal2()
        #test.detect_turn2bear()
        #test.detect_start_bull()
        #test.detect_turn2bear2()
#        test.testParameters()

    total_e = time.time()
    print("Total Time:", str( total_e - total_s ))


########For plos

    plot_date_day = ["2017-09-04"]
    for plot_date in stored_date_list_all:
        s = time.time()
        start_time = plot_date + " " + "9:20:00"
        end_time = plot_date + " " + "16:00:00"
        test.read_history(start_time, end_time)
        #test.get_data_direct(start_time, end_time)
        plots = show_plots(test)
        plots.init_plot(4, plot_date+"-bull002")
        test.mark_base(plots)


        # 8/29 8/28 8/24 8/21 8/18 8/16 8/15 8/11 8/8 8/2 | 08/14
        # ret = test.mark_bear_start(plots)
        #test.mark_bear_continue(plots)

        # 3 8 10 17 21
        #test.mark_bear_about_die(plots)

        #test.mark_pure004(plots)
        # ret = test.mark_bear_rrcross(plots)
        # ret = test.mark_bear_rrcross_pure(plots)
        ret = test.mark_bear_zma1_zma10_cross(plots)

        # ret = test.mark_rr_cross(plots)
        #test.export_ret()

        zma1_r_r_tl = test.ret["zma1_ratio_ratio"]
        plots.prepare_plot(zma1_r_r_tl, 4)
        e = time.time()
        print("Data finished:" + str( e - s ))

        if ret != 0:
            plots.show_plot()
        else:
            #plots.show_plot()
            plots.close_plot_all()



