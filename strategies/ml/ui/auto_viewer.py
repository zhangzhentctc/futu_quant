import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *

import pandas as pd
from strategies.ml.ui.whatthefuck import *
from strategies.ml.data_handler.dayk_handler import *
from strategies.ml.simulator.sample_simulator import *

class auto_viewer:
    def __init__(self, ui_ret, date_list):
        self.wtf1 = whatthefuck()
        self.wtf2 = whatthefuck()
        self.ui_ret = ui_ret
        self.date_list = date_list

    def __init_frame(self):
        self.root = Tk()
        self.f = Figure(figsize=(5, 4), dpi=100)
        self.plot_big_quo = self.f.add_subplot(311)
        self.plot_small_quo = self.f.add_subplot(323)
        self.plot_small_sap = self.f.add_subplot(324)
        self.plot_comp = self.f.add_subplot(337)
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
        self.__refresh_ret_text(mytext, self.wtf2)

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
        self.show_big_quote(0)
        self.canvs.draw()

        self.wtf2.string = str(self.ui_ret[0][3])
        self.plot_small_quo.clear()
        self.plot_small_quo.plot()
        self.show_small_quote(0)
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
        day = self.date_list[self.wtf1.cnt]

        self.plot_day_quo(day)


    def plot_unit_quo(self, day, num):
        dayk = dayk_handler(day)
        dayk.prepare_dayk()
        self.plot_small_quo.clear()
        self.plot_small_quo.plot(dayk.day_1ktable.iloc[num + 2:num + 7 + 10, COL_END ])
        self.plot_small_quo.plot(dayk.day_1ktable.iloc[num + 2:num + 7 + 10, COL_MA5 ])
        self.plot_small_quo.plot(dayk.day_1ktable.iloc[num + 2:num + 7 + 10, COL_MA10])
        self.plot_small_quo.plot(dayk.day_1ktable.iloc[num + 2:num + 7 + 10, COL_MA20])
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

    def plot_samp(self, sap_id):
        s_si = sample_simulator()
        s_si.prepare_sample_simulator()

        if s_si.move_to_id(sap_id) == -1:
            return

        pd_sap_data = self.__format_kbars2plot(s_si.ret_data)
        self.plot_small_sap.clear()
        self.plot_small_sap.plot(pd_sap_data)
        self.canvs.draw()

    def plot_voice(self):
        voice_data = [
            self.ui_ret[self.wtf2.cnt][15],
            self.ui_ret[self.wtf2.cnt][14],
            self.ui_ret[self.wtf2.cnt][13],
            self.ui_ret[self.wtf2.cnt][12],
            self.ui_ret[self.wtf2.cnt][11],
            self.ui_ret[self.wtf2.cnt][10],
            self.ui_ret[self.wtf2.cnt][9]
        ]
        data = []
        for i in range(0, len(voice_data)):
            data.append({
                "1": voice_data[i],"2": 10, "3":8
            })
        pd_data = pd.DataFrame(data, columns=["1","2","3"])
        self.plot_comp.clear()
        self.plot_comp.plot(pd_data)
        self.plot_comp.set_ylim(0, 20)
        self.canvs.draw()

    ## Show Sample
    def show_small_quote(self, step):
        if self.wtf2.cnt + step > len(self.ui_ret) - 1 or self.wtf2.cnt + step < 0:
            return
        self.wtf2.add_x(step)
        self.wtf2.string = str(self.ui_ret[self.wtf2.cnt][3])  + \
                           "\nclose:" + str(self.ui_ret[self.wtf2.cnt][5]) + \
                           " ma5:" + str(self.ui_ret[self.wtf2.cnt][6]) + \
                           " ma10:" + str(self.ui_ret[self.wtf2.cnt][7]) + \
                           " ma20:" + str(self.ui_ret[self.wtf2.cnt][8]) + \
                           "\n" + \
                           "" + str(self.ui_ret[self.wtf2.cnt][13]) + \
                           " " + str(self.ui_ret[self.wtf2.cnt][12]) + \
                           " " + str(self.ui_ret[self.wtf2.cnt][11]) + \
                           " " + str(self.ui_ret[self.wtf2.cnt][10]) + \
                           " " + str(self.ui_ret[self.wtf2.cnt][9])






        day = self.ui_ret[self.wtf2.cnt][0]
        num = self.ui_ret[self.wtf2.cnt][1]
        self.plot_unit_quo(day, num)
        sap_id = self.ui_ret[self.wtf2.cnt][4]
        self.plot_samp(sap_id)
        self.plot_voice()

    def prepare_viewer(self):
        self.init_viwer()
        self.init_plots()
        self.start_viewer()

    def __format_kbars2plot(self, cp_data):
        data = []
        for i in range(0, 7):
            data.append({
                "1": cp_data[i][0], "2": cp_data[i][1], "3": cp_data[i][2], "4": cp_data[i][3]
            })
        pd_data = pd.DataFrame(data, columns=["1", "2", "3", "4"])
        return pd_data