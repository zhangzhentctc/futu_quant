from db.db_ma_trend import *
#from openft.open_quant_context import *
import pandas as pd
import time
import math


# "No.", "cur", "time", "zma10", "zma20", "zma10_ratio", "zma20_ratio", "zma20_ratio_ratio", "zma_gap", "zma_gap_ratio", "zma_gap_ratio_ratio",
NO_POS = 0
CUR_POS = 1
TIME_POS = 2
ZMA10_POS = 3
ZMA20_POS = 4
ZMA10_RATIO_POS = 5
ZMA20_RATIO_POS = 6
ZMA10_RATIO_RATIO_POS = 7
ZMA20_RATIO_RATIO_POS = 8

ZMA_GAP_POS = 9
ZMA_GAP_RATIO_POS = 10
ZMA_GAP_RATIO_RATIO_POS = 11
# ZMA_GAP_RATIO_RATIO_R_POS = 12
TRADE_MARK_POS = 13
CUR_RATIO_POS = 14

NO_SRC_POS = 0
CUR_SRC_POS = 3
TIME_SRC_POS = 8



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
            data.append({"No.": line[NO_POS], "cur": line[CUR_POS], "time":line[TIME_POS], "zma10":line[ZMA10_POS],  "zma20":line[ZMA20_POS], "zma10_ratio":line[ZMA10_RATIO_POS],"zma20_ratio": line[ZMA20_RATIO_POS],  "zma10_ratio_ratio": line[ZMA10_RATIO_RATIO_POS], "zma20_ratio_ratio": line[ZMA20_RATIO_RATIO_POS], "zma_gap": line[ZMA_GAP_POS], "zma_gap_ratio": line[ZMA_GAP_RATIO_POS], "zma_gap_ratio_ratio": line[ZMA_GAP_RATIO_RATIO_POS], "zma_gap_ratio_ratio_r": line[ZMA_GAP_RATIO_RATIO_R_POS], "trade_mark": 0, "cur_ratio": line[CUR_RATIO_POS]})

        self.ret = pd.DataFrame(data, columns=["No.", "cur", "time", "zma10", "zma20", "zma10_ratio", "zma20_ratio", "zma10_ratio_ratio", "zma20_ratio_ratio", "zma_gap", "zma_gap_ratio", "zma_gap_ratio_ratio", "zma_gap_ratio_ratio_r", "trade_mark", "cur_ratio"])
        return self.ret

    ##
    #



    def addDayTestData(self, data):
        len = 0
        for index in data.iterrows():
             len += 1
        for i in range(2600, len):
             self.myop.dbop_add_day_data(self.mydb, data["No."][i], data["cur"][i], data["time"][i],
                                        data["zma10"][i], data["zma20"][i],
                                        data["zma10_ratio"][i], data["zma20_ratio"][i],
                                        data["zma10_ratio_ratio"][i], data["zma20_ratio_ratio"][i], data["zma_gap"][i], data["zma_gap_ratio"][i],
                                        data["zma_gap_ratio_ratio"][i], data["zma_gap_ratio_ratio_r"][i],
                                        data["cur_ratio"][i])

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
        self.count = self.op.dbop_read_ma_dur2(self.db, start, end)
        if self.count == 0:
            return -1
        return self.count

    def getNextData(self):
        ret = self.op.dbop_read_ma_dur_next(self.db)
        return ret

    def parse_data(self):
        data = []
        pre_cur = 0
        for i in range(0, self.count):
            line = self.getNextData()
            if line[CUR_SRC_POS] == 0:
                data.append({"No.": line[NO_SRC_POS], "cur": pre_cur, "time": line[TIME_SRC_POS], "trade_mark": 0, "cur_ratio":0})
            else:
                data.append({"No.": line[NO_SRC_POS], "cur": line[CUR_SRC_POS], "time": line[TIME_SRC_POS], "trade_mark": 0, "cur_ratio":0})
            pre_cur =line[CUR_SRC_POS]
        self.ret = pd.DataFrame(data, columns=["No.", "cur", "time", "zma10", "zma20", "zma10_ratio", "zma20_ratio", "zma10_ratio_ratio", "zma20_ratio_ratio", "zma_gap", "zma_gap_ratio", "zma_gap_ratio_ratio", "zma_gap_ratio_ratio_r", "trade_mark", "cur_ratio"])

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

    ## MA
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

    def cal_zma20_ratio(self):
        len = 2400
        t = 60
        val =0
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            ret, val = self.optimized_least_square_method(i - t + 1, i, "zma20")
            if ret == -1:
                val = 0
            self.ret.iloc[i, ZMA20_RATIO_POS] = val
        return 1

    def cal_zma20_ratio_ratio(self):
        len = 2400
        t = 240
        val =0
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            ret, val = self.optimized_least_square_method(i - t + 1, i, "zma20_ratio")
            if ret == -1:
                val = 0
            self.ret.iloc[i, ZMA20_RATIO_RATIO_POS] = val
        return 1

    def cal_zma10_ratio_ratio(self):
        len = 1200
        t = 240
        val = 0
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            ret, val = self.optimized_least_square_method(i - t + 1, i, "zma10_ratio")
            if ret == -1:
                val = 0
            self.ret.iloc[i, ZMA10_RATIO_RATIO_POS] = val
        return 1

    ## MA GAP
    def cal_zma_gap(self):
        len = 2400
        start_pos = len
        if self.count < start_pos + 1:
            return -1
        for i in range(start_pos, self.count):
            val = self.ret["zma10"][i] - self.ret["zma20"][i]
            self.ret.iloc[i, ZMA_GAP_POS] = val
        return 1

    def cal_zma_gap_ratio(self):
        len = 2400
        t = 360
        val =0
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            ret, val = self.optimized_least_square_method(i - t + 1, i, "zma_gap")
            if ret == -1:
                val = 0
            self.ret.iloc[i, ZMA_GAP_RATIO_POS] = float(val)
        return 1

    def cal_zma_gap_ratio_ratio(self):
        len = 1200
        t = 360
        val =0
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            ret, val = self.optimized_least_square_method(i - t + 1, i, "zma_gap_ratio")
            if ret == -1:
                val = 0
            self.ret.iloc[i, ZMA_GAP_RATIO_RATIO_POS] = val
            ret, r = self.optimized_least_square_method_r(i - t + 1, i, "zma_gap_ratio")
            if ret == -1:
                r = 0
            self.ret.iloc[i, ZMA_GAP_RATIO_RATIO_R_POS] = r
        return 1

    ## OLD
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
        print("cal_cur_ratio start")
        self.cal_cur_ratio()
        end_time = time.time()
        print("cal_cur_ratio finished:" + str( end_time - start_time ))

        start_time = time.time()
        print("cal_zma10 start")
        self.cal_zma10()
        end_time = time.time()
        print("cal_zma10 finished:" + str( end_time - start_time ))

        start_time = time.time()
        print("cal_zma20")
        self.cal_zma20()
        end_time = time.time()
        print("cal_zma20 finished:" + str( end_time - start_time))

        start_time = time.time()
        print("cal_zma10_ratio")
        self.cal_zma10_ratio()
        end_time = time.time()
        print("cal_zma10_ratio finished:" + str( end_time - start_time))

        start_time = time.time()
        print("cal_zma20_ratio")
        self.cal_zma20_ratio()
        end_time = time.time()
        print("cal_zma20_ratio finished:" + str( end_time - start_time))

        start_time = time.time()
        print("cal_zma10_ratio_ratio")
        self.cal_zma10_ratio_ratio()
        end_time = time.time()
        print("cal_zma10_ratio_ratio finished:" + str( end_time - start_time))

        start_time = time.time()
        print("cal_zma20_ratio_ratio")
        self.cal_zma20_ratio_ratio()
        end_time = time.time()
        print("cal_zma20_ratio_ratio finished:" + str( end_time - start_time))

        start_time = time.time()
        print("cal_zma_gap")
        self.cal_zma_gap()
        end_time = time.time()
        print("cal_zma_gap finished:" + str( end_time - start_time))

        start_time = time.time()
        print("cal_zma_gap_ratio")
        self.cal_zma_gap_ratio()
        end_time = time.time()
        print("cal_zma_gap_ratio finished:" + str( end_time - start_time))

        start_time = time.time()
        print("cal_zma_gap_ratio_ratio")
        self.cal_zma_gap_ratio_ratio()
        end_time = time.time()
        print("cal_zma_gap_ratio_ratio finished:" + str( end_time - start_time))



    def mark_trade(self, position, mark):
        self.ret.iloc[position, TRADE_MARK_POS] = mark

    def detectSignal(self):
        start = 2400 + 60 + 1
        position = start

        while position < self.count:
            if self.ret["zma_gap"][position] >= 5 and self.ret["zma_gap"][position] <= 10 and self.ret["zma_gap_ratio"][position] > 0.002 and self.ret["zma_gap_ratio_ratio"][position] > 0.000001 and \
                            self.ret["zma10_ratio"][position] > self.ret["zma20_ratio"][position] and self.ret["zma20_ratio"][position] >= 0.003 and self.ret["zma20_ratio_ratio"][position] > 0:
                self.mark_trade(position, 1)
            if self.ret["zma_gap"][position] <= -5 and self.ret["zma_gap"][position] >= -10 and  self.ret["zma_gap_ratio"][position] < -0.002 and self.ret["zma_gap_ratio_ratio"][position] < -0.000001 and \
                            self.ret["zma10_ratio"][position] < self.ret["zma20_ratio"][position] and self.ret["zma20_ratio"][position] <= -0.003 and self.ret["zma20_ratio_ratio"][position] < 0:
                self.mark_trade(position, -1)
            position += 1
        return 1

    def strategy_1st(self):
        start = 2400 + 60 + 1
        position = start

        while position < self.count:
            if self.ret["zma_gap"][position] >= 5 and self.ret["zma_gap"][position] <= 15 and \
                            self.ret["zma_gap_ratio"][position] > 0 and self.ret["zma_gap_ratio_ratio"][position] > 0 and abs(self.ret["zma_gap_ratio_ratio_r"][position]) > 0.3 and \
                            self.ret["zma10_ratio"][position] > self.ret["zma20_ratio"][position] and \
                            self.ret["zma20_ratio"][position] >= 0.005 and self.ret["zma10_ratio_ratio"][position] > 0 and self.ret["zma20_ratio_ratio"][position] > 0:
                self.mark_trade(position, 1)
            if self.ret["zma_gap"][position] <= -5 and self.ret["zma_gap"][position] >= -15 and \
                            self.ret["zma_gap_ratio"][position] < -0 and self.ret["zma_gap_ratio_ratio"][position] < 0 and abs(self.ret["zma_gap_ratio_ratio_r"][position]) > 0.3 and \
                            self.ret["zma10_ratio"][position] < self.ret["zma20_ratio"][position] and \
                            self.ret["zma20_ratio"][position] <= -0.005 and self.ret["zma10_ratio_ratio"][position] < 0 and self.ret["zma20_ratio_ratio"][position] < 0:
                self.mark_trade(position, -1)
            position += 1
        return 1

    ######
    ##   Get Test Parameters from Database
    ##     To: Dataframe: self.adj_paras
    ######
    def getAdjParas(self):
        ret = self.queryAdjParas()
        if ret == -1:
            print("query fail")
            return -1
        self.parseAdjParas()

    def queryAdjParas(self):
        self.AdjParas = self.myop.dbop_read_adj_paras(self.mydb)
        if self.AdjParas == 0:
            return -1
        return self.AdjParas

    def getNextAdjParas(self):
        ret = self.myop.dbop_read_adj_paras_next(self.mydb)
        return ret

    def parseAdjParas(self):
        data = []
        for i in range(0, self.AdjParas):
            line = self.getNextAdjParas()
            data.append({"para_index": line[0], "zma10_ratio":line[1],"zma20_ratio": line[2],  "zma10_ratio_ratio": line[3], "zma20_ratio_ratio": line[4],
                         "zma_gap_min": line[5], "zma_gap_max": line[6], "zma_gap_ratio": line[7], "zma_gap_ratio_ratio": line[8], "zma20": line[9], "cur_ratio":line[10]})

        self.adj_paras = pd.DataFrame(data, columns=["para_index", "zma10_ratio", "zma20_ratio", "zma10_ratio_ratio", "zma20_ratio_ratio", "zma_gap_min", "zma_gap_max", "zma_gap_ratio", "zma_gap_ratio_ratio", "zma20", "cur_ratio"])
        return self.adj_paras

    ######
    ##   Get Test Trade Mark from Database
    ##     To: Dataframe: self.trade_mark
    ######
    def getTradeMark(self):
        ret = self.queryTradeMark()
        if ret == -1:
            print("query fail")
            return -1
        self.parseTradeMark()

    def queryTradeMark(self):
        self.tradeMark = self.myop.dbop_read_mark_trade(self.mydb)
        if self.tradeMark == 0:
            return -1
        return self.tradeMark

    def getNextTradeMark(self):
        ret = self.myop.dbop_read_mark_trade_next(self.mydb)
        return ret

    def parseTradeMark(self):
        data = []
        for i in range(0, self.tradeMark):
            line = self.getNextTradeMark()
            data.append({"No.": line[1], "para_index":line[2],"trade_mark": line[3]})

        self.trade_mark = pd.DataFrame(data, columns=["No.", "para_index", "trade_mark"])
        return self.trade_mark

    ####
    ##    Mark Trade to DB by given Parameters
    ####
    def mark_trade_given_paras(self, No, index, mark):
        self.myop.dbop_add_mark_trade(self.mydb, No, index, mark)


    def strategy_func(self, adj_paras):
        start = 2400 + 60 + 1
        position = start
        record_c_trend = -1
        record_p_trend = -1
        trend_c_cnt = 0
        trend_p_cnt = 0
        trend = 0
        while position < self.count:
            if self.ret["zma10_ratio"][position] > 0:
                if trend != 1:
                    trend = 1
                    trend_c_cnt += 1
            else:
                if trend != -1:
                    trend = -1
                    trend_p_cnt += 1


            if self.ret["zma_gap"][position] >= adj_paras.zma_gap_min_sh and self.ret["zma_gap"][position] <= adj_paras.zma_gap_max_sh and \
                            self.ret["zma_gap_ratio"][position] > adj_paras.zma_gap_ratio_sh and self.ret["zma_gap_ratio_ratio"][position] > adj_paras.zma_gap_ratio_ratio_sh  and \
                            self.ret["zma10_ratio"][position] > self.ret["zma20_ratio"][position] and \
                            self.ret["zma20_ratio"][position] >= adj_paras.zma20_ratio_sh and self.ret["zma10_ratio_ratio"][position] > adj_paras.zma10_ratio_ratio_sh and self.ret["zma20_ratio_ratio"][position] > adj_paras.zma20_ratio_ratio_sh:
                if record_c_trend != trend_c_cnt:
                    self.mark_trade_given_paras(self.ret["No."][position], adj_paras.index,  1)
                    record_c_trend = trend_c_cnt

            if self.ret["zma_gap"][position] <= -1 * adj_paras.zma_gap_min_sh and self.ret["zma_gap"][position] >= -1 * adj_paras.zma_gap_max_sh and \
                            self.ret["zma_gap_ratio"][position] < -1 * adj_paras.zma_gap_ratio_sh and self.ret["zma_gap_ratio_ratio"][position] < -1 * adj_paras.zma_gap_ratio_ratio_sh  and \
                            self.ret["zma10_ratio"][position] < self.ret["zma20_ratio"][position] and \
                            self.ret["zma20_ratio"][position] <= -1 * adj_paras.zma20_ratio_sh and self.ret["zma10_ratio_ratio"][position] < -1 * adj_paras.zma10_ratio_ratio_sh and self.ret["zma20_ratio_ratio"][position] < -1 * adj_paras.zma20_ratio_ratio_sh:
                if record_p_trend != trend_p_cnt:
                    self.mark_trade_given_paras(self.ret["No."][position], adj_paras.index,  -1)
                    record_p_trend = trend_p_cnt
            position += 1

        return 1

    def strategy_break_func(self, adj_paras):
        start = 2400 + 60 + 1
        position = start
        record_c_trend = -1
        record_p_trend = -1
        trend_c_cnt = 0
        trend_p_cnt = 0
        trend = 0
        while position < self.count:
            if self.ret["zma10_ratio"][position] > 0:
                if trend != 1:
                    trend = 1
                    trend_c_cnt += 1
                    if record_c_trend != trend_c_cnt:
                        if self.ret["cur_ratio"][position] > adj_paras.cur_ratio_sh and \
                           self.ret["zma20_ratio"][position] < adj_paras.zma20_sh and \
                           self.ret["zma10_ratio_ratio"][position] > adj_paras.zma10_ratio_ratio_sh and \
                           self.ret["zma10_ratio_ratio"][position] * self.ret["zma20_ratio_ratio"][position] > 0:
                            self.mark_trade_given_paras(self.ret["No."][position], adj_paras.index, -1)
                        record_c_trend = trend_c_cnt
            else:
                if trend != -1:
                    trend = -1
                    trend_p_cnt += 1
                    if record_p_trend != trend_p_cnt:
                        if self.ret["cur_ratio"][position] < -1 * adj_paras.cur_ratio_sh and \
                           self.ret["zma20_ratio"][position] > -1 * adj_paras.zma20_sh and \
                           self.ret["zma10_ratio_ratio"][position] < -1 * adj_paras.zma10_ratio_ratio_sh and \
                           self.ret["zma10_ratio_ratio"][position] * self.ret["zma20_ratio_ratio"][position] > 0:
                            self.mark_trade_given_paras(self.ret["No."][position], adj_paras.index, 1)
                        record_p_trend = trend_p_cnt

            position += 1

        return 1


    ####
    ##  Write judge result
    ####
    def judge_func(self, adj_paras_index):
        # Get length
        day_data_len = 0
        for index in self.ret.iterrows():
            day_data_len += 1

        trade_mark_tol_len = 0
        for index in self.trade_mark.iterrows():
            trade_mark_tol_len += 1

        # Find data. Filter adj_paras
        trade_mark_len = 0
        data = []
        for i in range(0, trade_mark_tol_len):
            if self.trade_mark["para_index"][i] == adj_paras_index:
                data.append({"No.": self.trade_mark["No."][i], "para_index":self.trade_mark["para_index"][i],"trade_mark": self.trade_mark["trade_mark"][i]})
                trade_mark_len += 1
        indexed_trade_mark = pd.DataFrame(data, columns=["No.", "para_index", "trade_mark"])

#        print(indexed_trade_mark)
        # Start judging
        i = 0
        j = 0
        while( i < trade_mark_len ):
            while indexed_trade_mark["No."][i] < self.ret["No."][j]:
                i += 1
                if i >= trade_mark_len - 1 or j >= day_data_len - 1:
                    break
            if i>= trade_mark_len - 1 or j >= day_data_len - 1:
                break
            while indexed_trade_mark["No."][i] != self.ret["No."][j]:
                j += 1
                if i >= trade_mark_len - 1 or j >= day_data_len - 1:
                    break
            if i >= trade_mark_len - 1 or j >= day_data_len - 1:
                break
            buy_pos = j
            buy_val = self.ret["cur"][buy_pos]
            max_pos = buy_pos
            max_val = 0
            turn_pos = buy_pos
            turn_val = 0
            # When zma10_ratio turns, break
            while self.ret["zma10_ratio"][buy_pos] * self.ret["zma10_ratio"][j] > 0 and j < day_data_len:
                # C, trend is up, value is over buy val
                if self.ret["zma10_ratio"][buy_pos] >0:
                    if self.ret["cur"][j] > buy_val:
                        if self.ret["cur"][j] - buy_val > max_val:
                            max_val = self.ret["cur"][j] - buy_val
                            max_pos = j
                # P, trend is down, value is below buy val
                else:
                    if self.ret["cur"][j] < buy_val:
                        if buy_val - self.ret["cur"][j]  > max_val:
                            max_val = buy_val - self.ret["cur"][j]
                            max_pos = j

                # Find cur when zma10 turns
                turn_pos = j
                turn_val = self.ret["cur"][j]

                j+=1
            passive_gap = self.ret["cur"][max_pos] - self.ret["cur"][buy_pos]
            turn_gap = turn_val - self.ret["cur"][buy_pos]
            self.write_judge_ret(self.ret["No."][buy_pos], indexed_trade_mark["trade_mark"][i], passive_gap, self.ret["No."][turn_pos], turn_gap, adj_paras_index)
            i += 1

    def write_judge_ret(self, No, mark, passive_gap, turn_pos, turn_gap, index):
        self.myop.dbop_add_judge_result(self.mydb, No, mark, passive_gap, turn_pos, turn_gap, index)


    ####
    ##  1. Get Paras from DB
    ##  2. Test Paras
    ####
    def testParameters(self):
        self.getAdjParas()

        len = 0
        for index in self.adj_paras.iterrows():
             len += 1
        for i in range(0, len):
            ## Get Parameters
            para = adjust_paras()
            para.index                  = self.adj_paras["para_index"][i]
            para.zma10_ratio_sh         = self.adj_paras["zma10_ratio"][i]
            para.zma20_ratio_sh         = self.adj_paras["zma20_ratio"][i]
            para.zma10_ratio_ratio_sh   = self.adj_paras["zma10_ratio_ratio"][i]
            para.zma20_ratio_ratio_sh   = self.adj_paras["zma20_ratio_ratio"][i]
            para.zma_gap_min_sh         = self.adj_paras["zma_gap_min"][i]
            para.zma_gap_max_sh         = self.adj_paras["zma_gap_max"][i]
            para.zma_gap_ratio_sh       = self.adj_paras["zma_gap_ratio"][i]
            para.zma_gap_ratio_ratio_sh = self.adj_paras["zma_gap_ratio_ratio"][i]
            para.zma20_sh               = self.adj_paras["zma20"][i]
            para.cur_ratio_sh           = self.adj_paras["cur_ratio"][i]

            ## Test Paras
            print("TEST STRATEGY " + str(i))
            self.strategy_func(para)


        self.getTradeMark()
        print(self.trade_mark)

        for i in range(0, len):
            ## Get Parameters
            para = adjust_paras()
            para.index = self.adj_paras["para_index"][i]

            ## Judge
            self.judge_func(para.index)



    def search_biggest(self, start, end, prod):
        max_value = 0
        value = 0
        if prod == 1:
            value = self.zmax(start, end)
        if prod == -1:
            value = self.zmin(start, end)
        max_value = abs(self.ret["cur"][start] - value)
        return max_value

    def zmin(self, start, end):
        min_v = self.ret["cur"][start]
        for i in (start + 1, end + 1):
            if self.ret["cur"][i] < min_v:
                min_v = self.ret["cur"][i]
        return min_v

    def zmax(self, start, end):
        max_v = self.ret["cur"][start]
        for i in (start + 1, end + 1):
            if self.ret["cur"][i] > max_v:
                max_v = self.ret["cur"][i]
        return max_v

    def judge(self, trade_record):
        len = 0
        ret = []
        for index in trade_record.iterrows():
            len += 1

        for i in range(0, len):
            start = trade_record.iloc[i, 0]
            end = trade_record.iloc[i, 1]
            prod = trade_record.iloc[i, 2]
            max = self.search_biggest(start, end, prod)
            ret.append(max)
        return ret

    def readData(self, start, end):
        ret = self.queryData(start, end)
        if ret == -1:
            print("query fail")
            return -1
        self.parse_data()
        self.cal_data()

    def daytestFuc(self):
        self.strategy_1st()
        self.updateDayTestData_trade_mark(self.ret)
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

    def read_history(self,start_time, end_time):
        self.queryDayTestData(start_time, end_time)
        self.parseDayTestData()
        self.count = self.daytestcount

    def insert_para_test(self):
        zma20_ratio_list = [0.001, 0.002, 0.003, 0.004]
        zma10_ratio_ratio_list = [0.000005, 0.000008, 0.00001, 0.000012]
        cur_ratio_list = [5000, 8000, 10000, 12000, 15000]

        for zma20_r in zma20_ratio_list:
            for zma10_r_r in zma10_ratio_ratio_list:
                for cur_r in cur_ratio_list:
                    self.myop.dbop_add_adj_paras(self.mydb,zma20_r,zma10_r_r,cur_r)


if __name__ == "__main__":
#    Usage
    date_list = ["2017-05-04"]

    test = daytest()
    test.Initialize()
#    test.store_history(start_time, end_time)


    for date in date_list:
        start_time = date + " " + "9:30:00"
        end_time = date + " " + "16:00:00"
#        test.store_history(start_time, end_time)


        test.read_history(start_time, end_time)
#        test.daytestFuc()
        test.testParameters()



"""
                start_point = -1
                curvity_threshold = 5
                duration = 2400
                if zma20_f == 1 and ratio_f == 1:
                    curvity_threshold = self.ret["delta_delta_zma20_ma60"][position]/ 10
                    for i in range(0, duration):
                        if trend == 1:
                            if self.ret["delta_delta_zma20_ma60"][position - i] < curvity_threshold:
                                start_point = position - i
                                break
                        if trend == -1:
                            if self.ret["delta_delta_zma20_ma60"][position - i] > -1 * curvity_threshold:
                                start_point = position - i
                                break
                    if start_point == -1:
                        curvity = 0
                    gap = float(self.ret["delta_delta_zma20_ma60"][position]) - float(
                        self.ret["delta_delta_zma20_ma60"][start_point])
                    print("aaaa")
                    print(self.ret["delta_delta_zma20_ma60"][position])
                    print(self.ret["delta_delta_zma20_ma60"][start_point])
                    print(gap)
                    print(position)
                    print(start_point)
                    if position - start_point == 0:
                        cuvity = 0
                    else:
                        curvity = gap / (position - start_point)
"""

'''
    def cal_delta_delta_zma20_ma60(self):
        start_pos = 2461
        if self.count < start_pos + 1:
            return -1
        for i in range(start_pos, self.count):
            val = self.ret["delta_zma20_ma60"][i] - self.ret["delta_zma20_ma60"][i-1]
            val *= 1000
            self.ret.iloc[i, 9] = val
        return 0
'''
# max_val = abs(self.ret["delta_zma20_ma60"][i])
# max_pos = i
# min_val = abs(self.ret["delta_zma20_ma60"][i])
# min_pos = i
# for j in range(i - t + 1, i + 1):
#    if abs(self.ret["delta_zma20_ma60"][j]) < min_val:
#        min_val = abs(self.ret["delta_zma20_ma60"][j])
#        min_pos = j
#    if abs(self.ret["delta_zma20_ma60"][j]) > max_val:
#        max_val = abs(self.ret["delta_zma20_ma60"][j])
#        max_pos = j
# if min_pos != i:
#    ret, val = self.simple_ratio(min_pos, i, "delta_zma20_ma60")
#    if ret == -1:
#        return -1
# else:
#    if max_pos != i:
#        ret, val = self.simple_ratio(max_pos, i, "delta_zma20_ma60")
#        if ret == -1:
#            return -1
#   else:
#       val = 0
# self.ret.iloc[i, 12] = float(val)
'''
    def cal_zma_gap_ratio(self):
        len = 2400
        t = 240
        start_pos = len + t
        if self.count < start_pos:
            return -1
        for i in range(start_pos, self.count):
            max_val = abs(self.ret["zma_gap"][i])
            max_pos = i
            min_val = abs(self.ret["zma_gap"][i])
            min_pos = i
            for j in range(i - t + 1, i + 1):
                if abs(self.ret["zma_gap"][j]) < min_val:
                    min_val = abs(self.ret["zma_gap"][j])
                    min_pos = j
                if abs(self.ret["zma_gap"][j]) > max_val:
                    max_val = abs(self.ret["zma_gap"][j])
                    max_pos = j
            if min_pos != i:
                ret, val = self.simple_ratio(min_pos, i, "zma_gap")
                if ret == -1:
                    return -1
            else:
                if max_pos != i:
                    ret, val = self.simple_ratio(max_pos, i, "zma_gap")
                    if ret == -1:
                        return -1
                else:
                    val = 0
            self.ret.iloc[i, ZMA_GAP_RATIO_POS] = float(val)
        return 1
'''