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
        if self.count < len:
            return -1
        for i in range( len - 1, self.count):
            sum = 0
            for j in range(0, len):
                sum += self.ret["cur"][i-j]
            avr = sum/len
            self.ret.iloc[i, 2] = avr
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
        if self.count < len:
            return -1
        for i in range( len - 1, self.count):
            sum = 0
            for j in range(0, len):
                sum += self.ret["cur"][i-j]
            avr = sum/len
            self.ret.iloc[i, 3] = avr
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
        len = 1200
        if self.count < len + 1 + 60:
            return -1
        for i in range(len + 60, self.count):
            sum = 0
            for j in range(0, 60):
                sum += self.ret["delta_zma10"][i-j]
            avr = sum/60
            self.ret.iloc[i, 6] = avr
        return 0

    def cal_delta_zma20_ma60(self):
        len = 2400
        if self.count < len + 1 + 60:
            return -1
        for i in range(len + 60, self.count):
            sum = 0
            for j in range(0, 60):
                sum += self.ret["delta_zma20"][i-j]
            avr = sum/60
            self.ret.iloc[i, 7] = avr
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

    def detectSignal(self):
        start = 2400 + 60 + 1
        position = start
        status = 0
        zma20_f = 0
        zma20_x_f = 0
        ratio_f = 0
        ratio_x_f = 0
        while position < self.count:
            if abs(self.ret["delta_zma20_ma60"][position]) > 10:
                if zma20_f == 0:
                    print("delta_zma20_ma60 start: " + str(position))
                zma20_f = 1
            else:
                if zma20_f == 1:
                    print("delta_zma20_ma60 end: " + str(position))
                zma20_f = 0

            if abs(self.ret["delta_zma20_ma60"][position]) > 8:
                zma20_x_f = 1
            else:
                zma20_x_f = 0

            if self.ret["ratio"][position] > 1.9:
                if ratio_f == 0:
                    print("ratio start: " + str(position))
                ratio_f = 1
            else:
                if ratio_f == 1:
                    print("ratio end: " + str(position))
                ratio_f = 0

            if self.ret["ratio"][position] > 1:
                ratio_x_f = 1
            else:
                ratio_x_f = 0

            if zma20_f == 1 and ratio_f == 1:
                status = 1
                print("BUY:" + str(self.ret["time"][position]) + " " + str(self.ret["cur"][position]))

            if status != 0:
                if zma20_f == 0 and zma20_x_f == 1 and ratio_x_f == 1:
                    status = 2
                    print("KEEP")
                if zma20_f == 0 and (zma20_x_f == 0 or ratio_x_f == 0):
                    print("SELL"+ str(self.ret["time"][position]) + " " + str(self.ret["cur"][position]))

            position += 1


    def daytest(self):
        self.Initialize()
        ret = self.queryData()
        if ret == -1:
            print("query fail")
            return -1

        self.parse_data()
        self.cal_data()
        self.detectSignal()

