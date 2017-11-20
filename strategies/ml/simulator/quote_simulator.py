import math
from strategies.ml.data_handler.dayk_handler import *

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

class quote_simulator:
    def __init__(self, date):
        self.point = 19
        self.inspect_bars = 7
        self.date = date
        self.ret_data = []

    def __init_dayk_data(self):
        self.dayk_handler = dayk_handler(self.date)
        self.dayk_handler.prepare_dayk()
        self.dayk_handler.reset_ret()

    def __generate_ret(self):
        ret_data = []
        for i in range(0, self.inspect_bars):
            close_val = self.dayk_handler.day_1ktable.iloc[self.point + i, COL_END]
            ma5_val = self.dayk_handler.day_1ktable.iloc[self.point + i, COL_MA5]
            ma10_val = self.dayk_handler.day_1ktable.iloc[self.point + i, COL_MA10]
            ma20_val = self.dayk_handler.day_1ktable.iloc[self.point + i, COL_MA20]
            ret_data.append([close_val, ma5_val, ma10_val, ma20_val])
        self.ret_data = ret_data

    def prepare_quote_simulator(self):
        self.__init_dayk_data()
        self.__generate_ret()

    def get_next_data(self, step = 1):
        if self.point + step < 0 or self.point + step + self.inspect_bars >= self.dayk_handler.length:
            return -1
        self.point += step
        self.__generate_ret()
        return 0

    def reset_point(self):
        self.point = 19
        self.__generate_ret()
        return 0

    def get_point(self):
        return self.point

    def get_ret_data(self):
        return self.ret_data

    def get_simulator_date(self):
        return self.date

    def get_simulator_dayk_num(self):
        return self.point

    def set_distance(self, distance):
        self.dayk_handler.set_ret(self.point, distance)
