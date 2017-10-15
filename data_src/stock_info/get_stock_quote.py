from openft.open_quant_context import *
import threading
import time


class get_stock_quote(threading.Thread):
    def __init__(self, qc,  bull_code, bear_code, stock_code="HK_FUTURE.999010", cycle= 0.25):
        super(get_stock_quote, self).__init__()
        self.__quote_ctx = qc
        self.stock_code_list = [stock_code, bull_code, bear_code]
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
        self.k_num = 56

        ### For Quote
        self.bull_bid = -1
        self.bull_ask = -1
        self.bear_bid = -1
        self.bear_ask = -1
        self.bull_bid_seller = -1
        self.bull_ask_seller = -1
        self.bear_bid_seller = -1
        self.bear_ask_seller = -1

        self.MA20_vol = 0
        self.MA20_vol_last = 0
        self.vol_last = 0
        self.vol_now = 0

        self.ma5_list = []

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
        #print("Quoto", ret_data)
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

    def find_seller(self, ask_or_bid, seller_ident):
        max_val = seller_ident * 1000000
        count = 0
        pos = -1
        for item in ask_or_bid:
            if item[1] > max_val:
                pos = count
                break
            count += 1
        return pos

    def get_ask_bid(self):
        seller_ident = 10

        ret_status, ret_data = self.__quote_ctx.get_order_book(self.stock_code_list[1])
        if ret_status == RET_ERROR:
            return RET_ERROR

        self.bull_bid = ret_data["Bid"][0][0]
        self.bull_ask = ret_data["Ask"][0][0]

        pos = self.find_seller(ret_data["Bid"], seller_ident)
        if pos != -1:
            self.bull_bid_seller = ret_data["Bid"][pos][0]
        else:
            self.bull_bid_seller = -1

        pos = self.find_seller(ret_data["Ask"], seller_ident)
        if pos != -1:
            self.bull_ask_seller = ret_data["Ask"][pos][0]
        else:
            self.bull_ask_seller = -1

        ret_status, ret_data = self.__quote_ctx.get_order_book(self.stock_code_list[2])
        if ret_status == RET_ERROR:
            return RET_ERROR

        self.bear_bid = ret_data["Bid"][0][0]
        self.bear_ask = ret_data["Ask"][0][0]

        pos = self.find_seller(ret_data["Bid"], seller_ident)
        if pos != -1:
            self.bear_bid_seller = ret_data["Bid"][pos][0]
        else:
            self.bear_bid_seller = -1

        pos = self.find_seller(ret_data["Ask"], seller_ident)
        if pos != -1:
            self.bear_ask_seller = ret_data["Ask"][pos][0]
        else:
            self.bear_ask_seller = -1

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

        stock_code_list = [self.stock_code_list[0]]
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

    def cal_vol_ma(self):
        K_NO = self.k_num
        try:
            kline = self.ma_1m_table
        except:
            return

        tmp = 0
        for i in range(0, 20):
            tmp += int(kline.iloc[K_NO - 1 - i, 6])
        MA20_vol = tmp/20
        self.MA20_vol = round(MA20_vol, 2)

        tmp = 0
        for i in range(0, 20):
            tmp += int(kline.iloc[K_NO - 2 - i, 6])
        MA20_vol_last = tmp/20
        self.MA20_vol_last = round(MA20_vol_last, 2)


        self.vol_last = int(kline.iloc[K_NO - 2, 6])
        self.vol_now = int(kline.iloc[K_NO - 1, 6])
        #print("VOL MA20:", self.MA20_vol, "Last:", self.vol_last, " now:", self.vol_now)

        return

    def get_ma20_vol(self):
        return self.MA20_vol

    def get_ma20_vol_last(self):
        return self.MA20_vol_last

    def get_vol_last(self):
        return self.vol_last

    def get_vol_now(self):
        return self.vol_now

    # From new to old
    def cal_MA5_list(self):
        K_NO = self.k_num
        if K_NO < 17:
            return

        try:
            kline = self.ma_1m_table
        except:
            return
        # ma_1m_table has gap where latest val equals 0
        if kline.iloc[K_NO - 1, 3] == 0:
            return
        ma5_list = []
        for i in range(0, 10):
            tmp = 0
            for j in range(0, 5):
                tmp += kline.iloc[K_NO - 1 - i - j, 3]
            ma5 = tmp / 5
            ma5 = round(ma5, 2)
            ma5_list.append(ma5)

        self.ma5_list = ma5_list
        return



    def cal_delta_ma(self):
        K_NO = self.k_num
        if K_NO < 56:
            return

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

        self.deltaMA50_cur = (kline.iloc[K_NO - 2, 3] - kline.iloc[K_NO - 52, 3])/50
        self.deltaMA50_cur = round(self.deltaMA50_cur, 2)

        # MA5
        tmp = 0
        for i in range(0, 5):
            tmp += kline.iloc[K_NO - 2 - i, 3]
        self.MA5_cur = tmp / 5
        self.MA5_cur = round(self.MA5_cur, 2)

        # MA10
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

        # MA20
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

        # MA50
        tmp = 0
        for i in range(0, 50):
            tmp += kline.iloc[K_NO - 2 - i, 3]
        self.MA50_cur = tmp/50
        self.MA50_cur = round(self.MA50_cur, 2)

        tmp = 0
        for i in range(0, 50):
            tmp += kline.iloc[K_NO - 4 - i, 3]
        self.MA50_3 = tmp/50
        self.MA50_3 = round(self.MA50_3, 2)

        return

    def get_deltaMA50_cur(self):
        return self.deltaMA50_cur

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

    def get_MA5_List(self):
        return self.ma5_list

    def get_MA10_cur(self):
        return self.MA10_cur

    def get_MA10_3(self):
        return self.MA10_3

    def get_MA20_cur(self):
        return self.MA20_cur

    def get_MA20_3(self):
        return self.MA20_3

    def get_MA50_cur(self):
        return self.MA50_cur

    def get_MA50_3(self):
        return self.MA50_3

    def get_bull_bid(self):
        return self.bull_bid

    def get_bull_ask(self):
        return self.bull_ask

    def get_bear_bid(self):
        return self.bear_bid

    def get_bear_ask(self):
        return self.bear_ask

    def get_bull_bid_seller(self):
        return self.bull_bid_seller

    def get_bull_ask_seller(self):
        return self.bull_ask_seller

    def get_bear_bid_seller(self):
        return self.bear_bid_seller

    def get_bear_ask_seller(self):
        return self.bear_ask_seller

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

        for i in range (0, self.subscribe_trail):
            ret_status, ret_data = self.subscribe_stock("ORDER_BOOK")
            if ret_status == RET_OK:
                break
            print("subscribe fail. Retry.")
            time.sleep(0.5)

        if ret_status == RET_ERROR:
            print("subscribe fail 3 times")
            return -1

        i = 180
        while(1):
            start = time.time()
            ret = self.get_cur_stock_quoto()
            if ret == RET_ERROR:
                continue

            start_time = "09:31:00"
            cur_time = self.data_time
            start_time_list = start_time.split(":")
            start_time_second = int(start_time_list[0]) * 3600 + int(start_time_list[1]) * 60 + int(start_time_list[2])
            cur_time_list = cur_time.split(":")
            cur_time_second = int(cur_time_list[0]) * 3600 + int(cur_time_list[1]) * 60 + int(cur_time_list[2])
            if cur_time_second >=start_time_second:
                ret = self.get_ask_bid()
                if ret == RET_ERROR:
                    continue

            self.get_ma_1m(self.k_num)
            self.cal_delta_ma()
            self.cal_MA5_list()
            self.cal_vol_ma()
            self.ready = 1
            end = time.time()
            dur = end - start
            if dur < 0:
                continue
            if self.refresh < dur:
                #print("quoto duration overtime")
                continue
            else:
                time.sleep(self.refresh - dur)
            #i -= 1
        self.ready = 0
        print("Quoto Dies")