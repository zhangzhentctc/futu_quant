from db.db_ma_trend import *
from openft.open_quant_context import *


class daytest:
    def __init__(self):
        self.count = 0

    def Initialize(self):
        self.db = MySQLCommand("localhost", 3306, "root", "123456", "trend")
        self.db.connectMysql()
        self.op = dbop_ma_trand()

    def queryData(self):
        self.count = self.op.dbop_read_ma_dur2(self.db, "2017-04-21 9:20:00", "2017-04-21 16:00:00")
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
            data.append({"No.": line[0], "cur": line[3], "time": line[6]})

        self.ret = pd.DataFrame(data, columns=["No.", "cur", "zma10", "zma20", "delta_zma10", "delta_zma20", "delta_zma10_ma60", "delta_zma20_ma60", "ratio", "time"])
        return self.ret

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
        while position < self.count:
            if abs(self.ret["delta_zma20_ma60"][position]) > ma20_shrethold:
   #             if zma20_f == 0:
   #                 print("delta_zma20_ma60 start: " + str(position))
                zma20_f = 1
            else:
 #               if zma20_f == 1:
 #                   print("delta_zma20_ma60 end: " + str(position))
                zma20_f = 0

            if abs(self.ret["delta_zma20_ma60"][position]) > ma20_shrethold * 0.8:
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
                    status = 1
                    if self.ret["delta_zma20_ma60"][position] > 0:
                        prod = 1
                    if self.ret["delta_zma20_ma60"][position] < 0:
                        prod = -1
                    print("BUY:" + str(prod) + str(self.ret["time"][position]) + " " + str(self.ret["cur"][position]) + " " + str(self.ret["delta_zma20_ma60"][position]) + " " + str(self.ret["ratio"][position]))
                    buy_position = position

            if status != 0:
                if zma20_f == 0 and zma20_x_f == 1 and ratio_x_f == 1:
                    status = 2
                if zma20_f == 0 and (zma20_x_f == 0 or ratio_x_f == 0):
                    status = 0

                    print("SELL:" + str(self.ret["time"][position]) + " " + str(self.ret["cur"][position]))
                    sell_position = position
                    data.append({"buy_position": buy_position, "sell_position": sell_position, "product": prod})
                    prod = 0

            position += 1
        ret = pd.DataFrame(data, columns=["buy_position", "sell_position", "product"])
        return ret

    def search_biggest(self, start, end, prod):
        max_value = 0
        if prod == 1:
            for i in (start, end + 1):
                if self.ret["cur"][i] < self.ret["cur"][start]:
                    continue
                if abs(self.ret["cur"][start] - self.ret["cur"][i]) > max_value:
                    max_value = abs(self.ret["cur"][start] - self.ret["cur"][i])
        if prod == -1:
            for i in (start, end + 1):
                if self.ret["cur"][i] > self.ret["cur"][start]:
                    continue
                if abs(self.ret["cur"][start] - self.ret["cur"][i]) > max_value:
                    max_value = abs(self.ret["cur"][start] - self.ret["cur"][i])
        return max_value

    def judge(self, trade_recorde):
        len = 0
        ret = []
        for index in trade_recorde.iterrows():
            len += 1

        for i in range(0, len):
            start = trade_recorde.iloc[i, 0]
            end = trade_recorde.iloc[i, 1]
            prod = trade_recorde.iloc[i, 2]
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

