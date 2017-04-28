from data_src.stock_info.get_stock_quote import *
import threading
import time
import pandas as pd

NO_POS = 0
CUR_POS = 1
TIME_POS = 2
ZMA10_POS = 3
ZMA20_POS = 4
ZMA10_RATIO_POS = 5
ZMA20_RATIO_POS = 6
ZMA20_RATIO_RATIO_POS = 7
ZMA_GAP_POS = 8
ZMA_GAP_RATIO_POS = 9
ZMA_GAP_RATIO_RATIO_POS = 10


class zma20_strategy_quote(threading.Thread):
    def __init__(self, qc, interval = 0.5):
        super(zma20_strategy_quote, self).__init__()
        self.__quote_ctx = qc
        self.ret= []
        self.interval = 0.5
        self.count = 0
        self.is_available = 0
        data= []
        for i in range(0, 50000):
            data.append({"No.": 0})
        self.ret = pd.DataFrame(data, columns=["No.", "cur", "time", "zma10", "zma20", "zma10_ratio", "zma20_ratio",
                                               "zma20_ratio_ratio", "zma_gap", "zma_gap_ratio", "zma_gap_ratio_ratio"])

    ## MA
    def cal_zma10(self, position):
        len = 1200
        sum = 0
        if position < len - 1:
            return -1
        if position == len - 1:
            for j in range(0, len):
                sum += self.ret["cur"][len - 1 - j]
            avr0 = sum / len
            self.ret.iloc[position, ZMA10_POS] = avr0
            return 1
        starter = self.ret["cur"][position - len ]
        avr = self.ret["zma10"][position - 1 ] - starter/len + self.ret["cur"][position]/len
        self.ret.iloc[position, ZMA10_POS] = avr
        return 0

    def cal_zma20(self, position):
        len = 2400
        sum = 0
        if position < len - 1:
            return -1
        if position == len - 1:
            for j in range(0, len):
                sum += self.ret["cur"][len - 1 - j]
            avr0 = sum / len
            self.ret.iloc[position, ZMA20_POS] = avr0
            return 1
        starter = self.ret["cur"][position - len ]
        avr = self.ret["zma20"][position - 1 ] - starter/len + self.ret["cur"][position]/len
        self.ret.iloc[position, ZMA20_POS] = avr
        return 0

    ## MA Ratio
    def cal_zma10_ratio(self, position):
        len = 1200
        t = 60
        val =0
        start_pos = len + t
        if position < start_pos:
          return -1

        ret, val = self.optimized_least_square_method(position - t + 1, position, "zma10")
        if ret == -1:
            val = 0
        self.ret.iloc[position, ZMA10_RATIO_POS] = val
        return 1

    def cal_zma20_ratio(self, position):
        len = 2400
        t = 60
        val =0
        start_pos = len + t
        if position < start_pos:
          return -1
        ret, val = self.optimized_least_square_method(position - t + 1, position, "zma20")
        if ret == -1:
            val = 0
        self.ret.iloc[position, ZMA20_RATIO_POS] = val
        return 1

    def cal_zma20_ratio_ratio(self, position):
        len = 2400
        t = 240
        val =0
        start_pos = len + t + 60
        if position < start_pos:
          return -1

        ret, val = self.optimized_least_square_method(position - t + 1, position, "zma20_ratio")
        if ret == -1:
            val = 0
        self.ret.iloc[position, ZMA20_RATIO_RATIO_POS] = val
        return 1

    ## MA GAP
    def cal_zma_gap(self, position):
        len = 2400
        start_pos = len + 1
        if position < start_pos:
            return -1

        val = self.ret["zma10"][position] - self.ret["zma20"][position]
        self.ret.iloc[position, ZMA_GAP_POS] = val
        return 1

    def cal_zma_gap_ratio(self, position):
        len = 2400
        t = 240
        val =0
        start_pos = len + t + 1
        if position < start_pos:
          return -1

        ret, val = self.optimized_least_square_method(position - t + 1, position, "zma_gap")
        if ret == -1:
            val = 0
        self.ret.iloc[position, ZMA_GAP_RATIO_POS] = float(val)
        return 1

    def cal_zma_gap_ratio_ratio(self, position):
        len = 1200
        t = 180
        val =0
        start_pos = len + t + 240 + 1
        if position < start_pos:
          return -1

        ret, val = self.optimized_least_square_method(position - t + 1, position, "zma_gap_ratio")
        if ret == -1:
            val = 0
        self.ret.iloc[position, ZMA_GAP_RATIO_RATIO_POS] = val
        return 1

    def optimized_least_square_method(self, start, end, column):
        A = 0
        B = 0
        xi = 0
        t = end - start + 1
        avr_x = 0
        avr_y = 0
        if self.count < start:
            return -1, 0
        B = (t - 1) * t
        B /= 2
        for i in range(start, end + 1):
            cur = self.ret[column][i]
            A += xi * cur
            avr_x += xi / t
            avr_y += cur/t
            xi += 1
        M = t * avr_x
        ratio = (A - M * avr_y) / (B - M * avr_x)
        return 1, ratio

    def is_trade_time(self, data_time):
        return 1
        if data_time > "9:30:00" and data_time < "12;00:00":
            print("time ok" + str(data_time))
            return 1
        if data_time > "14:00:00" and data_time < "16;00:00":
            print("time ok" + str(data_time))
            return 1
        print("time not ok" + str(data_time))
        return 0

    def get_cur_zma_quote(self):
        if self.count <= 1:
            return RET_ERROR, ""
        pos = self.count - 1
        data = []
        data.append({"No.": self.ret.iloc[pos, NO_POS], "cur": self.ret.iloc[pos, CUR_POS], "time": self.ret.iloc[pos, TIME_POS],
                     "zma10": self.ret.iloc[pos, ZMA10_POS], "zma20": self.ret.iloc[pos, ZMA20_POS],
                     "zma10_ratio": self.ret.iloc[pos, ZMA10_RATIO_POS], "zma20_ratio": self.ret.iloc[pos, ZMA20_RATIO_POS],"zma20_ratio_ratio": self.ret.iloc[pos, ZMA20_RATIO_RATIO_POS],
                     "zma_gap": self.ret.iloc[pos, ZMA_GAP_POS], "zma_gap_ratio": self.ret.iloc[pos, ZMA_GAP_RATIO_POS], "zma_gap_ratio_ratio": self.ret.iloc[pos, ZMA_GAP_RATIO_RATIO_POS]
                     })
        zma_quote = pd.DataFrame(data,
                             columns=["No.", "cur", "time", "zma10", "zma20", "zma10_ratio", "zma20_ratio",
                                      "zma20_ratio_ratio", "zma_gap", "zma_gap_ratio",
                                      "zma_gap_ratio_ratio"])
        return RET_OK, zma_quote


    def run(self):
        stock_quote = get_stock_quote(self.__quote_ctx)
        stock_quote.start()
        while stock_quote.ready != 1:
            time.sleep(1)

        data_time = stock_quote.get_data_time()
        cur_stock_quoto = stock_quote.get_stock_quoto()

        while(1):
            if self.is_trade_time(data_time) == 1:
                start = time.time()
                self.is_available = 0
                self.count += 1
                self.ret.iloc[self.count, NO_POS] = self.count
                self.ret.iloc[self.count, CUR_POS] = cur_stock_quoto
                self.ret.iloc[self.count, TIME_POS] = data_time
                self.cal_zma10(self.count)
                self.cal_zma20(self.count)
                self.cal_zma10_ratio(self.count)
                self.cal_zma20_ratio(self.count)
                self.cal_zma20_ratio_ratio(self.count)
                self.cal_zma_gap(self.count)
                self.cal_zma_gap_ratio(self.count)
                self.cal_zma_gap_ratio_ratio(self.count)
                self.is_available = 1
                end = time.time()
                dur = end - start
                print(dur)
#                print(self.ret.iloc[[self.count]])
                if dur > self.interval:
                    time.sleep(0)
                else:
                    time.sleep(self.interval - dur)

                # If stock_quote dies. Restart it
                # Use previous Value as Current one
                if stock_quote.is_alive() == False:
                    stock_quote = get_stock_quote(self.__quote_ctx)
                    stock_quote.start()
                if stock_quote.ready == 1:
                    data_time = stock_quote.get_data_time()
                    cur_stock_quoto = stock_quote.get_stock_quoto()
                else:
                    cur_stock_quoto = self.ret.iloc[self.count, CUR_POS]
            else:
                self.is_available = 0
                time.sleep(self.interval)
                data_time = stock_quote.get_data_time()




