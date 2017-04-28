from openft.open_quant_context import *
import threading
import time


class get_stock_quote(threading.Thread):
    def __init__(self, qc, stock_code="HK_FUTURE.999010", cycle= 0.2):
        super(get_stock_quote, self).__init__()
        self.__quote_ctx = qc
        self.stock_code_list = [stock_code]
        self.cur_stock_quoto = 0
        self.cur_stock_quoto_index = "last_price"
        self.data_time = ""
        self.data_time_index = "data_time"
        self.subscribe_trail = 3
        self.refresh = cycle
        self.ready = 0

    def subscribe_stock(self):
        # subscribe "QUOTE"
        for stk_code in self.stock_code_list:
            ret_status, ret_data = self.__quote_ctx.subscribe(stk_code, "QUOTE")
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
        if val == 0:
            print("Get Val = 0 skip")
            return RET_ERROR
        self.cur_stock_quoto = val
        self.data_time = cur_time
        return RET_OK

    def get_data_time(self):
        return self.data_time

    def get_stock_quoto(self):
        return self.cur_stock_quoto

    def run(self):
        self.ready = 0
        ret_status = RET_OK
        ret_data = ""
        for i in range (0, self.subscribe_trail):
            ret_status, ret_data = self.subscribe_stock()
            if ret_status == RET_OK:
                break
            print("subscribe fail. Retry.")
            time.sleep(0.5)

        if ret_status == RET_ERROR:
            print("subscribe fail 3 times")
            return -1
        i = 30
        while(i):
            start = time.time()
            ret = self.get_cur_stock_quoto()
            if ret == RET_ERROR:
                continue
            self.ready = 1
            end = time.time()
            dur = end - start
            if dur < 0:
                continue
            time.sleep(self.refresh - dur)
            i -= 1
        self.ready = 0