from tkinter import *
from sample import *
from strategies.ma.detectSignal import *

class TrendToast:
    def __init__(self, detectMATrend, detectMATrend5,placer_c, placer_p):
        # Init tk
        self.detectMATrend  = detectMATrend
        self.detectMATrend5 = detectMATrend5
        self.placer_c = placer_c
        self.placer_p = placer_p
        self.delay = 200
        self.top = Tk()
        self.text = Text(self.top)
        self.text.pack(expand=1, fill='both')
        self.button_buy_c = Button(self.top, text = "BUY C on market", command = lambda : placer_c.buy_on_market_price(50000, "68021"))
        self.button_buy_c.pack()
        self.button_sell_c = Button(self.top, text = "SELL C on market", command = lambda : placer_c.sell_on_market_price(50000, "68021"))
        self.button_sell_c.pack()
        self.button_buy_p = Button(self.top, text = "BUY P on market", command = lambda : placer_p.buy_on_market_price(50000, "63850"))
        self.button_buy_p.pack()
        self.button_sell_p = Button(self.top, text = "SELL P on market", command = lambda : placer_p.sell_on_market_price(50000, "63850"))
        self.button_sell_p.pack()

    def display(self):
        self.__show(self.text,)
        self.top.mainloop()

    def get_ma_str(self):
        ma10_rate, ma20_rate = self.detectMATrend.get_ma_ch_rate()
        ma10_rate = round(ma10_rate, 1)
        ma20_rate = round(ma20_rate, 1)
        if ma10_rate >= 0:
            ma10_rate_str = "+" + str(ma10_rate)
        else:
            ma10_rate_str = str(ma10_rate)

        if ma20_rate >= 0:
            ma20_rate_str = "+" + str(ma20_rate)
        else:
            ma20_rate_str = str(ma20_rate)
        ch_rate = "\nDur2: MA10 " + ma10_rate_str + " MA20 " + ma20_rate_str
        return ch_rate

    def get_ma_str_5(self):
        ma10_rate, ma20_rate = self.detectMATrend5.get_ma_ch_rate()
        ma10_rate = round(ma10_rate, 1)
        ma20_rate = round(ma20_rate, 1)
        if ma10_rate >= 0:
            ma10_rate_str = "+" + str(ma10_rate)
        else:
            ma10_rate_str = str(ma10_rate)

        if ma20_rate >= 0:
            ma20_rate_str = "+" + str(ma20_rate)
        else:
            ma20_rate_str = str(ma20_rate)
        ch_rate = "\nDur5: MA10 " + ma10_rate_str + " MA20 " + ma20_rate_str
        return ch_rate

    def __show(self,text):
        text.delete(1.0, 'end')
        ret = self.detectMATrend.get_ma_trend()
        ch_rate = self.get_ma_str()
        ch_rate5 = self.get_ma_str_5()
        gap = self.detectMATrend.get_ma_cur_gap()
        gap = round(gap, 2)
        val_ch_rate = self.detectMATrend.get_ch_rate_val()
        if ret != 0:
            count = self.detectMATrend.count
            if ret == 1:
                val = "Upward"
            else:
                val = "Downward"
            time = count*(self.delay/1000)
            val = val + " " + str(time)
        else:
            val = "Wait"

        val_ch_rate_show = "\nChange Rate: " + str(val_ch_rate)
        gap = "\nGap: " + str(gap)
        text.insert('end', val + ch_rate + ch_rate5 + gap + val_ch_rate_show)
        text.after(self.delay, self.__show, text)