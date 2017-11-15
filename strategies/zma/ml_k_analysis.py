from db.db_ma_trend import *
#from openft.open_quant_context import *
import pandas as pd
import time
import math
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

    def Initialize(self):
        self.db = MySQLCommand("localhost", 3306, "root", "123456", "trend2")
        self.db.connectMysql()
        self.op = dbop_ma_trand()
        self.mydb = MySQLCommand("localhost", 3306, "root", "123456", "day_review_01")
        self.mydb.connectMysql()
        self.myop = dbop_ma_trand()

    def del_head_data(self):
        for i in range(0,20):
            self.day_1ktable.drop(i,inplace=True)

    def init_data_from_file(self, filename):
        self.day_1ktable = pd.read_csv(filename)
        self.day_1ktable['ma5']= 0
        self.day_1ktable['ma10'] = 0
        self.day_1ktable['ma20'] = 0
        self.day_1ktable['ret'] = 0
        self.cal_MAn(5)
        self.cal_MAn(10)
        self.cal_MAn(20)

        close_list = self.day_1ktable.iloc[self.point:self.point + 7, COL_END]
        ma5_list = self.day_1ktable.iloc[self.point:self.point + 7, COL_MA5]
        ma10_list = self.day_1ktable.iloc[self.point:self.point + 7, COL_MA10]
        ma20_list = self.day_1ktable.iloc[self.point:self.point + 7, COL_MA20]
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

    def cal_MAn(self, n):
        if n == 5:
            ncolum = COL_MA5
        elif n == 10:
            ncolum = COL_MA10
        elif n == 20:
            ncolum = COL_MA20
        else:
            return -1

        length = len(self.day_1ktable.index)
        for i in range(n - 1, length):
            tmp = 0
            for j in range(0, n):
                tmp += self.day_1ktable.iloc[i - j, COL_END]
            ma_n = tmp / n
            ma_n = round(ma_n, 2)
            self.day_1ktable.iloc[i, ncolum] = ma_n
        return 0

    def get_next_data(self, type = 1, inspect_bars=7):
        if type == 0:
            self.point_fix += 1
            i = self.point_fix
        else:
            self.point += 1
            i = self.point
        close_list = self.day_1ktable.iloc[i:i+inspect_bars, COL_END]
        ma5_list = self.day_1ktable.iloc[i:i+inspect_bars, COL_MA5]
        ma10_list = self.day_1ktable.iloc[i:i+inspect_bars, COL_MA10]
        ma20_list = self.day_1ktable.iloc[i:i+inspect_bars, COL_MA20]
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


    def get_before_data(self, type = 1, inspect_bars=7):
        if type == 0:
            self.point_fix -= 1
            i = self.point_fix
        else:
            self.point -= 1
            i = self.point

        close_list = self.day_1ktable.iloc[i:i+inspect_bars, COL_END]
        ma5_list = self.day_1ktable.iloc[i:i+inspect_bars, COL_MA5]
        ma10_list = self.day_1ktable.iloc[i:i+inspect_bars, COL_MA10]
        ma20_list = self.day_1ktable.iloc[i:i+inspect_bars, COL_MA20]
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

        data = []
        #for i in range(0,7):


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

    def get_ret(self):
        return self.day_1ktable.iloc[self.point, COL_RET]


def norm_matrix(matrix):
    pass



def get_next_dataset(data_handler, plot, type = 1):
    plot.clear()
    if type == 0:
        data_handler.get_next_data(0)
        plot.plot(data_handler.close_list_fix)
        plot.plot(data_handler.ma5_list_fix)
        plot.plot(data_handler.ma10_list_fix)
        plot.plot(data_handler.ma20_list_fix)
    else:
        data_handler.get_next_data()
        plot.plot(data_handler.close_list)
        plot.plot(data_handler.ma5_list)
        plot.plot(data_handler.ma10_list)
        plot.plot(data_handler.ma20_list)
    plot.set_ylim(0, 100)
    canvs.draw()

def get_before_dataset(data_handler, plot, type = 1):
    plot.clear()
    if type == 0:
        data_handler.get_before_data(0)
        plot.plot(data_handler.close_list_fix)
        plot.plot(data_handler.ma5_list_fix)
        plot.plot(data_handler.ma10_list_fix)
        plot.plot(data_handler.ma20_list_fix)
    else:
        data_handler.get_before_data()
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
    test.init_data_from_file("/Users/aaron/ret_1dayk_1020.csv")

    root = Tk()
    f = Figure(figsize=(5,4),dpi=100)
    f_plot = f.add_subplot(211 )
    f_plot2 = f.add_subplot(212 )
    canvs = FigureCanvasTkAgg(f, root)
    canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    Button(root, text='Next', command=lambda: get_next_dataset(test, f_plot)).pack()
    Button(root, text='Before', command=lambda: get_before_dataset(test, f_plot)).pack()
    Button(root, text='Start Up', command=lambda: set_ret_start_up(test)).pack()
    Button(root, text='Other', command=lambda: set_ret_other(test)).pack()
    mytext = Text(root, width=50, height = 10)
    mytext.pack()
    refresh_text(mytext, test)

    Button(root, text='Next2', command=lambda: get_next_dataset(test, f_plot2, 0)).pack()
    Button(root, text='Before2', command=lambda: get_before_dataset(test, f_plot2, 0)).pack()
    Button(root, text='Start Up2', command=lambda: set_ret_start_up(test)).pack()
    Button(root, text='Other2', command=lambda: set_ret_other(test)).pack()
    mytext2 = Text(root)
    mytext2.pack()
    refresh_text(mytext2, test)

    root.mainloop()
