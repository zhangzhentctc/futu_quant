from openft.open_quant_context import *
import threading
import time


class get_stock_quote(threading.Thread):
    def __init__(self, qc, stock_code="HK_FUTURE.999010", cycle= 0.25):
        super(get_stock_quote, self).__init__()
        self.__quote_ctx = qc
        self.stock_code_list = [stock_code]
        self.cur_stock_quoto = 0
        self.cur_stock_quoto_index = "last_price"
        self.data_time = ""
        self.data_time_index = "data_time"
        self.amplitude_index = "amplitude"
        self.cur_amplitude = 0
        self.subscribe_trail = 3
        self.refresh = cycle
        self.ready = 0
        self.deltaMA20_cur = 0
        self.deltaMA20_ma3 = 0
        self.deltaMA20_ma5 = 0

        global ma_1m_table_lock

    def subscribe_stock(self, type):
        # subscribe "QUOTE"
        for stk_code in self.stock_code_list:
            ret_status, ret_data = self.__quote_ctx.subscribe(stk_code, type)
            if ret_status != RET_OK:
                print("%s %s: %s" % (stk_code, "QUOTE", ret_data))
                return RET_ERROR, ret_data
        ret_status, ret_data = self.__quote_ctx.query_subscription()
        if ret_status == RET_ERROR:
            print(ret_status)
            return RET_ERROR, ret_data
        return RET_OK, ret_data

    def get_cur_stock_quoto(self):
        ret_status, ret_data = self.__quote_ctx.get_stock_quote(self.stock_code_list)
        if ret_status == RET_ERROR:
            return RET_ERROR
        quote_table = ret_data
        val = quote_table[self.cur_stock_quoto_index][0]
        cur_time = quote_table[self.data_time_index][0]
        cur_amplitude = quote_table[self.amplitude_index][0]
        if val == 0:
            print("Get Val = 0 skip")
            return RET_ERROR
        self.cur_stock_quoto = val
        self.data_time = cur_time
        self.cur_amplitude = cur_amplitude
        return RET_OK

    def get_data_time(self):
        return self.data_time

    def get_stock_quoto(self):
        return self.cur_stock_quoto

    def get_stock_amplitude(self):
        return self.cur_amplitude

    def get_1mK_line(self):
        ret = 0
        try:
            table = self.ma_1m_table
            ret = 1
        except:
            ret = 0
            table = []
        return ret, table

    def get_ma_1m(self, number):
        stock_code_list = ["HK_FUTURE.999010"]
        sub_type_list = ["K_1M"]

        for code in stock_code_list:
            for ktype in ["K_1M"]:
                ret_code, ret_data = self.__quote_ctx.get_cur_kline(code, number, ktype)
                if ret_code == RET_ERROR:
                    print(code, ktype, ret_data)
                    return
                kline_table = ret_data
#                print(kline_table)
                # Make Data List
                self.ma_1m_table = kline_table
                return self.ma_1m_table

    def cal_delta_ma(self):
        K_NO = 26
        try:
            kline = self.ma_1m_table
        except:
            return
        self.deltaMA20_cur = (kline.iloc[K_NO - 2, 3] - kline.iloc[K_NO - 22, 3])/20
        self.deltaMA20_cur = round(self.deltaMA20_cur, 2)
        self.deltaMA20_ma3 = (kline.iloc[K_NO - 2, 3] + kline.iloc[K_NO - 3, 3] + kline.iloc[K_NO - 4, 3] - kline.iloc[K_NO - 22, 3] - kline.iloc[K_NO - 23, 3] - kline.iloc[K_NO - 24, 3])/60
        self.deltaMA20_ma3 = round(self.deltaMA20_ma3, 2)
        self.deltaMA20_ma5 = (kline.iloc[K_NO - 2, 3] + kline.iloc[K_NO - 3, 3] + kline.iloc[K_NO - 4, 3] + kline.iloc[K_NO - 5, 3] + kline.iloc[K_NO - 6, 3] - kline.iloc[K_NO - 22, 3] - kline.iloc[K_NO - 23, 3] - kline.iloc[K_NO - 24, 3] - kline.iloc[K_NO - 25, 3] - kline.iloc[K_NO - 26, 3]) / 100
        self.deltaMA20_ma5 = round(self.deltaMA20_ma5, 2)

        self.deltaMA10_cur = (kline.iloc[K_NO - 2, 3] - kline.iloc[K_NO - 12, 3])/10
        self.deltaMA10_cur = round(self.deltaMA10_cur, 2)
        self.deltaMA10_ma3 = (kline.iloc[K_NO - 2, 3] + kline.iloc[K_NO - 3, 3] + kline.iloc[K_NO - 4, 3] - kline.iloc[K_NO - 12, 3] - kline.iloc[K_NO - 13, 3] - kline.iloc[K_NO - 14, 3])/30
        self.deltaMA10_ma3 = round(self.deltaMA10_ma3, 2)
        self.deltaMA10_ma5 = (kline.iloc[K_NO - 2, 3] + kline.iloc[K_NO - 3, 3] + kline.iloc[K_NO - 4, 3] + kline.iloc[K_NO - 5, 3] + kline.iloc[K_NO - 6, 3] - kline.iloc[K_NO - 12, 3] - kline.iloc[K_NO - 13, 3] - kline.iloc[K_NO - 14, 3] - kline.iloc[K_NO - 15, 3] - kline.iloc[K_NO - 16, 3]) / 50
        self.deltaMA10_ma5 = round(self.deltaMA10_ma5, 2)

        tmp = 0
        for i in range(0, 10):
            tmp += kline.iloc[K_NO - 2 - i, 3]
        self.MA10_cur = tmp/10
        self.MA10_cur = round(self.MA10_cur, 2)

        tmp = 0
        for i in range(0, 10):
            tmp += kline.iloc[K_NO - 4 - i, 3]
        self.MA10_3 = tmp/10
        self.MA10_3 = round(self.MA10_3, 2)

        tmp = 0
        for i in range(0, 20):
            tmp += kline.iloc[K_NO - 2 - i, 3]
        self.MA20_cur = tmp/20
        self.MA20_cur = round(self.MA20_cur, 2)

        tmp = 0
        for i in range(0, 20):
            tmp += kline.iloc[K_NO - 4 - i, 3]
        self.MA20_3 = tmp/20
        self.MA20_3 = round(self.MA20_3, 2)

        return

    def get_deltaMA20_cur(self):
        return self.deltaMA20_cur

    def get_deltaMA20_ma3(self):
        return self.deltaMA20_ma3

    def get_deltaMA20_ma5(self):
        return self.deltaMA20_ma5

    def get_deltaMA10_cur(self):
        return self.deltaMA10_cur

    def get_deltaMA10_ma3(self):
        return self.deltaMA10_ma3

    def get_deltaMA10_ma5(self):
        return self.deltaMA10_ma5

    def get_MA10_cur(self):
        return self.MA10_cur

    def get_MA10_3(self):
        return self.MA10_3

    def get_MA20_cur(self):
        return self.MA20_cur

    def get_MA20_3(self):
        return self.MA20_3

    def run(self):

        self.ready = 0
        ret_status = RET_OK
        ret_data = ""
        for i in range (0, self.subscribe_trail):
            ret_status, ret_data = self.subscribe_stock("QUOTE")
            if ret_status == RET_OK:
                break
            print("subscribe fail. Retry.")
            time.sleep(0.5)

        if ret_status == RET_ERROR:
            print("subscribe fail 3 times")
            return -1

        for i in range (0, self.subscribe_trail):
            ret_status, ret_data = self.subscribe_stock("K_1M")
            if ret_status == RET_OK:
                break
            print("subscribe fail. Retry.")
            time.sleep(0.5)

        if ret_status == RET_ERROR:
            print("subscribe fail 3 times")
            return -1

        i = 300
        while(1):
            start = time.time()
            ret = self.get_cur_stock_quoto()
            if ret == RET_ERROR:
                continue
            self.get_ma_1m(26)
            self.cal_delta_ma()
            self.ready = 1
            end = time.time()
            dur = end - start
            if dur < 0:
                continue
            if self.refresh < dur:
                continue
            else:
                time.sleep(self.refresh - dur)
            i -= 1
        self.ready = 0