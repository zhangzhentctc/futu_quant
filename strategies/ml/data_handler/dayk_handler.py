from db.db_ml import *
import pandas as pd

filename_prefix = "/Users/aaron/finance/dayk/dayk_"
filename_postfix = ".csv"

COL_CODE = 0
COL_TIME = 1
COL_START = 2
COL_END = 3
COL_HIGH = 4
COL_LOW = 5
COL_VOL = 6
COL_TURN = 7
COL_MA5 = 8
COL_MA10 = 9
COL_MA20 = 10
COL_RET = 11
COL_DAY = 12
COL_NUM = 13


class dayk_handler:
    def __init__(self, date):
        self.count = 0
        self.daytestcount = 0
        self.tmp = 0
        self.trend_c_cnt = 0
        self.trend = 0
        self.trend_p_cnt = 0
        self.data = []
        self.date = date

        self.distance = -1
        self.inspect_bars = 7

    def init_db(self):
        self.db = MySQLCommand("localhost", 3306, "root", "123456", "ml_k_analysis")
        self.db.connectMysql()
        self.dbop = db_ml()


    def import_dayk2db(self, date):

        file_full_path = filename_prefix + date + filename_postfix
        day_1ktable = pd.read_csv(file_full_path)
        day_1ktable['ma5']= 0
        day_1ktable['ma10'] = 0
        day_1ktable['ma20'] = 0
        day_1ktable['ret'] = 0

        day_1ktable = self.cal_MAn(5, day_1ktable)
        day_1ktable = self.cal_MAn(10, day_1ktable)
        day_1ktable = self.cal_MAn(20, day_1ktable)
        length = len(day_1ktable.index)

        count = self.dbop.dbop_get_day_data(self.db, date)
        if count != 0:
            print("Day Data Alreay Imported: ", date)
            return -1

        self.dbop.dbop_agancy_begin(self.db)
        ret = 0
        for i in range(0, length - 1):
            ret = self.dbop.dbop_insert_raw_data(self.db,
                                           day_1ktable["open"][i], day_1ktable["close"][i],day_1ktable["high"][i],day_1ktable["low"][i],
                                           day_1ktable["ma5"][i],day_1ktable["ma10"][i],day_1ktable["ma20"][i],
                                           ret, date, i)
            if ret == -1:
                break

        if ret == -1:
            self.dbop.dbop_agancy_rollback(self.db)
            print("Insert Error")
        else:
            self.dbop.dbop_agancy_commit(self.db)
            print("Insert OK")

        return


    def import_dayk_from_DB(self, date):
        self.date = date
        count = self.dbop.dbop_get_day_data(self.db, date)
        if count == 0:
            print("Day Data Does Not Exist: ", date)
            return -1
        data = []
        for i in range(0, count):
            line = self.dbop.dbop_get_day_data_next(self.db)
            data.append({
                "code":"HK_FUTURE.999010", "time_key":"",
                "open":line[3], "close":line[4], "high":line[5], "low":line[6],
                "volume":0, "turnover":0,
                "ma5":line[7],"ma10":line[8],"ma20":line[9],"ret":line[10],
                "day":line[1], "num":line[2]
            })

        self.day_1ktable = pd.DataFrame(data, columns=["code","time_key",
                                                       "open","close","high","low","volume","turnover",
                                                       "ma5","ma10","ma20","ret",
                                                       "day","num"])

        self.length = len(self.day_1ktable.index)
        return

    def del_head_data(self):
        for i in range(0,20):
            self.day_1ktable.drop(i,inplace=True)

    def init_data_from_file(self, filename):
        self.day_1ktable = pd.read_csv(filename)
        self.day_1ktable['ma5']= 0
        self.day_1ktable['ma10'] = 0
        self.day_1ktable['ma20'] = 0
        self.day_1ktable['ret'] = 0
        self.day_1ktable['day'] = 0
        self.day_1ktable['num'] = 0
        self.cal_MAn(5, self.day_1ktable)
        self.cal_MAn(10, self.day_1ktable)
        self.cal_MAn(20, self.day_1ktable)


    def cal_MAn(self, n, day_1ktable):
        if n == 5:
            ncolum = COL_MA5
        elif n == 10:
            ncolum = COL_MA10
        elif n == 20:
            ncolum = COL_MA20
        else:
            return -1

        length = len(day_1ktable.index)
        for i in range(n - 1, length):
            tmp = 0
            for j in range(0, n):
                tmp += day_1ktable.iloc[i - j, COL_END]
            ma_n = tmp / n
            ma_n = round(ma_n, 2)
            day_1ktable.iloc[i, ncolum] = ma_n
        return day_1ktable

    def set_ret(self, pos, ret):
        self.day_1ktable.iloc[pos, COL_RET] = ret
        num = self.day_1ktable.iloc[pos, COL_NUM]
        self.dbop.dbop_update_day_data_trade_mark(self.db,ret,self.date,num)

    def get_ret(self, pos):
        return self.day_1ktable.iloc[pos, COL_RET]

    def reset_ret(self):
        for pos in range(0, self.length):
            self.day_1ktable.iloc[pos, COL_RET] = 0
            num = self.day_1ktable.iloc[pos, COL_NUM]
            self.dbop.dbop_update_day_data_trade_mark(self.db, 0, self.date, num)

    def prepare_dayk(self):
        self.init_db()
        self.import_dayk_from_DB(self.date)