from db.db_ma_trend import *
#from openft.open_quant_context import *
import pandas as pd
import time

# "No.", "cur", "time", "zma10", "zma20", "zma10_ratio", "zma20_ratio", "zma20_ratio_ratio", "zma_gap", "zma_gap_ratio", "zma_gap_ratio_ratio",
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


class daytest:
    def __init__(self):
        self.count = 0
        self.daytestcount = 0

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
            data.append({"No.": line[NO_POS], "cur": line[CUR_POS], "time":line[TIME_POS], "zma10":line[ZMA10_POS],  "zma20":line[ZMA20_POS], "zma10_ratio":line[ZMA10_RATIO_POS],"zma20_ratio": line[ZMA20_RATIO_POS],  "zma20_ratio_ratio": line[ZMA20_RATIO_RATIO_POS], "zma_gap": line[ZMA_GAP_POS], "zma_gap_ratio": line[ZMA_GAP_RATIO_POS], "zma_gap_ratio_ratio": line[ZMA_GAP_RATIO_RATIO_POS]})

        self.ret = pd.DataFrame(data, columns=["No.", "cur", "time", "zma10", "zma20", "zma10_ratio", "zma20_ratio", "zma20_ratio_ratio", "zma_gap", "zma_gap_ratio", "zma_gap_ratio_ratio"])
        return self.ret

    def addDayTestData(self, data):
        len = 0
        for index in data.iterrows():
             len += 1
        for i in range(0, len):
             self.myop.dbop_add_day_data(self.mydb, data["No."][i], data["cur"][i], data["time"][i],
                                        data["zma10"][i], data["zma20"][i],
                                        data["zma10_ratio"][i], data["zma20_ratio"][i],
                                        data["zma20_ratio_ratio"][i], data["zma_gap"][i], data["zma_gap_ratio"][i],
                                        data["zma_gap_ratio_ratio"][i])

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
            if line[CUR_POS] == 0:
                data.append({"No.": line[NO_POS], "cur": pre_cur, "time": line[TIME_POS]})
            else:
                data.append({"No.": line[NO_POS], "cur": line[CUR_POS], "time": line[TIME_POS]})
            pre_cur =line[3]
        self.ret = pd.DataFrame(data, columns=["No.", "cur", "time", "zma10", "zma20", "zma10_ratio", "zma20_ratio", "zma20_ratio_ratio", "zma_gap", "zma_gap_ratio", "zma_gap_ratio_ratio"])
        return self.ret

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
            avr = avr0 - starter/len + self.ret["cur"][i]/len
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
        t = 240
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
        t = 180
        val =0
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            ret, val = self.optimized_least_square_method(i - t + 1, i, "zma_gap_ratio")
            if ret == -1:
                val = 0
            self.ret.iloc[i, ZMA_GAP_RATIO_RATIO_POS] = val
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
        return 1, ratio

    def simple_ratio(self, start, end, column):
        if self.count < start:
            return -1, 0
        ratio = (self.ret[column][end] - self.ret[column][start])/(end - start)
        return 1, ratio


    # Calculate all
    def cal_data(self):
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


    def detectSignal(self, ma20_shrethold, ma10_ma20_ratio_threshold):
        start = 2400 + 60 + 1
        position = start
        status = 0
        zma20_f = 0
        zma20_x_f = 0
        ratio_f = 0
        ratio_x_f = 0
        prod = 0
        data = []
        buy_position  = -1
        sell_position = -1
        cross = 0
        trend = 0

        while position < self.count:
            curvity = 0
            if self.ret["delta_zma20_ma60"][position] > 0:
                trend = 1
            else:
                trend = -1

            if abs(self.ret["delta_zma20_ma60"][position]) > ma20_shrethold:
   #             if zma20_f == 0:
   #                 print("delta_zma20_ma60 start: " + str(position))
                zma20_f = 1
            else:
 #               if zma20_f == 1:
 #                   print("delta_zma20_ma60 end: " + str(position))
                zma20_f = 0

            if abs(self.ret["delta_zma20_ma60"][position]) > 0:
                zma20_x_f = 1
            else:
                zma20_x_f = 0

            if self.ret["ratio"][position] > ma10_ma20_ratio_threshold:
 #               if ratio_f == 0:
 #                   print("ratio start: " + str(position))
                ratio_f = 1
            else:
#                if ratio_f == 1:
#                    print("ratio end: " + str(position))
                ratio_f = 0

            if self.ret["ratio"][position] > 1:
                ratio_x_f = 1
            else:
                ratio_x_f = 0

            if status == 0:
                if zma20_f == 1 and ratio_f == 1:
                    t = 240
                    ma20_max_pos = -1
                    ma20_max_val = 0
                    ma10_max_pos = -1
                    ma10_max_val = 0
                    for i in range (position - t + 1, position + 1):
                        if abs(self.ret["delta_zma20_ma60"][i] - self.ret["delta_zma20_ma60"][position]) > ma20_max_val:
                            ma20_max_val = abs(self.ret["delta_zma20_ma60"][i] - self.ret["delta_zma20_ma60"][position])
                            ma20_max_pos = i
                        if abs(self.ret["delta_zma10_ma60"][i] - self.ret["delta_zma10_ma60"][position]) > ma10_max_val:
                            ma10_max_val = abs(self.ret["delta_zma10_ma60"][i] - self.ret["delta_zma10_ma60"][position])
                            ma10_max_pos = i
                    ma20_curvity = (self.ret["delta_zma20_ma60"][position] - self.ret["delta_zma20_ma60"][ma20_max_pos]) / (position - ma20_max_pos + 1)
                    ma10_curvity = (self.ret["delta_zma10_ma60"][position] - self.ret["delta_zma10_ma60"][ma10_max_pos]) / (position - ma10_max_pos + 1)

#            if status == 0:
#                if self.ret["delta_zma20_ma60"][position - 1] < 0 and self.ret["delta_zma20_ma60"][position] > 0 and self.ret["delta_zma10_ma60"][position] > 12:
#                    cross = 1
#                    status = 1
#                    prod = 1
#                    print("BUY: C " + str(self.ret["time"][position]) + " cross " + str(self.ret["cur"][position]) + " " + str(self.ret["delta_zma10_ma60"][position]) + " " + str(self.ret["delta_zma20_ma60"][position]) + " " + str(ratio_x_f))
#                    buy_position = position
#                if self.ret["delta_zma20_ma60"][position - 1] > 0 and self.ret["delta_zma20_ma60"][position] < 0 and self.ret["delta_zma10_ma60"][position] < -12:
#                    cross = -1
#                    status = 1
#                    prod = -1
#                    print("BUY: P " + str(self.ret["time"][position]) + " cross " + str(self.ret["cur"][position]) + " " + str(self.ret["delta_zma10_ma60"][position]) + " " + str(self.ret["delta_zma20_ma60"][position]) + " " + str(ratio_x_f))
#                    buy_position = position

            if status == 0:
                if zma20_f == 1 and ratio_f == 1:
                    if self.ret["delta_zma20_ma60"][position] > 0 :
                        if (ma10_curvity / ma20_curvity) > 1.25 and ma20_curvity >= 20/1000:
                            prod = 1
                            status = 1
                            print("BUY:" + "C " + str(self.ret["time"][position]) + " " + str(
                                self.ret["cur"][position]) + " " + str(self.ret["delta_zma20_ma60"][position]) + " " + "curvity " + str(ma10_curvity) + " " + str(ma20_curvity) + " " + str(self.ret["zma_gap_ratio"][position]))
                            buy_position = position
                    if self.ret["delta_zma20_ma60"][position] < 0 :
                        if (ma10_curvity / ma20_curvity) > 1.25 and ma20_curvity <= -20/1000:
                            prod = -1
                            status = 1
                            print("BUY:" + "P " + str(self.ret["time"][position]) + " " + str(
                                self.ret["cur"][position]) + " " + str(self.ret["delta_zma20_ma60"][position]) + " " + "curvity " + str(ma10_curvity) + " " + str(ma20_curvity) + " " + str(self.ret["zma_gap_ratio"][position]))
                            buy_position = position

            if status != 0:
                if zma20_f == 0:

                    if zma20_x_f == 1 and ratio_x_f == 1:
                        status = 2
                    else:
                        status = 0
                        print("SELL:" + str(self.ret["time"][position]) + " " + str(self.ret["cur"][position]) + "  " + str(self.ret["ratio"][position]) + " " + str(self.ret["delta_zma10_ma60"][position]) + " " + str(self.ret["delta_zma20_ma60"][position]) + " " + str(ratio_x_f))
                        sell_position = position
                        data.append({"buy_position": buy_position, "sell_position": sell_position, "product": prod})
                        prod = 0

            position += 1
        ret = pd.DataFrame(data, columns=["buy_position", "sell_position", "product"])
        return ret

    def search_biggest(self, start, end, prod):
        max_value = 0
        value = 0
        if prod == 1:
            value = self.zmax(start, end)
        if prod == -1:
            value = self.zmin(start, end)
        print(value)
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
        trade_record = self.detectSignal(10, 1.9)
#        print(trade_record)
        judge_ret = self.judge(trade_record)
        print(judge_ret)

    def store_history(self, start, end):
        ret = self.queryData(start, end)
        if ret == -1:
            print("query fail")
            return -1
        self.parse_data()
        print("Parse ret")
        print(self.ret)
        self.cal_data()
        print("Cal ret")
        print(self.ret)
 #       self.addDayTestData(self.ret)

    def read_history(self,start_time, end_time):
        self.queryDayTestData(start_time, end_time)
        self.parseDayTestData()
        self.count = self.daytestcount


if __name__ == "__main__":
#    Usage
    start_time = "2017-04-27 9:30:00"
    end_time = "2017-04-27 16:00:00"
    test = daytest()
    test.Initialize()
#    test.readData(start_time, end_time)
    test.store_history(start_time, end_time)

#    test.read_history(start_time, end_time)
#    test.daytestFuc()


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