import matplotlib
from strategies.ml.comparer.sample_dayk_comparer import *
from strategies.ml.data_handler.dayk_handler import *
from strategies.ml.data_handler.sample_handler import *

from strategies.ml.comparer.inter_comparer import *

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *



class sample_tester:
    def __init__(self):
        self.distance_t = 30
        self.date_list = ["20171019", "20171020", "20171115", "20171116", "20171117"]
        self.test_ret = []

    def auto_test_sample(self):
        test_ret = []
        samp_h = sample_handler()
        samp_h.prepare_samples()

        for date in self.date_list:
            dayk = dayk_handler(date)
            dayk.prepare_dayk()
            dayk.reset_ret()
            sp_comp = sample_dayk_comparer(dayk, samp_h)
            sp_comp.init_compare_data()
            sp_comp.get_sample(2)

            for i in range(0, samp_h.length):
                for j in range(19, dayk.length - sp_comp.inspect_bars):
                    if sp_comp.distance < self.distance_t:
                        sp_comp.set_ret(self.distance_t)
                        print("set: ", date, " num:", sp_comp.point)
                        test_ret.append([date, sp_comp.point, sp_comp.distance, 0, 0])
                    sp_comp.get_data(1)
                #sp_comp.get_sample(1)
        self.test_ret = test_ret


##############################################################


class whatthefuck:
    def __init__(self):
        self.cnt = 0
        self.string = ""

    def add_x(self, x):
        self.cnt += x

    def assign(self, val):
        self.cnt = val


class test_ret_viewer:
    def __init__(self, tester):
        self.wtf1 = whatthefuck()
        self.wtf2 = whatthefuck()
        self.tester = tester

    def __init_frame(self):
        self.root = Tk()
        self.f = Figure(figsize=(5, 4), dpi=100)
        self.all_plot = self.f.add_subplot(211)
        self.f_plot = self.f.add_subplot(212)
        self.canvs = FigureCanvasTkAgg(self.f, self.root)
        self.canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def __init_button(self):
        Button(self.root, text='BigNext->', command=lambda: self.show_big_dia( 1)).pack()
        Button(self.root, text='<-BigBack', command=lambda: self.show_big_dia(-1)).pack()
        Button(self.root, text='Next->', command=lambda: self.show_result(1)).pack()
        Button(self.root, text='<-Back', command=lambda: self.show_result(-1)).pack()

    def __init_text(self):
        mytext = Text(self.root, width=50, height=5)
        mytext.pack()
        self.__refresh_ret_text(mytext, self.wtf1)

    def __refresh_ret_text(self, text, wtf):
        string = wtf.string
        text.delete(1.0, 'end')
        text.insert('end', string)
        text.after(100, self.__refresh_ret_text, text, wtf)

    def init_viwer(self):
        self.__init_frame()
        self.__init_button()
        self.__init_text()

    def start_viewer(self):
        self.root.mainloop()

    ### Show Day All
    def show_big_dia(self, step):
        if self.wtf1.cnt + step > len(self.tester.date_list) - 1 or self.wtf1.cnt + step < 0:
            return
        self.wtf1.add_x(step)
        day = self.tester.date_list[self.wtf1.cnt]
        dayk = dayk_handler()
        dayk.init_db()
        dayk.import_dayk_from_DB(day)
        self.all_plot.clear()
        self.all_plot.plot(dayk.day_1ktable.iloc[19:, COL_END])
        self.all_plot.plot(dayk.day_1ktable.iloc[19:, COL_MA5])
        self.all_plot.plot(dayk.day_1ktable.iloc[19:, COL_MA10])
        self.all_plot.plot(dayk.day_1ktable.iloc[19:, COL_MA20])
        for i in range(19, dayk.length - dayk.inspect_bars):
            if dayk.day_1ktable.iloc[i, COL_RET] == self.tester.distance_t:
                self.all_plot.annotate(
                    "BUY",
                    xy=(i + dayk.inspect_bars, dayk.day_1ktable.iloc[i + dayk.inspect_bars, COL_END]),
                    xytext=(i + dayk.inspect_bars, dayk.day_1ktable.iloc[i + dayk.inspect_bars, COL_END] + 50),
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2")
                )
        self.canvs.draw()


    ## Show 1 unit
    def show_result(self, step):
        if self.wtf2.cnt + step > len(self.tester.test_ret) - 1 or self.wtf2.cnt + step < 0:
            return
        print("TEST RET:", self.tester.test_ret)
        self.wtf2.add_x(step)
        self.wtf2.string = "Day: " +                     str(self.tester.test_ret[self.wtf2.cnt][0]) + \
                           " Num: " +                    str(self.tester.test_ret[self.wtf2.cnt][1]) + \
                           "\nDistance: " +              str(self.tester.test_ret[self.wtf2.cnt][2]) + \
                           "\nCompared with: \nDate: " + str(self.tester.test_ret[self.wtf2.cnt][3]) + \
                           "\nNum : " +                  str(self.tester.test_ret[self.wtf2.cnt][4])
        day = self.tester.test_ret[self.wtf2.cnt][0]
        num = self.tester.test_ret[self.wtf2.cnt][1]
        self.__show_unit_plot(day, num)

    def __show_unit_plot(self, day, num):
        dayk = dayk_handler()
        dayk.init_db()
        dayk.import_dayk_from_DB(day)
        comp = inter_comparer(dayk, dayk)
        comp.init_compare_data()
        comp.move_data(num)
        comp.sudo_move(1)
        self.f_plot.clear()
        self.f_plot.plot(comp.close_list_show)
        self.f_plot.plot(comp.ma5_list_show)
        self.f_plot.plot(comp.ma10_list_show)
        self.f_plot.plot(comp.ma20_list_show)
        self.f_plot.annotate(
            "BUY",
            xy=(num + dayk.inspect_bars - 1, 10),
            xytext=(num + dayk.inspect_bars - 1, 10 + 50),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2")
        )
        self.f_plot.set_ylim(0, 100)
        self.canvs.draw()


if __name__ == "__main__":
#    Usage
    tester = sample_tester()
    tester.auto_test_sample()
    viewer = test_ret_viewer(tester)
    viewer.init_viwer()
    viewer.start_viewer()

