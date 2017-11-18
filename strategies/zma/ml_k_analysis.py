from db.db_ml import *
#from openft.open_quant_context import *
import pandas as pd
import time
import math
import os
#from ui.ui_ml import *
from strategies.zma.feature_data_pkg import *


import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *

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

filename_prefix = "/Users/aaron/finance/dayk/dayk_"
filename_postfix = ".csv"


class dayk_handler:
    def __init__(self):
        self.count = 0
        self.daytestcount = 0
        self.tmp = 0
        self.trend_c_cnt = 0
        self.trend = 0
        self.trend_p_cnt = 0
        self.data = []

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





class sample_comparer:
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




class whatthefuck:
    def __init__(self):
        self.cnt = 0
        self.string = ""

    def add_x(self, x):
        self.cnt += x

    def assign(self, val):
        self.cnt = val

##############################################################

def get_dataset(data_handler, plot, step, type = 1):
    plot.clear()
    if type == 0:
        data_handler.get_data(step, 0)
        plot.plot(data_handler.close_list_fix)
        plot.plot(data_handler.ma5_list_fix)
        plot.plot(data_handler.ma10_list_fix)
        plot.plot(data_handler.ma20_list_fix)
    else:
        data_handler.get_data(step)
        plot.plot(data_handler.close_list)
        plot.plot(data_handler.ma5_list)
        plot.plot(data_handler.ma10_list)
        plot.plot(data_handler.ma20_list)
    plot.set_ylim(0, 100)
    canvs.draw()


def get_ret(data_handler):
    print(data_handler.get_ret())
    return data_handler.get_ret()


def set_ret_start_up(data_handler):
    data_handler.set_ret(6)

def set_ret_other(data_handler):
    data_handler.set_ret(-1)

def refresh_text(text, data_handler):
    ret = data_handler.get_ret()
    distance = data_handler.distance
    string = "Judge Result: " + str(ret) + "\nDistance: " + str(distance)
    text.delete(1.0, 'end')
    text.insert('end', string)
    text.after(100, refresh_text, text, data_handler)

def refresh_text2(text, data_handler):
    ret = data_handler.get_ret()
    string = "Judge Result: " + str(ret)
    text.delete(1.0, 'end')
    text.insert('end', string)
    text.after(100, refresh_text, text, data_handler)

distance_t = 30
def auto_test_sample():
    date_list = ["20171019", "20171020", "20171115", "20171116","20171117"]
    test_ret = []
    samp_h = sample_handler()
    samp_h.init_db()
    samp_h.import_samples_from_db()
    samp_h.translation_samples()
    wtf = whatthefuck()
    wtf2 = whatthefuck()
    for date in date_list:
        dayk = dayk_handler()
        dayk.init_db()
        dayk.import_dayk_from_DB(date)
        sp_comp = sample_comparer(dayk, samp_h)
        sp_comp.init_compare_data()
        sp_comp.get_sample(2)

        for i in range(0, samp_h.length):
            for j in range(19, dayk.length - sp_comp.inspect_bars):
                sp_comp.get_data(1)
                if sp_comp.distance < distance_t:
                    sp_comp.set_ret(distance_t)
                    print("set: ",date, " num:", sp_comp.point)
                    test_ret.append([date, sp_comp.point, sp_comp.distance, 0, 0])
            sp_comp.get_sample(1)
    print(test_ret)
    root = Tk()
    f = Figure(figsize=(5,4),dpi=100)
    all_plot = f.add_subplot(211)
    f_plot = f.add_subplot(212)
    canvs = FigureCanvasTkAgg(f, root)
    canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    Button(root, text='BigNext->', command=lambda: show_big_dia(canvs, all_plot, date_list, wtf2, 1)).pack()
    Button(root, text='<-BigBack', command=lambda: show_big_dia(canvs, all_plot, date_list, wtf2, -1)).pack()
    Button(root, text='Next->', command=lambda: show_result(canvs, f_plot, test_ret, wtf, 1)).pack()
    Button(root, text='<-Back', command=lambda: show_result(canvs, f_plot, test_ret, wtf, -1)).pack()
    mytext = Text(root, width=50, height = 5)
    mytext.pack()
    refresh_ret_text(mytext, wtf)
    root.mainloop()






def auto_test():
    wtf = whatthefuck()
    wtf2 = whatthefuck()
    date_list =["20171019","20171020","20171115"]
    test_ret = []
    #date_list = []
    for date_fix in date_list:
        dayk_fix = dayk_handler()
        dayk_fix.init_db()
        dayk_fix.import_dayk_from_DB(date_fix)
        for date in date_list:

            dayk = dayk_handler()
            dayk.init_db()
            dayk.import_dayk_from_DB(date)
            comp = inter_comparer(dayk, dayk_fix)
            comp.init_compare_data()
            ret = comp.get_next_good_point()
            if ret == -1:
                break
            for i in range(19, dayk.length - comp.inspect_bars):
                comp.get_data(1)
                if comp.distance < 30:

                    test_ret.append([date, comp.point, comp.distance, date_fix, comp.point_fix])


    print(test_ret)
    #test_ret = [['20171019', 31, 42.376573717092406, '20171019', 37], ['20171019', 32, 35.60351106281737, '20171019', 37], ['20171019', 33, 37.470521747102296, '20171019', 37], ['20171019', 34, 34.47146646140811, '20171019', 37], ['20171019', 35, 33.692254302732096, '20171019', 37], ['20171019', 36, 25.62108506679567, '20171019', 37], ['20171019', 37, 0.0, '20171019', 37], ['20171019', 38, 25.377194486388795, '20171019', 37], ['20171019', 39, 34.31364160213916, '20171019', 37], ['20171019', 40, 38.04902101237399, '20171019', 37], ['20171019', 41, 32.46709103076541, '20171019', 37], ['20171019', 42, 43.94036868302291, '20171019', 37], ['20171019', 49, 47.916990723546036, '20171019', 37], ['20171019', 50, 39.12541373583203, '20171019', 37], ['20171019', 51, 46.05466317323361, '20171019', 37], ['20171019', 54, 48.64502030012827, '20171019', 37], ['20171019', 55, 38.39546848262064, '20171019', 37], ['20171019', 56, 34.657207042691155, '20171019', 37], ['20171019', 57, 36.606065071242796, '20171019', 37], ['20171019', 58, 42.91834106765973, '20171019', 37], ['20171019', 59, 48.64362239800876, '20171019', 37], ['20171019', 73, 48.79834013570645, '20171019', 37], ['20171019', 74, 39.74448389399645, '20171019', 37], ['20171019', 75, 44.22221161362339, '20171019', 37], ['20171019', 83, 39.578605331667745, '20171019', 37], ['20171019', 84, 32.519870848451404, '20171019', 37], ['20171019', 85, 30.317090889463575, '20171019', 37], ['20171019', 86, 24.126126916685518, '20171019', 37], ['20171019', 87, 22.511863539032152, '20171019', 37], ['20171019', 88, 23.136032503434954, '20171019', 37], ['20171019', 89, 24.66576574931325, '20171019', 37], ['20171019', 90, 28.671658480109592, '20171019', 37], ['20171019', 91, 29.2863449409445, '20171019', 37], ['20171019', 92, 28.050739740692244, '20171019', 37], ['20171019', 93, 28.543090232138194, '20171019', 37], ['20171019', 94, 24.03959234263172, '20171019', 37], ['20171019', 95, 27.618942774840743, '20171019', 37], ['20171019', 96, 33.86916001320303, '20171019', 37], ['20171019', 97, 36.119330004858966, '20171019', 37], ['20171019', 98, 32.14218411993747, '20171019', 37], ['20171019', 99, 26.54968926371706, '20171019', 37], ['20171019', 100, 33.676757563635, '20171019', 37], ['20171019', 101, 41.10374678785219, '20171019', 37], ['20171019', 102, 42.05011296060849, '20171019', 37], ['20171019', 103, 35.993638326792535, '20171019', 37], ['20171019', 104, 32.24710839749722, '20171019', 37], ['20171019', 105, 31.531349479524582, '20171019', 37], ['20171019', 106, 32.74458733897742, '20171019', 37], ['20171019', 107, 34.01878892611948, '20171019', 37], ['20171019', 108, 31.538547842280693, '20171019', 37], ['20171019', 109, 22.63961130408163, '20171019', 37], ['20171019', 110, 23.153444668124834, '20171019', 37], ['20171019', 111, 26.01960799089666, '20171019', 37], ['20171019', 112, 25.097689136650413, '20171019', 37], ['20171019', 113, 18.689462271557787, '20171019', 37], ['20171019', 114, 36.75219721322886, '20171019', 37], ['20171019', 124, 49.42849380670829, '20171019', 37], ['20171019', 125, 41.42832364457798, '20171019', 37], ['20171019', 126, 36.1723651424678, '20171019', 37], ['20171019', 127, 33.345404480978054, '20171019', 37], ['20171019', 128, 29.34160868118951, '20171019', 37], ['20171019', 129, 31.913821457168783, '20171019', 37], ['20171019', 130, 30.3701168914447, '20171019', 37], ['20171019', 131, 25.00591929923847, '20171019', 37], ['20171019', 132, 18.7643811515326, '20171019', 37], ['20171019', 133, 15.970284906662956, '20171019', 37], ['20171019', 134, 18.022596927190715, '20171019', 37], ['20171019', 135, 28.895051479448927, '20171019', 37], ['20171019', 136, 32.635869836730045, '20171019', 37], ['20171019', 137, 27.596630229069838, '20171019', 37], ['20171019', 138, 30.658147367380316, '20171019', 37], ['20171019', 139, 38.66830743645218, '20171019', 37], ['20171019', 140, 38.347803066147385, '20171019', 37], ['20171019', 141, 34.80675221849872, '20171019', 37], ['20171019', 142, 37.9027175806692, '20171019', 37], ['20171019', 143, 45.3195984095195, '20171019', 37], ['20171019', 144, 44.756317989754656, '20171019', 37], ['20171019', 145, 38.37616447744666, '20171019', 37], ['20171019', 146, 29.852135601997283, '20171019', 37], ['20171019', 147, 28.14380926598189, '20171019', 37], ['20171019', 148, 25.053702321214576, '20171019', 37], ['20171019', 149, 27.894515589988234, '20171019', 37], ['20171019', 150, 24.640373373794766, '20171019', 37], ['20171019', 151, 27.574082033677747, '20171019', 37], ['20171019', 152, 22.50946467599767, '20171019', 37], ['20171019', 153, 14.439598332363548, '20171019', 37], ['20171019', 154, 19.35747917472674, '20171019', 37], ['20171019', 155, 24.287939393863052, '20171019', 37], ['20171019', 156, 26.608570048011998, '20171019', 37], ['20171019', 157, 25.37222891272991, '20171019', 37], ['20171019', 158, 24.317606790142207, '20171019', 37], ['20171019', 159, 22.518570114462143, '20171019', 37], ['20171019', 160, 16.99311625335268, '20171019', 37], ['20171019', 161, 17.199360453224322, '20171019', 37], ['20171019', 162, 21.40630748167365, '20171019', 37], ['20171019', 163, 23.261040389457314, '20171019', 37], ['20171019', 164, 20.709659581943857, '20171019', 37], ['20171019', 165, 29.905183497180413, '20171019', 37], ['20171019', 166, 35.47703482536313, '20171019', 37], ['20171019', 167, 31.729607624425476, '20171019', 37], ['20171019', 168, 29.839772117091776, '20171019', 37], ['20171019', 169, 33.399640716629314, '20171019', 37], ['20171019', 175, 47.64890345013104, '20171019', 37], ['20171019', 178, 49.4215944704329, '20171019', 37], ['20171019', 179, 42.06887210277871, '20171019', 37], ['20171019', 180, 43.662638491048945, '20171019', 37], ['20171019', 181, 41.74204115756696, '20171019', 37], ['20171019', 182, 37.30168896980454, '20171019', 37], ['20171019', 183, 28.003642620202367, '20171019', 37], ['20171019', 184, 28.37565858266613, '20171019', 37], ['20171019', 185, 25.231884590732122, '20171019', 37], ['20171019', 186, 25.347465356521166, '20171019', 37], ['20171019', 187, 15.958132722848442, '20171019', 37], ['20171019', 188, 14.495723507296926, '20171019', 37], ['20171019', 189, 20.810670339996406, '20171019', 37], ['20171019', 190, 26.38992231894606, '20171019', 37], ['20171019', 191, 29.53695989772855, '20171019', 37], ['20171019', 192, 24.44344492906001, '20171019', 37], ['20171019', 193, 17.811569273929265, '20171019', 37], ['20171019', 194, 16.673751827347463, '20171019', 37], ['20171019', 195, 21.9708898317747, '20171019', 37], ['20171019', 196, 24.97054264528453, '20171019', 37], ['20171019', 197, 20.58412009292586, '20171019', 37], ['20171019', 198, 20.471541221900637, '20171019', 37], ['20171019', 199, 23.8956062906979, '20171019', 37], ['20171019', 200, 27.424004084013358, '20171019', 37], ['20171019', 201, 28.568829167468, '20171019', 37], ['20171019', 202, 24.519910277160463, '20171019', 37], ['20171019', 203, 18.57928954508283, '20171019', 37], ['20171019', 204, 21.065896610399502, '20171019', 37], ['20171019', 205, 24.083978076722264, '20171019', 37], ['20171019', 206, 30.65243872842719, '20171019', 37], ['20171019', 207, 28.67165848010817, '20171019', 37], ['20171019', 208, 28.07757112002316, '20171019', 37], ['20171019', 209, 26.246447378645232, '20171019', 37], ['20171019', 210, 24.476069945969964, '20171019', 37], ['20171019', 211, 26.499622638822444, '20171019', 37], ['20171019', 212, 22.66764213587293, '20171019', 37], ['20171019', 213, 23.76808784904641, '20171019', 37], ['20171019', 214, 23.035407528410705, '20171019', 37], ['20171019', 215, 20.99371334471295, '20171019', 37], ['20171019', 216, 25.22264855244054, '20171019', 37], ['20171019', 217, 29.786775589176234, '20171019', 37], ['20171019', 218, 28.48066010470877, '20171019', 37], ['20171019', 219, 25.77700525662303, '20171019', 37], ['20171019', 220, 22.67831563410213, '20171019', 37], ['20171019', 221, 23.923001483927898, '20171019', 37], ['20171019', 222, 21.592498697464908, '20171019', 37], ['20171019', 223, 18.42731667932189, '20171019', 37], ['20171019', 224, 23.41751481263544, '20171019', 37], ['20171019', 225, 29.474667088874213, '20171019', 37], ['20171019', 226, 30.368898564155693, '20171019', 37], ['20171019', 227, 28.410526218287128, '20171019', 37], ['20171019', 228, 31.21909671979633, '20171019', 37], ['20171019', 229, 33.3358065749128, '20171019', 37], ['20171019', 233, 44.18875422548155, '20171019', 37], ['20171019', 234, 40.951752099268646, '20171019', 37], ['20171019', 235, 38.275788692069426, '20171019', 37], ['20171019', 236, 42.63784703757904, '20171019', 37], ['20171019', 237, 47.565386574693115, '20171019', 37], ['20171019', 245, 35.68865365911126, '20171019', 37], ['20171019', 246, 33.53842572333999, '20171019', 37], ['20171019', 247, 34.44430286709248, '20171019', 37], ['20171019', 248, 39.088131190938036, '20171019', 37], ['20171020', 50, 42.544306317059124, '20171019', 37], ['20171020', 61, 35.20641986911104, '20171019', 37], ['20171020', 62, 41.31387176240008, '20171019', 37], ['20171020', 63, 40.06789238280565, '20171019', 37], ['20171020', 64, 42.05479758600666, '20171019', 37], ['20171020', 65, 41.22249385954227, '20171019', 37], ['20171020', 66, 44.94271909887012, '20171019', 37], ['20171020', 74, 45.559214216225676, '20171019', 37], ['20171020', 75, 42.452585315855124, '20171019', 37], ['20171020', 76, 39.848136719300385, '20171019', 37], ['20171020', 77, 43.54016536486927, '20171019', 37], ['20171020', 78, 21.140340583823928, '20171019', 37], ['20171020', 79, 22.447538840595985, '20171019', 37], ['20171020', 80, 25.268913708350595, '20171019', 37], ['20171020', 81, 40.19081984732431, '20171019', 37], ['20171020', 82, 42.34295691139152, '20171019', 37], ['20171020', 83, 44.0936730155257, '20171019', 37], ['20171020', 90, 45.55519728856409, '20171019', 37], ['20171020', 91, 40.431349223095566, '20171019', 37], ['20171020', 99, 32.42073410643003, '20171019', 37], ['20171020', 100, 36.410355669779406, '20171019', 37], ['20171020', 101, 38.981021023054915, '20171019', 37], ['20171020', 102, 34.01173326956367, '20171019', 37], ['20171020', 103, 24.410120851810596, '20171019', 37], ['20171020', 104, 19.474085344374906, '20171019', 37], ['20171020', 105, 19.81191560652282, '20171019', 37], ['20171020', 106, 26.300038022785916, '20171019', 37], ['20171020', 107, 34.64909811236048, '20171019', 37], ['20171020', 108, 32.04200368266626, '20171019', 37], ['20171020', 109, 22.412764220416843, '20171019', 37], ['20171020', 110, 22.686339501999846, '20171019', 37], ['20171020', 111, 22.27253914577298, '20171019', 37], ['20171020', 112, 17.451074465486858, '20171019', 37], ['20171020', 113, 21.853146226573557, '20171019', 37], ['20171020', 114, 24.93443402205, '20171019', 37], ['20171020', 115, 21.00076189094133, '20171019', 37], ['20171020', 116, 20.99252247825489, '20171019', 37], ['20171020', 117, 26.69898874489492, '20171019', 37], ['20171020', 118, 30.388978265154662, '20171019', 37], ['20171020', 119, 25.5397729042374, '20171019', 37], ['20171020', 120, 24.40536826192205, '20171019', 37], ['20171020', 121, 30.964140549998138, '20171019', 37], ['20171020', 122, 41.29292917679602, '20171019', 37], ['20171020', 129, 48.25913385050043, '20171019', 37], ['20171020', 130, 42.56451573787548, '20171019', 37], ['20171020', 131, 37.44470590083591, '20171019', 37], ['20171020', 132, 35.47556905815742, '20171019', 37], ['20171020', 133, 29.489828755013544, '20171019', 37], ['20171020', 134, 28.971779372350127, '20171019', 37], ['20171020', 135, 35.993471630281654, '20171019', 37], ['20171020', 136, 46.16477011748386, '20171019', 37], ['20171020', 140, 49.53980217965948, '20171019', 37], ['20171020', 141, 44.7587756758416, '20171019', 37], ['20171020', 142, 37.742707904970864, '20171019', 37], ['20171020', 143, 31.996531061976604, '20171019', 37], ['20171020', 144, 34.45646528592256, '20171019', 37], ['20171020', 145, 36.55133376499416, '20171019', 37], ['20171020', 146, 31.960287858527742, '20171019', 37], ['20171020', 147, 23.06456156097425, '20171019', 37], ['20171020', 148, 20.481503851035455, '20171019', 37], ['20171020', 149, 28.059187443687208, '20171019', 37], ['20171020', 150, 28.62037735600233, '20171019', 37], ['20171020', 159, 44.8834713452484, '20171019', 37], ['20171020', 160, 40.09780542623283, '20171019', 37], ['20171020', 161, 40.53139523875266, '20171019', 37], ['20171020', 162, 39.836214679609434, '20171019', 37], ['20171020', 163, 34.95351198377561, '20171019', 37], ['20171020', 164, 45.33715915228931, '20171019', 37], ['20171020', 170, 44.88061942531435, '20171019', 37], ['20171020', 171, 38.46286520788475, '20171019', 37], ['20171020', 172, 36.47300371507574, '20171019', 37], ['20171020', 173, 37.38125198545312, '20171019', 37], ['20171020', 174, 34.00661700316558, '20171019', 37], ['20171020', 175, 28.167570005239345, '20171019', 37], ['20171020', 176, 24.10315332067567, '20171019', 37], ['20171020', 177, 20.268053680608677, '20171019', 37], ['20171020', 178, 25.741561724184514, '20171019', 37], ['20171020', 179, 32.18633250309802, '20171019', 37], ['20171020', 180, 29.586550998722046, '20171019', 37], ['20171020', 181, 24.337543014856198, '20171019', 37], ['20171020', 182, 20.910858423316416, '20171019', 37], ['20171020', 183, 21.575217264258967, '20171019', 37], ['20171020', 184, 26.938188506281534, '20171019', 37], ['20171020', 185, 27.573610572428464, '20171019', 37], ['20171020', 186, 23.60406744609877, '20171019', 37], ['20171020', 187, 25.772931536788224, '20171019', 37], ['20171020', 188, 28.635502440152283, '20171019', 37], ['20171020', 189, 26.136143556385207, '20171019', 37], ['20171020', 190, 20.442162312240285, '20171019', 37], ['20171020', 191, 24.234314514752406, '20171019', 37], ['20171020', 192, 38.71387348225396, '20171019', 37], ['20171020', 193, 41.521343908885314, '20171019', 37], ['20171020', 194, 34.733442098357024, '20171019', 37], ['20171020', 195, 27.999321420348124, '20171019', 37], ['20171020', 196, 29.95987316394881, '20171019', 37], ['20171020', 197, 36.1191638884388, '20171019', 37], ['20171020', 198, 38.31970772331084, '20171019', 37], ['20171020', 199, 37.105983345007864, '20171019', 37], ['20171020', 200, 31.380376033438697, '20171019', 37], ['20171020', 201, 30.01559594610862, '20171019', 37], ['20171020', 202, 30.999709676060956, '20171019', 37], ['20171020', 203, 28.005213800291617, '20171019', 37], ['20171020', 204, 26.50105658271044, '20171019', 37], ['20171020', 205, 24.906986971530955, '20171019', 37], ['20171020', 206, 22.150846484953764, '20171019', 37], ['20171020', 207, 24.129111048689918, '20171019', 37], ['20171020', 208, 24.306542329175937, '20171019', 37], ['20171020', 209, 25.027025392563562, '20171019', 37], ['20171020', 210, 26.94212315315928, '20171019', 37], ['20171020', 211, 26.80000000000061, '20171019', 37], ['20171020', 212, 24.074841640186218, '20171019', 37], ['20171020', 213, 22.50986450425704, '20171019', 37], ['20171020', 214, 19.822159317289106, '20171019', 37], ['20171020', 215, 17.81280438336448, '20171019', 37], ['20171020', 216, 17.199302311431218, '20171019', 37], ['20171020', 217, 21.148758828830438, '20171019', 37], ['20171020', 218, 25.042164443193542, '20171019', 37], ['20171020', 219, 21.972482790981854, '20171019', 37], ['20171020', 220, 22.32608340036358, '20171019', 37], ['20171020', 221, 26.359210913834556, '20171019', 37], ['20171020', 222, 27.740115356645493, '20171019', 37], ['20171020', 223, 22.146196061625588, '20171019', 37], ['20171020', 224, 18.891850094682898, '20171019', 37], ['20171020', 225, 20.353230701782188, '20171019', 37], ['20171020', 226, 22.494577124276027, '20171019', 37], ['20171020', 227, 28.987756035954114, '20171019', 37], ['20171020', 228, 34.77407079995064, '20171019', 37], ['20171020', 229, 36.19182228073205, '20171019', 37], ['20171020', 230, 36.35530222677227, '20171019', 37], ['20171020', 231, 39.65362530714974, '20171019', 37], ['20171020', 232, 39.401395914360705, '20171019', 37], ['20171020', 233, 36.8928990457552, '20171019', 37], ['20171020', 234, 34.79813213378513, '20171019', 37], ['20171020', 235, 41.7121085537496, '20171019', 37], ['20171020', 236, 44.1445806413381, '20171019', 37], ['20171020', 237, 45.592696783580855, '20171019', 37], ['20171020', 238, 46.817518088850875, '20171019', 37], ['20171020', 239, 45.03625206431204, '20171019', 37], ['20171020', 240, 42.151725943307504, '20171019', 37], ['20171020', 241, 34.24494123224231, '20171019', 37], ['20171020', 242, 30.514521133386953, '20171019', 37], ['20171020', 243, 32.542464565548116, '20171019', 37], ['20171020', 244, 31.314373696435478, '20171019', 37], ['20171020', 245, 24.711131095114666, '20171019', 37], ['20171020', 246, 19.794696259350047, '20171019', 37], ['20171020', 247, 26.17605776277146, '20171019', 37], ['20171020', 248, 28.141570674003923, '20171019', 37], ['20171020', 249, 29.45549184787012, '20171019', 37], ['20171020', 250, 26.071670448975187, '20171019', 37], ['20171020', 251, 38.800128865764876, '20171019', 37], ['20171020', 252, 45.31458926217673, '20171019', 37], ['20171020', 258, 46.77841382517932, '20171019', 37], ['20171020', 259, 42.26229998473734, '20171019', 37], ['20171020', 260, 37.80719508241754, '20171019', 37], ['20171020', 261, 40.026116474121636, '20171019', 37], ['20171020', 262, 38.29284528472623, '20171019', 37], ['20171020', 263, 31.446398839929827, '20171019', 37], ['20171020', 264, 24.299012325607418, '20171019', 37], ['20171020', 265, 20.957337617168562, '20171019', 37], ['20171020', 266, 24.29720148494444, '20171019', 37], ['20171020', 267, 32.571122179010814, '20171019', 37], ['20171020', 268, 38.203978850376316, '20171019', 37], ['20171020', 269, 34.20081870365035, '20171019', 37], ['20171020', 270, 24.609835432201045, '20171019', 37], ['20171020', 271, 25.06044692339013, '20171019', 37], ['20171020', 272, 24.702186138073436, '20171019', 37], ['20171020', 273, 18.106076328128207, '20171019', 37], ['20171020', 274, 23.2535158631982, '20171019', 37], ['20171020', 275, 29.87192662015606, '20171019', 37], ['20171020', 276, 33.666422441358236, '20171019', 37], ['20171020', 277, 30.766475261232017, '20171019', 37], ['20171020', 278, 21.000523802990962, '20171019', 37], ['20171020', 279, 18.289833241448, '20171019', 37], ['20171020', 280, 20.625906040704947, '20171019', 37], ['20171020', 281, 19.926866286498235, '20171019', 37], ['20171020', 282, 23.130067012440055, '20171019', 37], ['20171020', 283, 27.500472723209253, '20171019', 37], ['20171020', 284, 23.434163095787145, '20171019', 37], ['20171020', 285, 17.43932338136939, '20171019', 37], ['20171020', 286, 23.350074946345607, '20171019', 37], ['20171020', 287, 28.15851558587488, '20171019', 37], ['20171020', 288, 29.727192938452376, '20171019', 37], ['20171020', 289, 23.91351082547253, '20171019', 37], ['20171020', 290, 21.145306807894105, '20171019', 37], ['20171020', 291, 27.21738415057511, '20171019', 37], ['20171020', 292, 30.110861827585325, '20171019', 37], ['20171020', 293, 44.722231608004314, '20171019', 37], ['20171020', 299, 49.594757787492284, '20171019', 37], ['20171020', 300, 44.05094777641078, '20171019', 37], ['20171020', 301, 40.93978505073023, '20171019', 37], ['20171020', 302, 33.26833329158567, '20171019', 37], ['20171020', 303, 37.379994649544415, '20171019', 37], ['20171020', 304, 34.84344988659953, '20171019', 37], ['20171020', 305, 30.24172614121155, '20171019', 37], ['20171020', 306, 32.04019350753052, '20171019', 37], ['20171020', 307, 28.619573721493698, '20171019', 37], ['20171020', 308, 20.23986165960678, '20171019', 37], ['20171020', 309, 21.970935346498695, '20171019', 37], ['20171020', 310, 17.315426647935368, '20171019', 37], ['20171020', 311, 22.41062248131384, '20171019', 37], ['20171020', 312, 25.111113077677626, '20171019', 37], ['20171020', 313, 27.57328417145758, '20171019', 37], ['20171020', 314, 31.412608933356648, '20171019', 37], ['20171020', 331, 38.524823166370275, '20171019', 37], ['20171020', 332, 32.57594204316839, '20171019', 37], ['20171020', 333, 28.89290570364804, '20171019', 37], ['20171020', 334, 26.28014459625265, '20171019', 37], ['20171020', 335, 25.868475022699556, '20171019', 37], ['20171020', 335, 25.868475022699556, '20171019', 37], ['20171020', 335, 25.868475022699556, '20171019', 37], ['20171115', 22, 44.976927418398795, '20171019', 37], ['20171115', 23, 38.26706155429111, '20171019', 37], ['20171115', 24, 29.827705241938602, '20171019', 37], ['20171115', 25, 38.284853401835385, '20171019', 37], ['20171115', 26, 37.026477013079266, '20171019', 37], ['20171115', 27, 48.319126647737455, '20171019', 37], ['20171115', 33, 48.172979978408726, '20171019', 37], ['20171115', 34, 45.77241527383003, '20171019', 37], ['20171115', 35, 43.886307659677946, '20171019', 37], ['20171115', 36, 44.98722040757745, '20171019', 37], ['20171115', 67, 45.53016582443256, '20171019', 37], ['20171115', 68, 36.10360092844135, '20171019', 37], ['20171115', 69, 37.25254353732196, '20171019', 37], ['20171115', 70, 45.14773526988958, '20171019', 37], ['20171115', 71, 40.294490938588964, '20171019', 37], ['20171115', 72, 36.652694307513045, '20171019', 37], ['20171115', 73, 41.407487245665635, '20171019', 37], ['20171115', 74, 41.88668046049869, '20171019', 37], ['20171115', 75, 25.679641742048222, '20171019', 37], ['20171115', 76, 31.486187447831504, '20171019', 37], ['20171115', 89, 49.68987824496855, '20171019', 37], ['20171115', 90, 41.53478060613669, '20171019', 37], ['20171115', 91, 36.06252902944999, '20171019', 37], ['20171115', 92, 31.434407899624073, '20171019', 37], ['20171115', 93, 31.932209444383425, '20171019', 37], ['20171115', 94, 20.778017229753818, '20171019', 37], ['20171115', 95, 27.320139091885434, '20171019', 37], ['20171115', 96, 22.174174167260677, '20171019', 37], ['20171115', 97, 27.81657779095096, '20171019', 37], ['20171115', 98, 37.523432678794116, '20171019', 37], ['20171115', 99, 49.38416750336098, '20171019', 37], ['20171115', 115, 44.1849748217654, '20171019', 37], ['20171115', 116, 36.85650553158783, '20171019', 37], ['20171115', 117, 32.87044264989375, '20171019', 37], ['20171115', 118, 28.64210187817953, '20171019', 37], ['20171115', 119, 20.97517580379279, '20171019', 37], ['20171115', 120, 27.713354181693706, '20171019', 37], ['20171115', 121, 29.94691970804319, '20171019', 37], ['20171115', 122, 19.804999368846737, '20171019', 37], ['20171115', 123, 15.138229751196645, '20171019', 37], ['20171115', 124, 17.703276532890648, '20171019', 37], ['20171115', 125, 20.717625346549003, '20171019', 37], ['20171115', 126, 27.908206678322987, '20171019', 37], ['20171115', 127, 28.936205694596207, '20171019', 37], ['20171115', 128, 25.943168657663573, '20171019', 37], ['20171115', 129, 27.142549622317116, '20171019', 37], ['20171115', 130, 29.926743892377523, '20171019', 37], ['20171115', 131, 20.746710582643377, '20171019', 37], ['20171115', 132, 19.7095915736473, '20171019', 37], ['20171115', 133, 24.344444951568466, '20171019', 37], ['20171115', 134, 31.702460472334543, '20171019', 37], ['20171115', 135, 30.915950575713477, '20171019', 37], ['20171115', 136, 25.015035478686507, '20171019', 37], ['20171115', 137, 23.20948082142142, '20171019', 37], ['20171115', 138, 24.402213014395848, '20171019', 37], ['20171115', 139, 27.45556409910424, '20171019', 37], ['20171115', 140, 28.68480433958071, '20171019', 37], ['20171115', 141, 24.844798248325453, '20171019', 37], ['20171115', 142, 21.238879443134504, '20171019', 37], ['20171115', 143, 24.444181311715237, '20171019', 37], ['20171115', 144, 29.57992562532907, '20171019', 37], ['20171115', 145, 35.319881087001995, '20171019', 37], ['20171115', 146, 39.574410924230754, '20171019', 37], ['20171115', 165, 36.63929584476244, '20171019', 37], ['20171115', 166, 32.91434337792619, '20171019', 37], ['20171115', 172, 49.15495905806349, '20171019', 37], ['20171115', 174, 44.56691598035382, '20171019', 37], ['20171115', 175, 36.0767515167305, '20171019', 37], ['20171115', 176, 39.14148694160633, '20171019', 37], ['20171115', 177, 41.31254046896706, '20171019', 37], ['20171115', 178, 33.009634957085716, '20171019', 37], ['20171115', 179, 39.08626357174658, '20171019', 37], ['20171115', 187, 42.15829692955041, '20171019', 37], ['20171115', 188, 33.03440630615488, '20171019', 37], ['20171115', 189, 26.105478352252874, '20171019', 37], ['20171115', 190, 33.886309920087136, '20171019', 37], ['20171115', 191, 27.577672128009688, '20171019', 37], ['20171115', 192, 36.30121210097787, '20171019', 37], ['20171115', 193, 42.248763295514536, '20171019', 37], ['20171115', 206, 43.36459385258744, '20171019', 37], ['20171115', 207, 40.82264077690174, '20171019', 37], ['20171115', 208, 42.38627136231659, '20171019', 37], ['20171115', 209, 40.57371070040218, '20171019', 37], ['20171115', 210, 34.077558597997125, '20171019', 37], ['20171115', 211, 27.436654314984736, '20171019', 37], ['20171115', 212, 25.776656105863793, '20171019', 37], ['20171115', 213, 23.03110939577181, '20171019', 37], ['20171115', 214, 26.583039705797486, '20171019', 37], ['20171115', 215, 21.33752562974328, '20171019', 37], ['20171115', 216, 31.80641444740555, '20171019', 37], ['20171115', 217, 42.982717457136026, '20171019', 37], ['20171115', 218, 42.827234325835974, '20171019', 37], ['20171115', 226, 49.99653988028017, '20171019', 37], ['20171115', 227, 46.40879227043368, '20171019', 37], ['20171115', 228, 38.993666152337056, '20171019', 37], ['20171115', 229, 34.40008720919287, '20171019', 37], ['20171115', 230, 27.509743728358274, '20171019', 37], ['20171115', 231, 25.95476834803203, '20171019', 37], ['20171115', 232, 34.08621422217408, '20171019', 37], ['20171115', 233, 32.9461075090819, '20171019', 37], ['20171115', 234, 33.74637758337885, '20171019', 37], ['20171115', 235, 29.74215863046922, '20171019', 37], ['20171115', 236, 22.636784223912645, '20171019', 37], ['20171115', 237, 31.400127388275802, '20171019', 37], ['20171115', 238, 30.46210760928932, '20171019', 37], ['20171115', 239, 30.649861337368264, '20171019', 37], ['20171115', 240, 34.36576785116143, '20171019', 37], ['20171115', 241, 31.511775576757625, '20171019', 37], ['20171115', 242, 24.9966797795222, '20171019', 37], ['20171115', 243, 20.813937638035203, '20171019', 37], ['20171115', 244, 29.322448738126223, '20171019', 37], ['20171115', 245, 39.23929153284979, '20171019', 37], ['20171115', 246, 49.73377122237978, '20171019', 37], ['20171115', 247, 49.123069936639894, '20171019', 37], ['20171115', 248, 48.770359851040645, '20171019', 37], ['20171115', 249, 40.95482877512697, '20171019', 37], ['20171115', 250, 36.792037181977, '20171019', 37], ['20171115', 251, 32.54642837547653, '20171019', 37], ['20171115', 252, 32.1885693997112, '20171019', 37], ['20171115', 253, 26.142455890754313, '20171019', 37], ['20171115', 254, 21.7833422596261, '20171019', 37], ['20171115', 255, 18.041895687537743, '20171019', 37], ['20171115', 256, 19.90999748869955, '20171019', 37], ['20171115', 257, 24.99755988091638, '20171019', 37], ['20171115', 258, 18.673671304807623, '20171019', 37], ['20171115', 259, 21.29906101216539, '20171019', 37], ['20171115', 260, 26.0043842457381, '20171019', 37], ['20171115', 261, 27.065660900853274, '20171019', 37], ['20171115', 262, 24.13114170527471, '20171019', 37], ['20171115', 263, 20.09288431261228, '20171019', 37], ['20171115', 264, 22.16916777869534, '20171019', 37], ['20171115', 265, 20.059960119600728, '20171019', 37], ['20171115', 266, 20.05796599857467, '20171019', 37], ['20171115', 267, 25.968403878558814, '20171019', 37], ['20171115', 268, 25.41346100002878, '20171019', 37], ['20171115', 269, 19.715222545028595, '20171019', 37], ['20171115', 270, 18.787761974221713, '20171019', 37], ['20171115', 271, 21.530490008358107, '20171019', 37], ['20171115', 272, 25.74964077419429, '20171019', 37], ['20171115', 273, 32.08071071531923, '20171019', 37], ['20171115', 274, 33.959328615271296, '20171019', 37], ['20171115', 275, 30.740657117244318, '20171019', 37], ['20171115', 276, 24.9204735107491, '20171019', 37], ['20171115', 277, 25.03988817866355, '20171019', 37], ['20171115', 278, 26.43951588059053, '20171019', 37], ['20171115', 279, 31.531603194255904, '20171019', 37], ['20171115', 280, 32.91808013842854, '20171019', 37], ['20171115', 281, 32.912702714909244, '20171019', 37], ['20171115', 298, 40.36862643192328, '20171019', 37], ['20171115', 299, 34.16489426297339, '20171019', 37], ['20171115', 300, 28.699198595083747, '20171019', 37], ['20171115', 301, 24.53576980655197, '20171019', 37], ['20171115', 302, 27.178631312119677, '20171019', 37], ['20171115', 303, 26.347333830959354, '20171019', 37], ['20171115', 304, 31.421775888704843, '20171019', 37], ['20171115', 305, 25.10330655511295, '20171019', 37], ['20171115', 306, 28.80982471310779, '20171019', 37], ['20171115', 307, 35.021450569615126, '20171019', 37], ['20171115', 308, 31.316289690829997, '20171019', 37], ['20171115', 309, 37.18031737357782, '20171019', 37], ['20171115', 310, 37.924952208274895, '20171019', 37], ['20171115', 311, 28.602517371726325, '20171019', 37], ['20171115', 312, 21.56863463457848, '20171019', 37], ['20171115', 313, 20.28565995968431, '20171019', 37], ['20171115', 314, 24.499387747451753, '20171019', 37], ['20171115', 315, 29.77378041163099, '20171019', 37], ['20171115', 316, 31.661080208988462, '20171019', 37], ['20171115', 317, 37.70249328625311, '20171019', 37], ['20171115', 318, 39.73814288564516, '20171019', 37], ['20171115', 319, 36.701471360150116, '20171019', 37], ['20171115', 320, 35.35955316459525, '20171019', 37], ['20171115', 321, 34.95771731678002, '20171019', 37], ['20171115', 322, 30.583034512616823, '20171019', 37], ['20171115', 323, 35.28430245874153, '20171019', 37], ['20171115', 324, 41.12546656270313, '20171019', 37], ['20171115', 325, 36.75551659275117, '20171019', 37], ['20171115', 326, 30.33077644901441, '20171019', 37], ['20171115', 327, 26.460083144240333, '20171019', 37], ['20171115', 328, 24.96902080579137, '20171019', 37], ['20171115', 329, 27.732471941750813, '20171019', 37], ['20171115', 330, 26.716100014785503, '20171019', 37], ['20171115', 331, 32.806889520343255, '20171019', 37], ['20171115', 332, 37.565143417801195, '20171019', 37], ['20171115', 333, 31.541623293673332, '20171019', 37], ['20171115', 334, 23.790754506741827, '20171019', 37], ['20171115', 334, 23.790754506741827, '20171019', 37], ['20171115', 334, 23.790754506741827, '20171019', 37], ['20171019', 71, 47.67173166563445, '20171020', 29], ['20171019', 72, 43.646191128208564, '20171020', 29], ['20171019', 86, 46.21279043728202, '20171020', 29], ['20171019', 87, 45.28483189766779, '20171020', 29], ['20171019', 88, 48.87473785095906, '20171020', 29], ['20171020', 28, 44.395089818584744, '20171020', 29], ['20171020', 29, 0.0, '20171020', 29], ['20171020', 30, 38.43173168099592, '20171020', 29], ['20171020', 78, 45.498285681990254, '20171020', 29], ['20171020', 104, 49.72781917599078, '20171020', 29], ['20171115', 60, 29.598040475678435, '20171020', 29], ['20171115', 61, 40.81333115539279, '20171020', 29], ['20171115', 161, 44.27190983004984, '20171020', 29], ['20171115', 188, 48.6348023538696, '20171020', 29], ['20171115', 189, 48.01233174924933, '20171020', 29], ['20171115', 254, 48.6220320430976, '20171020', 29], ['20171115', 298, 46.84124251127479, '20171020', 29], ['20171115', 299, 42.09261217838611, '20171020', 29], ['20171115', 300, 45.4702540129263, '20171020', 29], ['20171115', 301, 49.396113207417194, '20171020', 29], ['20171019', 33, 49.838780081380186, '20171115', 26], ['20171019', 35, 49.794658348059414, '20171115', 26], ['20171019', 36, 40.13990533122849, '20171115', 26], ['20171019', 37, 34.975419940295644, '20171115', 26], ['20171019', 38, 27.84022270025837, '20171115', 26], ['20171019', 39, 20.8547836239062, '20171115', 26], ['20171019', 40, 25.69365680474256, '20171115', 26], ['20171019', 41, 25.957118484146097, '20171115', 26], ['20171019', 42, 29.221567377538225, '20171115', 26], ['20171019', 43, 33.91754708112023, '20171115', 26], ['20171019', 44, 40.2384641854095, '20171115', 26], ['20171019', 45, 42.39186242664824, '20171115', 26], ['20171019', 46, 47.69599563904483, '20171115', 26], ['20171019', 56, 48.0877323233263, '20171115', 26], ['20171019', 57, 49.43881066530602, '20171115', 26], ['20171019', 85, 44.97766112194009, '20171115', 26], ['20171019', 86, 36.57083537465397, '20171115', 26], ['20171019', 87, 30.075903976438948, '20171115', 26], ['20171019', 88, 25.67138484772393, '20171115', 26], ['20171019', 89, 23.754494311603295, '20171115', 26], ['20171019', 90, 24.865478077043974, '20171115', 26], ['20171019', 91, 29.82116697917709, '20171115', 26], ['20171019', 92, 34.56651558951214, '20171115', 26], ['20171019', 93, 34.45785831998312, '20171115', 26], ['20171019', 94, 35.16444226772374, '20171115', 26], ['20171019', 95, 38.45040962070696, '20171115', 26], ['20171019', 96, 45.27224315184894, '20171115', 26], ['20171019', 97, 47.26582274752159, '20171115', 26], ['20171019', 98, 45.11487559552953, '20171115', 26], ['20171019', 99, 44.49568518407243, '20171115', 26], ['20171019', 100, 49.98015606218079, '20171115', 26], ['20171019', 105, 49.76133036806808, '20171115', 26], ['20171019', 106, 48.96227118915103, '20171115', 26], ['20171019', 108, 47.30344596326821, '20171115', 26], ['20171019', 109, 43.058425424067224, '20171115', 26], ['20171019', 110, 43.244305983561524, '20171115', 26], ['20171019', 111, 42.97953001138914, '20171115', 26], ['20171019', 112, 38.72722556548394, '20171115', 26], ['20171019', 113, 38.985227971628746, '20171115', 26], ['20171019', 127, 49.38671886246331, '20171115', 26], ['20171019', 128, 47.478689956653476, '20171115', 26], ['20171019', 129, 49.651827760919005, '20171115', 26], ['20171019', 130, 49.374446832344255, '20171115', 26], ['20171019', 131, 45.90071894861924, '20171115', 26], ['20171019', 132, 41.52967613647025, '20171115', 26], ['20171019', 133, 35.3521427922, '20171115', 26], ['20171019', 134, 35.881387933021585, '20171115', 26], ['20171019', 135, 43.026317527764675, '20171115', 26], ['20171019', 136, 47.26008886999648, '20171115', 26], ['20171019', 137, 46.289199604228244, '20171115', 26], ['20171019', 147, 42.808573907570974, '20171115', 26], ['20171019', 148, 36.20541395979272, '20171115', 26], ['20171019', 149, 33.50408930265081, '20171115', 26], ['20171019', 150, 38.90352169148709, '20171115', 26], ['20171019', 151, 41.56500932274754, '20171115', 26], ['20171019', 152, 38.60031087957745, '20171115', 26], ['20171019', 153, 37.45816332924007, '20171115', 26], ['20171019', 154, 37.97946813740365, '20171115', 26], ['20171019', 155, 39.96618570741998, '20171115', 26], ['20171019', 156, 41.21829690804735, '20171115', 26], ['20171019', 157, 43.53446910208021, '20171115', 26], ['20171019', 158, 43.83913776524364, '20171115', 26], ['20171019', 159, 38.45321833085059, '20171115', 26], ['20171019', 160, 31.54530075938502, '20171115', 26], ['20171019', 161, 28.818154000561577, '20171115', 26], ['20171019', 162, 28.002821286435807, '20171115', 26], ['20171019', 163, 26.17747123004958, '20171115', 26], ['20171019', 164, 31.040264174133515, '20171115', 26], ['20171019', 165, 44.44619218785811, '20171115', 26], ['20171019', 166, 49.45802260503407, '20171115', 26], ['20171019', 167, 49.957702108884625, '20171115', 26], ['20171019', 184, 48.58973142547862, '20171115', 26], ['20171019', 185, 45.893790429644284, '20171115', 26], ['20171019', 186, 40.090772005539684, '20171115', 26], ['20171019', 187, 34.15333073069255, '20171115', 26], ['20171019', 188, 31.91266206382723, '20171115', 26], ['20171019', 189, 33.22210107744638, '20171115', 26], ['20171019', 190, 40.143293337742236, '20171115', 26], ['20171019', 191, 44.100249432402094, '20171115', 26], ['20171019', 192, 41.9385025960648, '20171115', 26], ['20171019', 193, 36.709617268506065, '20171115', 26], ['20171019', 194, 33.1858704873043, '20171115', 26], ['20171019', 195, 31.757455817493636, '20171115', 26], ['20171019', 196, 29.74114994414283, '20171115', 26], ['20171019', 197, 29.523312822242563, '20171115', 26], ['20171019', 198, 33.49346204858428, '20171115', 26], ['20171019', 199, 36.3735618272398, '20171115', 26], ['20171019', 200, 41.58273680266891, '20171115', 26], ['20171019', 201, 43.52675039559141, '20171115', 26], ['20171019', 202, 38.04757548123373, '20171115', 26], ['20171019', 203, 29.938637243536974, '20171115', 26], ['20171019', 204, 21.393550429979072, '20171115', 26], ['20171019', 205, 18.412767309669658, '20171115', 26], ['20171019', 206, 21.016279404310932, '20171115', 26], ['20171019', 207, 28.73840635804387, '20171115', 26], ['20171019', 208, 33.9405067728814, '20171115', 26], ['20171019', 209, 36.39708779559237, '20171115', 26], ['20171019', 210, 37.809072985198, '20171115', 26], ['20171019', 211, 36.28853813534091, '20171115', 26], ['20171019', 212, 34.66753524552975, '20171115', 26], ['20171019', 213, 31.81612798566333, '20171115', 26], ['20171019', 214, 27.089813583709653, '20171115', 26], ['20171019', 215, 25.950105972810345, '20171115', 26], ['20171019', 216, 31.58420491321636, '20171115', 26], ['20171019', 217, 37.58904095610871, '20171115', 26], ['20171019', 218, 40.8014705617344, '20171115', 26], ['20171019', 219, 41.02791732467194, '20171115', 26], ['20171019', 220, 41.392922100282725, '20171115', 26], ['20171019', 221, 37.75375478015508, '20171115', 26], ['20171019', 222, 32.050085803318616, '20171115', 26], ['20171019', 223, 29.68935836288955, '20171115', 26], ['20171019', 224, 35.59764037123838, '20171115', 26], ['20171019', 225, 41.889378128590586, '20171115', 26], ['20171019', 226, 44.9525305183151, '20171115', 26], ['20171019', 227, 48.81981155227935, '20171115', 26], ['20171019', 246, 48.6835701238106, '20171115', 26], ['20171020', 46, 49.18747808131645, '20171115', 26], ['20171020', 47, 34.035128911169856, '20171115', 26], ['20171020', 48, 38.693487824177595, '20171115', 26], ['20171020', 50, 49.226882899486995, '20171115', 26], ['20171020', 76, 49.16952308086728, '20171115', 26], ['20171020', 77, 43.62235665344044, '20171115', 26], ['20171020', 78, 36.75483641645053, '20171115', 26], ['20171020', 79, 35.90197766140561, '20171115', 26], ['20171020', 80, 30.824697889842447, '20171115', 26], ['20171020', 81, 33.27145924061711, '20171115', 26], ['20171020', 82, 31.358156833590325, '20171115', 26], ['20171020', 83, 31.0754565533652, '20171115', 26], ['20171020', 84, 39.94809131861399, '20171115', 26], ['20171020', 85, 45.743545992854685, '20171115', 26], ['20171020', 86, 48.13886164005357, '20171115', 26], ['20171020', 99, 45.458200580311924, '20171115', 26], ['20171020', 103, 45.91564003691945, '20171115', 26], ['20171020', 104, 39.3169174783571, '20171115', 26], ['20171020', 105, 32.62698269837268, '20171115', 26], ['20171020', 106, 38.813193633092176, '20171115', 26], ['20171020', 107, 47.492862621660585, '20171115', 26], ['20171020', 108, 47.36165115365035, '20171115', 26], ['20171020', 109, 46.85022945514838, '20171115', 26], ['20171020', 110, 45.19577413874098, '20171115', 26], ['20171020', 111, 36.83338159876206, '20171115', 26], ['20171020', 112, 30.58496362593876, '20171115', 26], ['20171020', 113, 30.592417361169897, '20171115', 26], ['20171020', 114, 25.86994395046183, '20171115', 26], ['20171020', 115, 20.526470714666324, '20171115', 26], ['20171020', 116, 23.987455054674722, '20171115', 26], ['20171020', 117, 29.24086182040528, '20171115', 26], ['20171020', 118, 28.34314731994288, '20171115', 26], ['20171020', 119, 26.889998140572906, '20171115', 26], ['20171020', 120, 27.484868564358102, '20171115', 26], ['20171020', 121, 23.352216168922293, '20171115', 26], ['20171020', 122, 24.071601525450525, '20171115', 26], ['20171020', 123, 30.58166117136624, '20171115', 26], ['20171020', 124, 40.406657867232354, '20171115', 26], ['20171020', 125, 45.67288035584604, '20171115', 26], ['20171020', 130, 46.30254852597217, '20171115', 26], ['20171020', 131, 40.82599661980233, '20171115', 26], ['20171020', 132, 34.76032220794406, '20171115', 26], ['20171020', 133, 27.043039769968445, '20171115', 26], ['20171020', 134, 20.70883869269442, '20171115', 26], ['20171020', 135, 15.72113227474446, '20171115', 26], ['20171020', 136, 21.4119125722113, '20171115', 26], ['20171020', 137, 27.94430174472601, '20171115', 26], ['20171020', 138, 32.39342525883583, '20171115', 26], ['20171020', 139, 37.275943985364904, '20171115', 26], ['20171020', 140, 42.677675663041995, '20171115', 26], ['20171020', 141, 46.60424873335164, '20171115', 26], ['20171020', 142, 46.350620276325216, '20171115', 26], ['20171020', 143, 46.08403194166213, '20171115', 26], ['20171020', 144, 49.88105852926697, '20171115', 26], ['20171020', 146, 43.40350216284416, '20171115', 26], ['20171020', 147, 32.72561687730294, '20171115', 26], ['20171020', 148, 24.518482824189327, '20171115', 26], ['20171020', 149, 14.19697150803774, '20171115', 26], ['20171020', 150, 15.07905832603596, '20171115', 26], ['20171020', 151, 34.66493905951629, '20171115', 26], ['20171020', 152, 39.112632230519004, '20171115', 26], ['20171020', 153, 42.471637594982646, '20171115', 26], ['20171020', 154, 46.63916808863703, '20171115', 26], ['20171020', 163, 48.54552502548664, '20171115', 26], ['20171020', 174, 49.57497352495518, '20171115', 26], ['20171020', 175, 49.051156969026295, '20171115', 26], ['20171020', 176, 45.82014840656954, '20171115', 26], ['20171020', 177, 42.42034889059783, '20171115', 26], ['20171020', 178, 46.15395974345007, '20171115', 26], ['20171020', 179, 49.73135831645836, '20171115', 26], ['20171020', 180, 49.08299094391127, '20171115', 26], ['20171020', 181, 46.680574118149885, '20171115', 26], ['20171020', 182, 43.2692962734557, '20171115', 26], ['20171020', 183, 41.506071844972425, '20171115', 26], ['20171020', 184, 43.174599013771974, '20171115', 26], ['20171020', 185, 42.18070649005254, '20171115', 26], ['20171020', 186, 43.05837897552613, '20171115', 26], ['20171020', 187, 45.559367862164514, '20171115', 26], ['20171020', 188, 46.606523148590384, '20171115', 26], ['20171020', 189, 42.52521604883526, '20171115', 26], ['20171020', 190, 37.4514886219508, '20171115', 26], ['20171020', 191, 44.78859229759291, '20171115', 26], ['20171020', 202, 49.26014616299983, '20171115', 26], ['20171020', 203, 46.154566404637784, '20171115', 26], ['20171020', 204, 45.00868805019857, '20171115', 26], ['20171020', 205, 42.92875493186429, '20171115', 26], ['20171020', 206, 41.7464729049063, '20171115', 26], ['20171020', 207, 42.152271587662845, '20171115', 26], ['20171020', 208, 42.69697881583859, '20171115', 26], ['20171020', 209, 44.49130252083125, '20171115', 26], ['20171020', 210, 47.05930301226427, '20171115', 26], ['20171020', 211, 46.48565370090143, '20171115', 26], ['20171020', 212, 44.932950047823084, '20171115', 26], ['20171020', 213, 41.79504755350978, '20171115', 26], ['20171020', 214, 36.881024931529254, '20171115', 26], ['20171020', 215, 30.81759237838071, '20171115', 26], ['20171020', 216, 29.120302196233787, '20171115', 26], ['20171020', 217, 32.52030135161788, '20171115', 26], ['20171020', 218, 35.039206612022426, '20171115', 26], ['20171020', 219, 36.64693711621818, '20171115', 26], ['20171020', 220, 40.14117586718294, '20171115', 26], ['20171020', 221, 44.78370239272507, '20171115', 26], ['20171020', 222, 43.33241281073783, '20171115', 26], ['20171020', 223, 39.08060900242073, '20171115', 26], ['20171020', 224, 33.4108066349801, '20171115', 26], ['20171020', 225, 24.352535802253037, '20171115', 26], ['20171020', 226, 16.073020873501935, '20171115', 26], ['20171020', 227, 14.138528919234913, '20171115', 26], ['20171020', 228, 17.324664498917056, '20171115', 26], ['20171020', 229, 21.720036832380757, '20171115', 26], ['20171020', 230, 29.3554083602992, '20171115', 26], ['20171020', 231, 34.8914029525895, '20171115', 26], ['20171020', 232, 36.35835529833565, '20171115', 26], ['20171020', 233, 36.48257118132093, '20171115', 26], ['20171020', 234, 34.932019695404804, '20171115', 26], ['20171020', 235, 31.240806647715907, '20171115', 26], ['20171020', 236, 27.960758215753668, '20171115', 26], ['20171020', 237, 30.467851909836405, '20171115', 26], ['20171020', 238, 35.5080835866986, '20171115', 26], ['20171020', 239, 41.29750597796604, '20171115', 26], ['20171020', 240, 43.83113048964142, '20171115', 26], ['20171020', 241, 43.75614242595087, '20171115', 26], ['20171020', 242, 44.59748871853748, '20171115', 26], ['20171020', 243, 44.90314020199617, '20171115', 26], ['20171020', 244, 37.955473913522205, '20171115', 26], ['20171020', 245, 29.36535373531238, '20171115', 26], ['20171020', 246, 26.1323936905905, '20171115', 26], ['20171020', 247, 23.76615240210489, '20171115', 26], ['20171020', 248, 22.806490304298414, '20171115', 26], ['20171020', 249, 24.94205284253996, '20171115', 26], ['20171020', 250, 23.365872549511014, '20171115', 26], ['20171020', 251, 27.652088528717954, '20171115', 26], ['20171020', 252, 25.03845043128531, '20171115', 26], ['20171020', 253, 31.908118089286603, '20171115', 26], ['20171020', 254, 39.59674229024567, '20171115', 26], ['20171020', 255, 46.20116881638626, '20171115', 26], ['20171020', 256, 49.0698481758393, '20171115', 26], ['20171020', 257, 49.27788550658647, '20171115', 26], ['20171020', 258, 48.28030654417974, '20171115', 26], ['20171020', 259, 47.00363815706354, '20171115', 26], ['20171020', 260, 48.419376286773165, '20171115', 26], ['20171020', 263, 43.54101514664175, '20171115', 26], ['20171020', 264, 34.74653939603381, '20171115', 26], ['20171020', 265, 27.731318035754096, '20171115', 26], ['20171020', 266, 26.96045251845771, '20171115', 26], ['20171020', 267, 39.909171878154, '20171115', 26], ['20171020', 270, 48.75362550621294, '20171115', 26], ['20171020', 271, 45.89350716604841, '20171115', 26], ['20171020', 272, 36.34372022784851, '20171115', 26], ['20171020', 273, 30.882519327283116, '20171115', 26], ['20171020', 274, 34.55387098430552, '20171115', 26], ['20171020', 275, 42.969663717557864, '20171115', 26], ['20171020', 276, 49.47168887353753, '20171115', 26], ['20171020', 277, 48.579172491924766, '20171115', 26], ['20171020', 278, 44.419657810479315, '20171115', 26], ['20171020', 279, 38.26536292784913, '20171115', 26], ['20171020', 280, 29.106287980435138, '20171115', 26], ['20171020', 281, 22.716073604389315, '20171115', 26], ['20171020', 282, 28.996275622913636, '20171115', 26], ['20171020', 283, 30.686935330853363, '20171115', 26], ['20171020', 284, 27.858212433678705, '20171115', 26], ['20171020', 285, 29.757385637854888, '20171115', 26], ['20171020', 286, 34.092198521069285, '20171115', 26], ['20171020', 287, 38.937924957552184, '20171115', 26], ['20171020', 288, 40.06781750981627, '20171115', 26], ['20171020', 289, 38.79773189246942, '20171115', 26], ['20171020', 290, 39.883129265392974, '20171115', 26], ['20171020', 291, 41.96972718519953, '20171115', 26], ['20171020', 292, 43.701441623818994, '20171115', 26], ['20171020', 307, 47.77007431436607, '20171115', 26], ['20171020', 308, 42.20630284685129, '20171115', 26], ['20171020', 309, 34.83759463568261, '20171115', 26], ['20171020', 310, 26.18121463951047, '20171115', 26], ['20171020', 311, 20.670365260441322, '20171115', 26], ['20171020', 312, 21.583512225769947, '20171115', 26], ['20171020', 313, 29.34140419270932, '20171115', 26], ['20171020', 314, 31.669417424385387, '20171115', 26], ['20171020', 315, 49.49494923727101, '20171115', 26], ['20171020', 331, 47.075704986755454, '20171115', 26], ['20171020', 332, 44.339778980053666, '20171115', 26], ['20171020', 333, 40.12321024045915, '20171115', 26], ['20171020', 334, 36.93104385202291, '20171115', 26], ['20171020', 335, 37.41435553367185, '20171115', 26], ['20171020', 335, 37.41435553367185, '20171115', 26], ['20171020', 335, 37.41435553367185, '20171115', 26], ['20171115', 23, 43.14051460054806, '20171115', 26], ['20171115', 24, 29.836822887166086, '20171115', 26], ['20171115', 25, 16.70646581416973, '20171115', 26], ['20171115', 26, 0.0, '20171115', 26], ['20171115', 27, 20.529247428972116, '20171115', 26], ['20171115', 28, 35.96723508972847, '20171115', 26], ['20171115', 29, 47.64191431922026, '20171115', 26], ['20171115', 30, 47.89941544528724, '20171115', 26], ['20171115', 31, 48.817005233828425, '20171115', 26], ['20171115', 68, 42.99876742419657, '20171115', 26], ['20171115', 69, 46.103839319520084, '20171115', 26], ['20171115', 70, 48.08012063212962, '20171115', 26], ['20171115', 71, 44.96124998262528, '20171115', 26], ['20171115', 74, 46.812626501831794, '20171115', 26], ['20171115', 75, 34.31466158947196, '20171115', 26], ['20171115', 76, 30.127860860008724, '20171115', 26], ['20171115', 77, 38.65871182540823, '20171115', 26], ['20171115', 90, 48.72894417079084, '20171115', 26], ['20171115', 91, 42.15668393031027, '20171115', 26], ['20171115', 92, 37.84983487414563, '20171115', 26], ['20171115', 93, 30.346696690085526, '20171115', 26], ['20171115', 94, 31.557661510320685, '20171115', 26], ['20171115', 95, 31.690661084930934, '20171115', 26], ['20171115', 96, 33.7504074049487, '20171115', 26], ['20171115', 97, 41.33852924331003, '20171115', 26], ['20171115', 118, 43.53336651351464, '20171115', 26], ['20171115', 119, 40.36520779086773, '20171115', 26], ['20171115', 120, 46.41984489418191, '20171115', 26], ['20171115', 121, 44.432893221125006, '20171115', 26], ['20171115', 122, 37.664811163736566, '20171115', 26], ['20171115', 123, 33.644940184223934, '20171115', 26], ['20171115', 124, 28.24149429474415, '20171115', 26], ['20171115', 125, 24.939366471506, '20171115', 26], ['20171115', 126, 33.54352396514162, '20171115', 26], ['20171115', 127, 36.79233615849995, '20171115', 26], ['20171115', 128, 40.29789076366198, '20171115', 26], ['20171115', 129, 45.96613971174932, '20171115', 26], ['20171115', 130, 42.31597806975553, '20171115', 26], ['20171115', 131, 35.06254411762068, '20171115', 26], ['20171115', 132, 31.092764431618132, '20171115', 26], ['20171115', 133, 35.30019829972714, '20171115', 26], ['20171115', 134, 40.094762750264785, '20171115', 26], ['20171115', 135, 42.31089694156882, '20171115', 26], ['20171115', 136, 43.2112022512685, '20171115', 26], ['20171115', 137, 43.542898387682015, '20171115', 26], ['20171115', 138, 42.377352442076436, '20171115', 26], ['20171115', 139, 43.960072793388235, '20171115', 26], ['20171115', 140, 44.488492894230944, '20171115', 26], ['20171115', 141, 42.21895308981566, '20171115', 26], ['20171115', 142, 41.084230551393716, '20171115', 26], ['20171115', 143, 42.44165406767435, '20171115', 26], ['20171115', 144, 46.92253190099716, '20171115', 26], ['20171115', 187, 38.865228675514736, '20171115', 26], ['20171115', 188, 32.94820177187286, '20171115', 26], ['20171115', 189, 29.019579597231985, '20171115', 26], ['20171115', 190, 25.489017242728753, '20171115', 26], ['20171115', 191, 22.01272359341426, '20171115', 26], ['20171115', 192, 24.988357288946183, '20171115', 26], ['20171115', 193, 28.314837100011435, '20171115', 26], ['20171115', 194, 39.47224341230586, '20171115', 26], ['20171115', 195, 44.60289228290136, '20171115', 26], ['20171115', 196, 38.59468875376458, '20171115', 26], ['20171115', 197, 43.10345693792715, '20171115', 26], ['20171115', 198, 49.220971140352454, '20171115', 26], ['20171115', 211, 44.34652184782985, '20171115', 26], ['20171115', 212, 37.23562809998019, '20171115', 26], ['20171115', 213, 31.88817962819539, '20171115', 26], ['20171115', 214, 26.288894993894978, '20171115', 26], ['20171115', 215, 21.475614077366142, '20171115', 26], ['20171115', 216, 22.665392121029537, '20171115', 26], ['20171115', 217, 24.946623017956593, '20171115', 26], ['20171115', 218, 26.828641411744766, '20171115', 26], ['20171115', 219, 37.774435799892835, '20171115', 26], ['20171115', 220, 47.284500631810616, '20171115', 26], ['20171115', 229, 42.580394549607774, '20171115', 26], ['20171115', 230, 31.10475847840956, '20171115', 26], ['20171115', 231, 32.83738722858549, '20171115', 26], ['20171115', 232, 33.90377560095642, '20171115', 26], ['20171115', 233, 42.01640155939147, '20171115', 26], ['20171115', 234, 48.167769306872586, '20171115', 26], ['20171115', 235, 45.51496457210685, '20171115', 26], ['20171115', 236, 46.46116658027441, '20171115', 26], ['20171115', 237, 48.18692768791152, '20171115', 26], ['20171115', 238, 46.657903939203756, '20171115', 26], ['20171115', 242, 45.73823345954724, '20171115', 26], ['20171115', 243, 39.241967330907784, '20171115', 26], ['20171115', 244, 48.07192527869124, '20171115', 26], ['20171115', 252, 45.98730259539123, '20171115', 26], ['20171115', 253, 39.16396302725336, '20171115', 26], ['20171115', 254, 33.34267535756685, '20171115', 26], ['20171115', 255, 29.76235877749093, '20171115', 26], ['20171115', 256, 30.638276713941966, '20171115', 26], ['20171115', 257, 29.589085825690074, '20171115', 26], ['20171115', 258, 30.81626194073618, '20171115', 26], ['20171115', 259, 35.81181369324966, '20171115', 26], ['20171115', 260, 40.774698036895614, '20171115', 26], ['20171115', 261, 41.6047833788379, '20171115', 26], ['20171115', 262, 39.88363072740678, '20171115', 26], ['20171115', 263, 39.49237901165258, '20171115', 26], ['20171115', 264, 34.99508536923483, '20171115', 26], ['20171115', 265, 28.765708751914445, '20171115', 26], ['20171115', 266, 30.72344381738696, '20171115', 26], ['20171115', 267, 34.26172791906654, '20171115', 26], ['20171115', 268, 31.7956600812141, '20171115', 26], ['20171115', 269, 28.819056195512374, '20171115', 26], ['20171115', 270, 27.753053886015238, '20171115', 26], ['20171115', 271, 28.184144478766903, '20171115', 26], ['20171115', 272, 32.859275707172706, '20171115', 26], ['20171115', 273, 43.96116467974904, '20171115', 26], ['20171115', 274, 49.809798232877824, '20171115', 26], ['20171115', 275, 49.16262808272281, '20171115', 26], ['20171115', 276, 46.737287041505596, '20171115', 26], ['20171115', 277, 44.11367135027533, '20171115', 26], ['20171115', 278, 43.5710913335916, '20171115', 26], ['20171115', 279, 46.81685593886145, '20171115', 26], ['20171115', 280, 49.832519502832056, '20171115', 26], ['20171115', 299, 47.96473704712777, '20171115', 26], ['20171115', 300, 39.6742737803748, '20171115', 26], ['20171115', 301, 33.610534063000514, '20171115', 26], ['20171115', 302, 31.629068908207202, '20171115', 26], ['20171115', 303, 39.76453193487945, '20171115', 26], ['20171115', 304, 41.40768044699022, '20171115', 26], ['20171115', 305, 42.318317546897404, '20171115', 26], ['20171115', 306, 49.75083918890312, '20171115', 26], ['20171115', 308, 49.565492028225236, '20171115', 26], ['20171115', 311, 43.719057629368294, '20171115', 26], ['20171115', 312, 34.20856617866351, '20171115', 26], ['20171115', 313, 26.107853224653528, '20171115', 26], ['20171115', 314, 21.582492905130067, '20171115', 26], ['20171115', 315, 29.04269271262558, '20171115', 26], ['20171115', 316, 41.730564338383324, '20171115', 26], ['20171115', 322, 49.572875647878654, '20171115', 26], ['20171115', 327, 47.34803058206593, '20171115', 26], ['20171115', 328, 44.25015254211202, '20171115', 26], ['20171115', 329, 41.81408853484737, '20171115', 26], ['20171115', 330, 42.85970135220345, '20171115', 26], ['20171115', 334, 46.85471160940106, '20171115', 26], ['20171115', 334, 46.85471160940106, '20171115', 26], ['20171115', 334, 46.85471160940106, '20171115', 26]]

    root = Tk()
    f = Figure(figsize=(5,4),dpi=100)
    all_plot = f.add_subplot(211)
    f_plot = f.add_subplot(111)
    canvs = FigureCanvasTkAgg(f, root)
    canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    Button(root, text='Next->', command=lambda: show_result(canvs, f_plot, test_ret, wtf, 1)).pack()
    Button(root, text='<-Back', command=lambda: show_result(canvs, f_plot, test_ret, wtf, -1)).pack()
    mytext = Text(root, width=50, height = 5)
    mytext.pack()
    refresh_ret_text(mytext, wtf)
    root.mainloop()

def show_big_dia(canvs, plot, date_list, wtf, step):
    if wtf.cnt + step > len(date_list) - 1 or wtf.cnt + step < 0:
        return
    wtf.add_x(step)
    day = date_list[wtf.cnt]
    print("Inspect DAY:", day)
    dayk = dayk_handler()
    dayk.init_db()
    dayk.import_dayk_from_DB(day)
    plot.clear()
    plot.plot(dayk.day_1ktable.iloc[19:, COL_END])
    plot.plot(dayk.day_1ktable.iloc[19:, COL_MA5])
    plot.plot(dayk.day_1ktable.iloc[19:, COL_MA10])
    plot.plot(dayk.day_1ktable.iloc[19:, COL_MA20])
    for i in range(19, dayk.length - dayk.inspect_bars):
        if dayk.day_1ktable.iloc[i, COL_RET] == distance_t:
            plot.annotate(
                "BUY",
                xy=(i+dayk.inspect_bars, dayk.day_1ktable.iloc[i+dayk.inspect_bars, COL_END]),
                xytext=(i+dayk.inspect_bars, dayk.day_1ktable.iloc[i+dayk.inspect_bars, COL_END] + 50),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2")
            )
    canvs.draw()

def refresh_ret_text(text, wtf):
    string = wtf.string
    text.delete(1.0, 'end')
    text.insert('end', string)
    text.after(100, refresh_ret_text, text, wtf)

def show_result(canvs, plot, test_ret, wtf, step):
    wtf.add_x(step)
    wtf.string = "Day: " + str(test_ret[wtf.cnt][0]) + " Num: " + str(test_ret[wtf.cnt][1])
    wtf.string += "\nDistance: " + str(test_ret[wtf.cnt][2]) + "\nCompared with: \nDate: " +   str(test_ret[wtf.cnt][3]) + "\nNum : " +   str(test_ret[wtf.cnt][4])

    day = test_ret[wtf.cnt][0]
    num = test_ret[wtf.cnt][1]
    show_unit_plot(canvs, plot, day, num)

def show_unit_plot(canvs, plot, day, num):
    dayk = dayk_handler()
    dayk.init_db()
    dayk.import_dayk_from_DB(day)
    comp = inter_comparer(dayk, dayk)
    comp.init_compare_data()
    comp.move_data(num)
    comp.sudo_move(1)
    plot.clear()
    plot.plot(comp.close_list_show)
    plot.plot(comp.ma5_list_show)
    plot.plot(comp.ma10_list_show)
    plot.plot(comp.ma20_list_show)
    plot.annotate(
        "BUY",
        xy=(num + dayk.inspect_bars - 1, 10),
        xytext=(num + dayk.inspect_bars - 1, 10 + 50),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2")
    )
    plot.set_ylim(0, 100)
    canvs.draw()



if __name__ == "__main__":
#    Usage
    #samp = sample_handler()
    #samp.init_db()
    #samp.input_sample_mannual()
    #os._exit(0)


    #date = "20171019"
    #date_fix = "20171019"
    auto_test_sample()
    os._exit(0)



    # Enable following two lines to import data to DB
    date = "20171116"
    test = dayk_handler()
    test.init_db()
    test.import_dayk2db(date)
    os._exit(0)

    #file_full_path = filename_prefix + date + filename_postfix
    #test.init_data_from_file(file_full_path)
    #test.import_dayk_from_DB(date)

    #test.init_compare_data()



    dayk = dayk_handler()
    dayk.init_db()
    dayk.import_dayk_from_DB(date)

    dayk_fix = dayk_handler()
    dayk_fix.init_db()
    dayk_fix.import_dayk_from_DB(date_fix)

    comp = inter_comparer(dayk, dayk_fix)
    comp.init_compare_data()

    root = Tk()
    f = Figure(figsize=(5,4),dpi=100)
    f_plot = f.add_subplot(211 )
    f_plot2 = f.add_subplot(212 )
    canvs = FigureCanvasTkAgg(f, root)
    canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    Button(root, text='Next', command=lambda: get_dataset(comp, f_plot, 1)).pack()
    Button(root, text='Before', command=lambda: get_dataset(comp, f_plot, -1)).pack()
    Button(root, text='Next>>', command=lambda: get_dataset(comp, f_plot, 10)).pack()
    Button(root, text='<<Before', command=lambda: get_dataset(comp, f_plot, -10)).pack()
    Button(root, text='Start Up', command=lambda: set_ret_start_up(comp)).pack()
    Button(root, text='Other', command=lambda: set_ret_other(comp)).pack()
    mytext = Text(root, width=50, height = 5)
    mytext.pack()
    refresh_text(mytext, comp)

    Button(root, text='Next2', command=lambda: get_dataset(comp, f_plot2, 1, 0)).pack()
    Button(root, text='Before2', command=lambda: get_dataset(comp, f_plot2, -1, 0)).pack()
    Button(root, text='Next2>>', command=lambda: get_dataset(comp, f_plot2, 10, 0)).pack()
    Button(root, text='<<Before2', command=lambda: get_dataset(comp, f_plot2, -10, 0)).pack()
    #Button(root, text='Start Up2', command=lambda: set_ret_start_up(test)).pack()
    #Button(root, text='Other2', command=lambda: set_ret_other(test)).pack()
    mytext2 = Text(root)
    mytext2.pack()
    refresh_text(mytext2, comp)

    root.mainloop()
