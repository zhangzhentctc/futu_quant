import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from tkinter import *
import threading
import random
import time

# 因为update的参数是调用函数data_gen,所以第一个默认参数不能是framenum
class view:
    def __init__(self, gen):
        self.gen = gen
        self.root = Tk()
        self.f = Figure(figsize=(5, 4), dpi=100)
        self.plot_big_quo = self.f.add_subplot(111)
        self.canvs = FigureCanvasTkAgg(self.f, self.root)
        self.canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def update(self,data):
        #self.bar1.set_ydata(self.data_y)
        #self.bar1.set_xdata(self.data_x)

        if self.gen.mutex_lock.acquire(1):
            self.price_pos = self.gen.get_prices()
            self.price_vol = self.gen.get_vol()
            self.bar1 = self.plot_big_quo.barh(self.price_pos, self.price_vol, height=0.3, align='center', alpha=0.4)
            #self.bar1.set_xdata(self.price_pos)
            #self.bar1.set_ydata(self.price_vol)
        self.gen.mutex_lock.release()
        return self.bar1,

    def init_view(self):
        self.price_pos = [30019, 30020, 30021, 30022, 30023, 30024, 30025, 30026, 30027, 30028, 30029, 30030, 30031, 30032, 30033, 30034, 30035, 30036, 30037, 30038, 30039, 30040, 30041, 30042, 30043, 30044, 30045, 30046, 30047, 30048, 30049, 30050, 30051, 30052, 30053, 30054, 30055, 30056, 30057, 30058, 30059, 30060, 30061, 30062, 30063, 30064, 30065, 30066, 30067, 30068]
        self.price_vol = [55, 77, 52, 51, 63, 84, 96, 67, 94, 85, 87, 70, 98, 92, 93, 70, 95, 62, 74, 59, 55, 85, 54, 80, 64, 60, 53, 54, 63, 62, 89, 74, 93, 61, 89, 87, 68, 95, 100, 70, 56, 64, 93, 53, 97, 57, 94, 75, 67, 90]
        self.bar1 = self.plot_big_quo.barh(self.price_pos, self.price_vol, height=0.1, align='center', alpha=0.4)

    def view_start(self):
        ani = animation.FuncAnimation(self.f, self.update, interval=2 * 1000)
        self.canvs.draw()
        self.root.mainloop()

class Gen_data(threading.Thread):
    def __init__(self):
        super(Gen_data, self).__init__()
        self.vol_l = []
        self.prices_l = []
        self.mutex_lock = threading.Lock()


    def get_prices(self):
        return self.prices_l

    def get_vol(self):
        return self.vol_l

    def run(self):
        while True:
            if self.mutex_lock.acquire(1):
                min_price = random.randint(30000, 30100)
                for i in range(0, 50):
                    self.vol_l.append(random.randint(50, 100))
                    self.prices_l.append(min_price + i)

            self.mutex_lock.release()
            time.sleep(0.5)










gen = Gen_data()
gen.start()
v = view(gen)
v.init_view()
v.view_start()