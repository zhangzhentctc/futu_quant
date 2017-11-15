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

filename_prefix = "/Users/aaron/finance/dayk/dayk_"
filename_postfix = ".csv"

class daytest:
    def __init__(self):
        self.count = 0
        self.daytestcount = 0
        self.tmp = 0
        self.trend_c_cnt = 0
        self.trend = 0
        self.trend_p_cnt = 0
        self.data = []
        self.point = 19
        self.point_fix = 19
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


    def init_compare_data(self):
        close_list = self.day_1ktable.iloc[self.point:self.point + self.inspect_bars, COL_END]
        ma5_list = self.day_1ktable.iloc[self.point:self.point + self.inspect_bars, COL_MA5]
        ma10_list = self.day_1ktable.iloc[self.point:self.point + self.inspect_bars, COL_MA10]
        ma20_list = self.day_1ktable.iloc[self.point:self.point + self.inspect_bars, COL_MA20]
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
        self.close_list = close_list - all_min
        self.ma5_list = ma5_list - all_min
        self.ma10_list = ma10_list - all_min
        self.ma20_list = ma20_list - all_min



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


    def get_data(self, step, type = 1):
        if type == 0:
            self.point_fix += step
            i = self.point_fix
        else:
            self.point += step
            i = self.point
        close_list = self.day_1ktable.iloc[i:i+self.inspect_bars, COL_END]
        ma5_list = self.day_1ktable.iloc[i:i+self.inspect_bars, COL_MA5]
        ma10_list = self.day_1ktable.iloc[i:i+self.inspect_bars, COL_MA10]
        ma20_list = self.day_1ktable.iloc[i:i+self.inspect_bars, COL_MA20]
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



    def cal_single_distance(self, close_list, ma5_list, ma10_list, ma20_list, close_list_fix, ma5_list_fix, ma10_list_fix, ma20_list_fix, inspect_bars=7):
        length = inspect_bars
        sum = 0
        weigh=[0.6,0.6,0.8,1,1,2,2]
        for i in range(0, length):
            index = self.point + i
            index_fix = self.point_fix + i
            tmp = 0
            tmp += (close_list[index] - close_list_fix[index_fix]) * (close_list[index] - close_list_fix[index_fix])
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
        close_list_fix = self.close_list_fix
        ma5_list_fix = self.ma5_list_fix
        ma10_list_fix = self.ma10_list_fix
        ma20_list_fix = self.ma20_list_fix
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
        for i in range(1, move_len):
            close_list += 1
            ma5_list += 1
            ma10_list += 1
            ma20_list += 1
            tmp_distance = self.cal_single_distance(close_list, ma5_list, ma10_list, ma20_list, close_list_fix, ma5_list_fix, ma10_list_fix, ma20_list_fix)
            if tmp_distance < distance_min:
                distance_min = tmp_distance
        self.distance = distance_min


    def set_ret(self, ret):
        self.day_1ktable.iloc[self.point, COL_RET] = ret
        self.dbop.dbop_update_day_data_trade_mark(self.db,ret,date,num)

    def get_ret(self):
        return self.day_1ktable.iloc[self.point, COL_RET]



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





if __name__ == "__main__":
#    Usage
    test = daytest()
    test.init_db()
    date = "20171115"
    # Enable following two lines to import data
    #test.import_dayk(date)
    #os._exit(0)

    #file_full_path = filename_prefix + date + filename_postfix
    #test.init_data_from_file(file_full_path)
    test.import_dayk_from_DB(date)

    test.init_compare_data()
    root = Tk()
    f = Figure(figsize=(5,4),dpi=100)
    f_plot = f.add_subplot(211 )
    f_plot2 = f.add_subplot(212 )
    canvs = FigureCanvasTkAgg(f, root)
    canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    Button(root, text='Next', command=lambda: get_dataset(test, f_plot, 1)).pack()
    Button(root, text='Before', command=lambda: get_dataset(test, f_plot, -1)).pack()
    Button(root, text='Next>>', command=lambda: get_dataset(test, f_plot, 10)).pack()
    Button(root, text='<<Before', command=lambda: get_dataset(test, f_plot, -10)).pack()
    Button(root, text='Start Up', command=lambda: set_ret_start_up(test)).pack()
    Button(root, text='Other', command=lambda: set_ret_other(test)).pack()
    mytext = Text(root, width=50, height = 10)
    mytext.pack()
    refresh_text(mytext, test)

    Button(root, text='Next2', command=lambda: get_dataset(test, f_plot2, 1, 0)).pack()
    Button(root, text='Before2', command=lambda: get_dataset(test, f_plot2, -1, 0)).pack()
    Button(root, text='Next2>>', command=lambda: get_dataset(test, f_plot2, 10, 0)).pack()
    Button(root, text='<<Before2', command=lambda: get_dataset(test, f_plot2, -10, 0)).pack()
    #Button(root, text='Start Up2', command=lambda: set_ret_start_up(test)).pack()
    #Button(root, text='Other2', command=lambda: set_ret_other(test)).pack()
    mytext2 = Text(root)
    mytext2.pack()
    refresh_text(mytext2, test)

    root.mainloop()
