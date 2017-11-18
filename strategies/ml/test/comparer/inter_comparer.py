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


class inter_comparer:
    def __init__(self, dayk_handler, dayk_handler_fix):
        self.point = 19
        self.point_fix = 19
        self.inspect_bars = 7
        self.distance = -1
        self.dayk_handler = dayk_handler
        self.dayk_handler_fix = dayk_handler_fix

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

        close_list = self.dayk_handler_fix.day_1ktable.iloc[self.point:self.point + self.inspect_bars, COL_END]
        ma5_list = self.dayk_handler_fix.day_1ktable.iloc[self.point:self.point + self.inspect_bars, COL_MA5]
        ma10_list = self.dayk_handler_fix.day_1ktable.iloc[self.point:self.point + self.inspect_bars, COL_MA10]
        ma20_list = self.dayk_handler_fix.day_1ktable.iloc[self.point:self.point + self.inspect_bars, COL_MA20]
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
        self.close_list_fix = close_list - all_min
        self.ma5_list_fix = ma5_list - all_min
        self.ma10_list_fix = ma10_list - all_min
        self.ma20_list_fix = ma20_list - all_min

    def cal_single_distance(self, close_list, ma5_list, ma10_list, ma20_list, close_list_fix, ma5_list_fix, ma10_list_fix, ma20_list_fix, inspect_bars=7):
        length = inspect_bars
        sum = 0
        weigh=[0.6,0.6,0.8,1,1,4,4]
        for i in range(0, length):
            index = self.point + i
            index_fix = self.point_fix + i
            tmp = 0
            tmp += (close_list[index] - close_list_fix[index_fix]) * (close_list[index] - close_list_fix[index_fix]) * 2
            tmp += (ma5_list[index] - ma5_list_fix[index_fix]) * (ma5_list[index] - ma5_list_fix[index_fix])
            tmp += (ma10_list[index] - ma10_list_fix[index_fix]) * (ma10_list[index] - ma10_list_fix[index_fix])
            tmp += (ma20_list[index] - ma20_list_fix[index_fix]) * (ma20_list[index] - ma20_list_fix[index_fix])
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

        close_list_fix = self.close_list_fix.copy()
        ma5_list_fix = self.ma5_list_fix.copy()
        ma10_list_fix = self.ma10_list_fix.copy()
        ma20_list_fix = self.ma20_list_fix.copy()


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

        distance_min = self.cal_single_distance(close_list, ma5_list, ma10_list, ma20_list, close_list_fix, ma5_list_fix, ma10_list_fix, ma20_list_fix)
        self.distance = distance_min
        return
        for i in range(1, move_len):
            close_list += 1
            ma5_list += 1
            ma10_list += 1
            ma20_list += 1
            tmp_distance = self.cal_single_distance(close_list, ma5_list, ma10_list, ma20_list, close_list_fix, ma5_list_fix, ma10_list_fix, ma20_list_fix)
            if tmp_distance < distance_min:
                distance_min = tmp_distance
        self.distance = distance_min

    def get_data(self, step, type=1):
        if type == 0:
            if self.point_fix + step >= self.dayk_handler_fix.length - self.inspect_bars - 1:
                return
            self.point_fix += step
            i = self.point_fix
            dayk = self.dayk_handler_fix.day_1ktable
        else:
            if self.point + step >= self.dayk_handler.length - self.inspect_bars - 1:
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
        if type == 0:
            self.close_list_fix = close_list - all_min
            self.ma5_list_fix = ma5_list - all_min
            self.ma10_list_fix = ma10_list - all_min
            self.ma20_list_fix = ma20_list - all_min
        else:
            self.close_list = close_list - all_min
            self.ma5_list = ma5_list - all_min
            self.ma10_list = ma10_list - all_min
            self.ma20_list = ma20_list - all_min
        #self.cal_single_distance()
        self.cal_best_distance()

    def sudo_move(self, step, type = 1):
        if type == 0:
            if self.point_fix + step >= self.dayk_handler_fix.length - self.inspect_bars - 1:
                return
            self.point_fix += step
            i = self.point_fix
            dayk = self.dayk_handler_fix.day_1ktable
        else:
            if self.point + step >= self.dayk_handler.length - self.inspect_bars - 1:
                return
            self.point += step
            i = self.point
            dayk = self.dayk_handler.day_1ktable

        close_list = dayk.iloc[i + step:i + self.inspect_bars + step, COL_END].copy()
        ma5_list = dayk.iloc[i + step:i + self.inspect_bars + step, COL_MA5].copy()
        ma10_list = dayk.iloc[i + step:i + self.inspect_bars + step, COL_MA10].copy()
        ma20_list = dayk.iloc[i + step:i + self.inspect_bars + step, COL_MA20].copy()
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
        if type == 0:
            self.close_list_fix_show = close_list - all_min
            self.ma5_list_fix_show = ma5_list - all_min
            self.ma10_list_fix_show = ma10_list - all_min
            self.ma20_list_fix_show = ma20_list - all_min
        else:
            self.close_list_show = close_list - all_min
            self.ma5_list_show = ma5_list - all_min
            self.ma10_list_show = ma10_list - all_min
            self.ma20_list_show = ma20_list - all_min

    def move_data(self, pos, type=1):
        if type == 0:
            if pos >= self.dayk_handler_fix.length - self.inspect_bars - 1:
                return
            self.point_fix = pos
            i = self.point_fix
            dayk = self.dayk_handler_fix.day_1ktable
        else:
            if pos >= self.dayk_handler.length - self.inspect_bars - 1:
                return
            self.point = pos
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
        if type == 0:
            self.close_list_fix = close_list - all_min
            self.ma5_list_fix = ma5_list - all_min
            self.ma10_list_fix = ma10_list - all_min
            self.ma20_list_fix = ma20_list - all_min
        else:
            self.close_list = close_list - all_min
            self.ma5_list = ma5_list - all_min
            self.ma10_list = ma10_list - all_min
            self.ma20_list = ma20_list - all_min
        self.cal_best_distance()

    def get_next_good_point(self):
        ret_list = self.dayk_handler_fix.day_1ktable.iloc[:, COL_RET]
        length = len(self.dayk_handler_fix.day_1ktable.index)
        found = 0
        target = 0
        if self.point_fix >= length - self.inspect_bars:
            return -1
        for i in range(self.point, length - self.inspect_bars):
            if ret_list[i] == 6:
                target = i
                found = 1
                break
            else:
                found = 0
        if found == 0:
            print("Good Point Not Found")
            return -1
        else:
            self.get_data(target-self.point_fix,0)
        return 0

    def set_ret(self, ret):
        self.dayk_handler.set_ret(self.point, ret)


    def get_ret(self):
        return self.dayk_handler.get_ret(self.point)
