import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *

import pandas as pd
from strategies.ml.ui.whatthefuck import *
from strategies.ml.data_handler.dayk_handler import *

class auto_viewer:
    def __init__(self, ui_ret, date_list):
        self.wtf1 = whatthefuck()
        self.wtf2 = whatthefuck()
        self.ui_ret = ui_ret
        self.date_list = date_list

    def __init_frame(self):
        self.root = Tk()
        self.f = Figure(figsize=(5, 4), dpi=100)
        self.plot_big_quo = self.f.add_subplot(211)
        self.plot_small_quo = self.f.add_subplot(212)
        self.canvs = FigureCanvasTkAgg(self.f, self.root)
        self.canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def __init_button(self):
        Button(self.root, text='BigNext->', command=lambda: self.show_big_quote(1)).pack()
        Button(self.root, text='<-BigBack', command=lambda: self.show_big_quote(-1)).pack()
        Button(self.root, text='Next->', command=lambda: self.show_small_quote(1)).pack()
        Button(self.root, text='<-Back', command=lambda: self.show_small_quote(-1)).pack()

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

    def init_plots(self):

        self.plot_big_quo.clear()
        self.plot_big_quo.plot()
        self.canvs.draw()


        self.wtf1.string = str(self.ui_ret[0][3])
        self.plot_small_quo.clear()
        self.plot_small_quo.plot()
        self.canvs.draw()

    def plot_day_quo(self, day):
        dayk = dayk_handler(day)
        dayk.prepare_dayk()
        self.plot_big_quo.clear()
        self.plot_big_quo.plot(dayk.day_1ktable.iloc[19:, COL_END])
        self.plot_big_quo.plot(dayk.day_1ktable.iloc[19:, COL_MA5])
        self.plot_big_quo.plot(dayk.day_1ktable.iloc[19:, COL_MA10])
        self.plot_big_quo.plot(dayk.day_1ktable.iloc[19:, COL_MA20])

        for i in range(0, len(self.ui_ret)):
            if day == self.ui_ret[i][0]:
                self.plot_big_quo.annotate(
                    "BUY " +  str(self.ui_ret[i][2]),
                    xy=(self.ui_ret[i][1] + dayk.inspect_bars,
                        dayk.day_1ktable.iloc[self.ui_ret[i][1] + dayk.inspect_bars, COL_END]),
                    xytext=(self.ui_ret[i][1] + dayk.inspect_bars,
                            dayk.day_1ktable.iloc[self.ui_ret[i][1] + dayk.inspect_bars, COL_END] + 50),
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.1")
                )
        self.canvs.draw()
        return

    ### Show Quote
    def show_big_quote(self, step):
        if self.wtf1.cnt + step > len(self.date_list) - 1 or self.wtf1.cnt + step < 0:
            return
        self.wtf1.add_x(step)
        self.wtf1.string = str(self.ui_ret[0][3])
        day = self.date_list[self.wtf1.cnt]

        self.plot_day_quo(day)


    def plot_unit_quo(self, day, num):
        dayk = dayk_handler(day)
        dayk.prepare_dayk()
        self.plot_small_quo.clear()
        self.plot_small_quo.plot(dayk.day_1ktable.iloc[num:num + 7 + 10, COL_END ])
        self.plot_small_quo.plot(dayk.day_1ktable.iloc[num:num + 7 + 10, COL_MA5 ])
        self.plot_small_quo.plot(dayk.day_1ktable.iloc[num:num + 7 + 10, COL_MA10])
        self.plot_small_quo.plot(dayk.day_1ktable.iloc[num:num + 7 + 10, COL_MA20])
        self.plot_small_quo.annotate(
            "BUY " + str(self.ui_ret[self.wtf2.cnt][2]),
            xy=(self.ui_ret[self.wtf2.cnt][1] + dayk.inspect_bars,
                dayk.day_1ktable.iloc[self.ui_ret[self.wtf2.cnt][1] + dayk.inspect_bars, COL_END]),
            xytext=(self.ui_ret[self.wtf2.cnt][1] + dayk.inspect_bars,
                    dayk.day_1ktable.iloc[self.ui_ret[self.wtf2.cnt][1] + dayk.inspect_bars, COL_END] + 5),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.1")
        )
        self.canvs.draw()
        return

    ## Show Sample
    def show_small_quote(self, step):
        if self.wtf2.cnt + step > len(self.ui_ret) - 1 or self.wtf2.cnt + step < 0:
            return
        self.wtf2.add_x(step)
        self.wtf1.string = str(self.ui_ret[0][3])
        day = self.ui_ret[self.wtf2.cnt][0]
        num = self.ui_ret[self.wtf2.cnt][1]
        self.plot_unit_quo(day, num)

    def prepare_viewer(self):
        self.init_viwer()
        self.init_plots()
        self.start_viewer()

