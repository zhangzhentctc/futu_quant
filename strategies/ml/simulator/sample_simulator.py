import math
from strategies.ml.data_handler.sample_handler import *

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


##
## Operation of Pointer to Samples
##
class sample_simulator:
    def __init__(self):
        self.point = 0
        self.inspect_bars = 7

        self.ret_data = []

    def prepare_sample_simulator(self):
        self.sample_handler = sample_handler()
        self.sample_handler.prepare_samples()

    def __generate_ret(self):
        ret_data = []
        for i in range(0, self.inspect_bars):
            close = self.sample_handler.samples.iloc[self.point, i * 4 + 2]
            ma5 = self.sample_handler.samples.iloc[self.point, i * 4 + 3]
            ma10 = self.sample_handler.samples.iloc[self.point, i * 4 + 4]
            ma20 = self.sample_handler.samples.iloc[self.point, i * 4 + 5]
            ret_data.append([close, ma5, ma10, ma20])
        self.ret_data = ret_data

    def move_to_id(self, id):
        pos = -1
        for i in range(0, self.sample_handler.length):
            t_id = self.sample_handler.get_sample_id(i)
            if t_id == id:
                pos = i

        if pos < 0 or pos >= self.sample_handler.length:
            return -1
        self.point = pos
        self.__generate_ret()
        return 0

    def get_next_data(self, step = 1):
        if self.point + step < 0 or self.point + step >= self.sample_handler.length:
            return -1
        self.point += step
        self.__generate_ret()
        return 0

    def reset_point(self):
        self.point = 0
        self.__generate_ret()

    def get_ret_data(self):
        return self.ret_data

    def get_sample_id(self):
        return self.sample_handler.get_sample_id(self.point)

    def get_sample_type(self):
        return self.sample_handler.get_sample_type(self.point)

    def get_sample_status(self):
        return self.sample_handler.get_sample_status(self.point)

    def get_sample_comp_cnt(self):
        return self.sample_handler.get_sample_comp_cnt(self.point)
