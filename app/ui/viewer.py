import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import matplotlib.animation as animation
from app.db.ticker_handler import *


class viewer:
    def __init__(self, ticker_h):
        self.ticker_h = ticker_h


    def __init_bars(self):
        self.root = Tk()
        self.f = Figure(figsize=(5, 4), dpi=100)
        self.plot_bar_buy = self.f.add_subplot(131)
        self.plot_bar_neul = self.f.add_subplot(132)
        self.plot_bar_sell = self.f.add_subplot(133)
        self.canvs = FigureCanvasTkAgg(self.f, self.root)
        self.canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def __init_controller(self):
        Button(self.root, text='10s  ->', command=lambda: self.__refresh_bars(10)).pack()
        Button(self.root, text='10s  <-', command=lambda: self.__refresh_bars(-10)).pack()
        Button(self.root, text='1Min ->>', command=lambda: self.__refresh_bars(60)).pack()
        Button(self.root, text='1Min <<-', command=lambda: self.__refresh_bars(-60)).pack()
        self.btn_starter = Button(self.root, text='Input Start Time', command=self.__get_start_time).pack()
        self.eny_starter = Entry(self.root, show=None)
        self.eny_starter.pack()
        Button(self.root, text='reset', command=lambda: self.__refresh_bars(-60)).pack()

    def __get_start_time(self):
        self.start_time = self.eny_starter.get()
        self.ticker_h.set_start(self.start_time)


    def init_viewer(self):
        self.__init_bars()
        self.__init_controller()

    def start_viewer(self):
        self.__refresh_bars(60)
        self.canvs.draw()
        self.root.mainloop()

    def set_auto_refresh(self):
        ani = animation.FuncAnimation(self.f, self.__refresh_bars, interval=1 * 1000)

    def __refresh_bars(self, step):
        self.__get_next_bar_data(step)
        #self.plot_bar_buy.clear()
        self.plot_bar_buy.barh(self.data_prices_l, self.data_buy_l, height=0.1, align='center', alpha=0.4)
        #self.plot_bar_neul.clear()
        self.plot_bar_neul.barh(self.data_prices_l, self.data_neul_l, height=0.1, align='center', alpha=0.4)
        #self.plot_bar_sell.clear()
        self.plot_bar_sell.barh(self.data_prices_l, self.data_sell_l, height=0.1, align='center', alpha=0.4)

    def __get_next_bar_data(self, step):
        self.ticker_h.move_end_ptr(step)
        self.ticker_h.gen_data()

        self.data_prices_l = self.ticker_h.price_l
        self.data_buy_l = self.ticker_h.buy_l
        self.data_neul_l = self.ticker_h.neul_l
        self.data_sell_l = self.ticker_h.sell_l


ticker_h = ticker_handler()
ticker_h.init_db()
ticker_h.import_tickers_from_db()

v = viewer(ticker_h)
v.init_viewer()
#v.set_auto_refresh()
v.start_viewer()
