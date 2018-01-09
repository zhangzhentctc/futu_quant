import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import matplotlib.animation as animation


class viewer:
    def __init__(self):
        pass


    def __init_bars(self):
        self.root = Tk()
        self.f = Figure(figsize=(5, 4), dpi=100)
        self.plot_bar_buy = self.f.add_subplot(311)
        self.plot_bar_neul = self.f.add_subplot(312)
        self.plot_bar_sell = self.f.add_subplot(313)
        self.canvs = FigureCanvasTkAgg(self.f, self.root)
        self.canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def __init_controller(self):
        pass

    def init_viewer(self):
        self.__init_bars()
        self.__init_controller()

    def start_viewer(self):
        self.canvs.draw()
        self.root.mainloop()

    def set_auto_refresh(self):
        ani = animation.FuncAnimation(self.f, self.__refresh_bars, interval=1 * 1000)

    def __refresh_bars(self):
        self.data_prices_l = [30000, 30000, 30000, 30000, 30000]
        self.data_buy_l = [100, 100, 100, 100, 100]
        self.data_neul_l = [100, 100, 100, 100, 100]
        self.data_sell_l = [100, 100, 100, 100, 100]
        self.plot_bar_buy.clear()
        self.plot_bar_buy.barh(self.data_prices_l, self.data_buy_l, height=0.1, align='center', alpha=0.4)
        self.plot_bar_neul.clear()
        self.plot_bar_neul.barh(self.data_prices_l, self.data_neul_l, height=0.1, align='center', alpha=0.4)
        self.plot_bar_sell.clear()
        self.plot_bar_sell.barh(self.data_prices_l, self.data_sell_l, height=0.1, align='center', alpha=0.4)




