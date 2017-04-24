from db.db_ma_trend import *
#from openft.open_quant_context import *
import pandas as pd

class daytest:
    def __init__(self):
        self.count = 0

    def Initialize(self):
        self.db = MySQLCommand("localhost", 3306, "root", "123456", "trend2")
        self.db.connectMysql()
        self.op = dbop_ma_trand()

    def queryData(self):
        self.count = self.op.dbop_read_ma_dur2(self.db, "2017-04-24 9:30:00", "2017-04-24 16:00:00")
        if self.count == 0:
            return -1
        return self.count

    def getNextData(self):
        ret = self.op.dbop_read_ma_dur_next(self.db)
        return ret

    def parse_data(self):
        data = []
        for i in range(0, self.count):
            line = self.getNextData()
            data.append({"No.": line[0], "cur": line[3], "time": line[8]})

        self.ret = pd.DataFrame(data, columns=["No.", "cur", "zma10", "zma20", "delta_zma10", "delta_zma20", "delta_zma10_ma60", "delta_zma20_ma60", "ratio",  "delta_delta_zma20_ma60", "time"])
        return self.ret

    def cal_delta_delta_zma20_ma60(self):
        start_pos = 2461
        if self.count < start_pos + 1:
            return -1
        for i in range(start_pos, self.count):
            val = self.ret["delta_zma20_ma60"][i] - self.ret["delta_zma20_ma60"][i-1]
            val *= 1000
            self.ret.iloc[i, 9] = val
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

    def cal_data(self):
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
        print("cal_delta_delta_zma20_ma60")
        self.cal_delta_delta_zma20_ma60()

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
        print(self.ret)
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
                                self.ret["cur"][position]) + " " + str(self.ret["delta_zma20_ma60"][position]) + " " + "curvity " + str(ma10_curvity) + " " + str(ma20_curvity))
                            buy_position = position
                    if self.ret["delta_zma20_ma60"][position] < 0 :
                        if (ma10_curvity / ma20_curvity) > 1.25 and ma20_curvity <= -20/1000:
                            prod = -1
                            status = 1
                            print("BUY:" + "P " + str(self.ret["time"][position]) + " " + str(
                            self.ret["cur"][position]) + " " + str(self.ret["delta_zma20_ma60"][position]) + " " + "curvity " + str(ma10_curvity) + " " + str(ma20_curvity))
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

    def daytest(self):
        self.Initialize()
        ret = self.queryData()
        if ret == -1:
            print("query fail")
            return -1

        self.parse_data()
        self.cal_data()
        trade_record = self.detectSignal(10, 1.9)
#        print(trade_record)
        judge_ret = self.judge(trade_record)
        print(judge_ret)

if __name__ == "__main__":
#    Usage
    test = daytest()
    test.daytest()



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

"""
            if status == 0:
                ##
                # Calculate y = ax + b
                ##
                t = 240
                A = 0
                B = 0
                C = 0
                D = 0
                for i in range(position - t + 1, position + 1):
                    A += i * i
                    B += i
                    C += i * self.ret["delta_zma20_ma60"][i]
                    D += self.ret["delta_zma20_ma60"][i]

                curvity = (C * t - D * B)/ (A * t - B * B)
"""