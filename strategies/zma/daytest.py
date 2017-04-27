from db.db_ma_trend import *
#from openft.open_quant_context import *
import pandas as pd
import time

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

#    data["No."], data["cur"], data["zma10"], data["zma20"], data["delta_zma10"], data["delta_zma20"], data["delta_zma10_ma60"], data["delta_zma20_ma60"], data["ratio"], data["delta_delta_zma20_ma60"], data["time"]
    def addDayTestData(self, data):
        len = 0
        for index in data.iterrows():
            len += 1
        for i in range(0, len):
            self.myop.dbop_add_day_data(self.mydb, data["No."][i], data["cur"][i], data["time"][i], data["zma10"][i], data["zma20"][i], \
                                   data["delta_zma10"][i], data["delta_zma20"][i], data["delta_zma10_ma60"][i], data["delta_zma20_ma60"][i], data["ratio"][i], data["zma_gap"][i], data["zma_gap_ratio"][i], data["delta_zma20_ma60_ratio"][i], data["zma10_ratio"][i], data["zma20_ratio"][i],data["zma20_ratio_ratio"][i])


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
            data.append({"No.": line[0], "cur": line[1], "zma10":line[3], "zma20":line[4], "delta_zma10":line[5], "delta_zma20":line[6], "delta_zma10_ma60":line[7], "delta_zma20_ma60":line[8], "ratio":line[9],  "zma_gap":line[10], "zma_gap_ratio":line[11],"time": line[2], "delta_zma20_ma60_ratio": line[12], "zma10_ratio": line[13], "zma20_ratio": line[14], "zma20_ratio_ratio": line[15]})

        self.ret = pd.DataFrame(data, columns=["No.", "cur", "zma10", "zma20", "delta_zma10", "delta_zma20", "delta_zma10_ma60", "delta_zma20_ma60", "ratio",  "zma_gap", "zma_gap_ratio", "time", "delta_zma20_ma60_ratio", "zma10_ratio", "zma20_ratio", "zma20_ratio_ratio"])
        return self.ret

    def queryData(self, start = "2017-04-24 9:30:00", end = "2017-04-24 16:00:00"):
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
            if line[3] == 0:
                data.append({"No.": line[0], "cur": pre_cur, "time": line[8]})
            else:
                data.append({"No.": line[0], "cur": line[3], "time": line[8]})
            pre_cur =line[3]
        self.ret = pd.DataFrame(data, columns=["No.", "cur", "zma10", "zma20", "delta_zma10", "delta_zma20", "delta_zma10_ma60", "delta_zma20_ma60", "ratio",  "zma_gap", "zma_gap_ratio", "time", "delta_zma20_ma60_ratio", "zma10_ratio", "zma20_ratio", "zma20_ratio_ratio"])
        return self.ret

## Conduct 4t times calculation
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

    def simple_ratio(self, start, end, column):
        if self.count < start:
            return -1, 0
        ratio = (self.ret[column][end] - self.ret[column][start])/(end - start)
        return 1, ratio

    def cal_zma10(self):
        len = 1200
        sum = 0
        start_pos = len - 1
        if self.count < len:
            return -1
        for j in range(0, len):
            sum += self.ret["cur"][len - 1 - j]
        avr0 = sum / len
        self.ret.iloc[start_pos, 2] = avr0
        starter = self.ret["cur"][0]
        for i in range(start_pos + 1, self.count):
            avr = avr0 - starter/len + self.ret["cur"][i]/len
            self.ret.iloc[i, 2] = avr
            avr0 = avr
            starter = self.ret["cur"][i - len]
        return 0

    def cal_delta_zma10(self):
        len = 1200
        if self.count < len + 1:
            return -1
        for i in range(len, self.count):
            delta = self.ret["zma10"][i] - self.ret["zma10"][i-1]
            delta *= 1000
            self.ret.iloc[i, 4] = delta
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
        self.ret.iloc[start_pos, 3] = avr0
        starter = self.ret["cur"][0]
        for i in range(start_pos + 1, self.count):
            avr = avr0 - starter/len + self.ret["cur"][i]/len
            self.ret.iloc[i, 3] = avr
            avr0 = avr
            starter = self.ret["cur"][i - len]
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

    def cal_zma_gap(self):
        len = 2400
        start_pos = len
        if self.count < start_pos + 1:
            return -1
        for i in range(start_pos, self.count):
            val = self.ret["zma10"][i] - self.ret["zma20"][i]
            self.ret.iloc[i, 9] = val
        return 1

    def cal_zma_gap_ratio(self):
        len = 2400
        t = 240
        start_pos = len + t
        if self.count < start_pos:
            return -1
        for i in range(start_pos, self.count):
#        for i in range(7900, 7901):
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
            self.ret.iloc[i, 10] = float(val)
        return 1


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

    def cal_zma10_ratio(self):
        len = 1200
        t = 60
        val =0
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            ret, val = self.least_square_method(i - t + 1, i, "zma10")
            if ret == -1:
                val = 0
            self.ret.iloc[i, 13] = val
        return 1

    def cal_zma20_ratio(self):
        len = 2400
        t = 60
        val =0
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            ret, val = self.least_square_method(i - t + 1, i, "zma20")
            if ret == -1:
                val = 0
            self.ret.iloc[i, 14] = val
        return 1

    def cal_zma20_ratio_ratio(self):
        len = 2400
        t = 240
        val =0
        start_pos = len + t
        if self.count < start_pos:
          return -1
        for i in range(start_pos, self.count):
            ret, val = self.least_square_method(i - t + 1, i, "zma20_ratio")
            if ret == -1:
                val = 0
            self.ret.iloc[i, 15] = val
        return 1

    def cal_data(self):
        start_time = time.time()
        print("cal_zma10")
        self.cal_zma10()
        print("cal_zma20")
        self.cal_zma20()
        print("cal_delta_zma10")
        self.cal_delta_zma10()
        print("cal_delta_zma20")
        self.cal_delta_zma20()
        print("cal_delta_zma10_ma60")
        self.cal_delta_zma10_ma60()
        print("cal_delta_zma20_ma60")
        self.cal_delta_zma20_ma60()
        print("cal_ratio")
        self.cal_ratio()
        print("cal_zma_gap")
        self.cal_zma_gap()
        print("cal_zma_gap_ratio")
        self.cal_zma_gap_ratio()
        print("delta_zma20_ma60_ratio")
        self.cal_delta_zma20_ma60_ratio()
        self.cal_zma10_ratio()
        self.cal_zma20_ratio()
        self.cal_zma20_ratio_ratio()
        end_time = time.time()
        print("start from: " + str(start_time) + " to: " + str(end_time))

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
        self.addDayTestData(self.ret)

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