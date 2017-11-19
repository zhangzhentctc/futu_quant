import math

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

class sample_dayk_comparer:
    def __init__(self, dayk_handler, sample_handler):
        self.point = 19
        self.sample_num = 0
        self.inspect_bars = 7
        self.distance = -1
        self.dayk_handler = dayk_handler
        self.sample_handler = sample_handler

    def init_compare_data(self):
        close_list = self.dayk_handler.day_1ktable.iloc[self.point:self.point + self.inspect_bars, COL_END]
        ma5_list = self.dayk_handler.day_1ktable.iloc[self.point:self.point + self.inspect_bars, COL_MA5]
        ma10_list = self.dayk_handler.day_1ktable.iloc[self.point:self.point + self.inspect_bars, COL_MA10]
        ma20_list = self.dayk_handler.day_1ktable.iloc[self.point:self.point + self.inspect_bars, COL_MA20]
        close_list_min = close_list.min()
        ma5_list_min = ma5_list.min()
        ma10_list_min = ma10_list.min()
        ma20_list_min = ma20_list.min()
        all_min = close_list_min
        if ma5_list_min < all_min:
            all_min = ma5_list_min
        if ma10_list_min < all_min:
            all_min = ma10_list_min
        if ma20_list_min < all_min:
            all_min = ma20_list_min

        self.close_list = close_list - all_min
        self.ma5_list = ma5_list - all_min
        self.ma10_list = ma10_list - all_min
        self.ma20_list = ma20_list - all_min


    def cal_single_distance(self, close_list, ma5_list, ma10_list, ma20_list, inspect_bars=7):
        length = inspect_bars
        sum = 0
        weigh=[0.6, 0.6, 0.8, 1, 1, 4, 4]
        for i in range(0, length):
            index = self.point + i
            tmp = 0
            t = close_list[index] - self.sample_handler.samples.iloc[self.sample_num, i * 4 + 2]
            tmp += t * t * 2
            t = ma5_list[index]   - self.sample_handler.samples.iloc[self.sample_num, i * 4 + 3]
            tmp += t * t
            t = ma10_list[index]  - self.sample_handler.samples.iloc[self.sample_num, i * 4 + 4]
            tmp += t * t
            t = ma20_list[index]  - self.sample_handler.samples.iloc[self.sample_num, i * 4 + 5]
            tmp += t * t

            tmp *= weigh[i]
            sum += tmp
        distance = math.sqrt(sum)
        #self.distance = distance
        return distance


    def cal_best_distance(self):
        close_list = self.close_list.copy()
        ma5_list = self.ma5_list.copy()
        ma10_list = self.ma10_list.copy()
        ma20_list = self.ma20_list.copy()
        distance_min = self.cal_single_distance(close_list, ma5_list, ma10_list, ma20_list)
        self.distance = distance_min
        return


        close_list_max = close_list.max()
        ma5_list_max = ma5_list.max()
        ma10_list_max = ma10_list.max()
        ma20_list_max = ma20_list.max()
        all_max = close_list_max
        if ma5_list_max > all_max:
            all_max = ma5_list_max
        if ma10_list_max > all_max:
            all_max = ma10_list_max
        if ma20_list_max > all_max:
            all_max = ma20_list_max

        if all_max >= 100:
            move_len = 1
        else:
            move_len = int(100 - all_max)


        for i in range(1, move_len):
            close_list += 1
            ma5_list += 1
            ma10_list += 1
            ma20_list += 1
            tmp_distance = self.cal_single_distance(close_list, ma5_list, ma10_list, ma20_list, close_list_fix, ma5_list_fix, ma10_list_fix, ma20_list_fix)
            if tmp_distance < distance_min:
                distance_min = tmp_distance
        self.distance = distance_min


    def get_data(self, step):
        if (self.point + step >= self.dayk_handler.length - self.inspect_bars - 1) or \
            (self.point + step <= 19):
            return
        self.point += step
        i = self.point
        dayk = self.dayk_handler.day_1ktable

        close_list = dayk.iloc[i:i + self.inspect_bars, COL_END]
        ma5_list = dayk.iloc[i:i + self.inspect_bars, COL_MA5]
        ma10_list = dayk.iloc[i:i + self.inspect_bars, COL_MA10]
        ma20_list = dayk.iloc[i:i + self.inspect_bars, COL_MA20]
        close_list_min = close_list.min()
        ma5_list_min = ma5_list.min()
        ma10_list_min = ma10_list.min()
        ma20_list_min = ma20_list.min()
        all_min = close_list_min
        if ma5_list_min < all_min:
            all_min = ma5_list_min
        if ma10_list_min < all_min:
            all_min = ma10_list_min
        if ma20_list_min < all_min:
            all_min = ma20_list_min

        self.close_list = close_list - all_min
        self.ma5_list = ma5_list - all_min
        self.ma10_list = ma10_list - all_min
        self.ma20_list = ma20_list - all_min

        self.cal_best_distance()


    def get_sample(self, step):
        if self.sample_num + step > self.sample_handler.length - 1 or \
            self.sample_num + step < 0:
            return
        self.sample_num += step
        self.cal_best_distance()


    def set_ret(self, ret):
        self.dayk_handler.set_ret(self.point, ret)


    def get_ret(self):
        return self.dayk_handler.get_ret(self.point)
