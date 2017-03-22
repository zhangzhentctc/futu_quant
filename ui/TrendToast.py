from tkinter import *
from sample import *
from strategies.ma.detectSignal import *

class TrendToast:
    def __init__(self,detectMATrend):
        # Init tk
        self.detectMATrend = detectMATrend
        self.delay = 200
        self.top = Tk()
        self.text = Text(self.top)
        self.text.pack(expand=1, fill='both')

    def display(self):
        self.__show(self.text,)
        self.top.mainloop()

    def __show(self,text):
        text.delete(1.0, 'end')
        ret = self.detectMATrend.get_ma_trend()
        ma10_rate, ma20_rate = self.detectMATrend.get_ma_ch_rate()
        gap = self.detectMATrend.get_ma_cur_gap()
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
        ch_rate = "\nMA10 " + str(ma10_rate) + "\n" + "MA20 " + str(ma20_rate)
        gap = "\nGap: " + str(gap)
        text.insert('end', val + ch_rate + gap)
        text.after(self.delay, self.__show, text)